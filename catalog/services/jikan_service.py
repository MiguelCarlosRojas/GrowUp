import os
import time
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Request Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

# In-memory cache for API responses and real items catalog
_CACHE = {}
_ITEMS_REGISTRY = {}
CACHE_TTL = 900  # 15 minutes


def get_base_url():
    url = getattr(settings, 'JIKAN_API_BASE_URL', os.getenv('JIKAN_API_BASE_URL', ''))
    if not url:
        url = os.getenv('JIKAN_API_BASE_URL', 'https://api.jikan.moe/v4')
    return url.rstrip('/')


def _get_cache(key):
    if key in _CACHE:
        data, expire_at = _CACHE[key]
        if time.time() < expire_at:
            return data
        else:
            del _CACHE[key]
    return None


def _set_cache(key, data):
    _CACHE[key] = (data, time.time() + CACHE_TTL)


def _register_items(items):
    """Registers real items in memory for fast lookup during detail views and search fallback."""
    for it in items:
        if isinstance(it, dict) and it.get('mal_id'):
            _ITEMS_REGISTRY[str(it['mal_id'])] = it


def _safe_request(endpoint_path, params=None, timeout=10):
    base_url = get_base_url()
    if not base_url:
        logger.error("JIKAN_API_BASE_URL is not configured in .env")
        return None

    url = f"{base_url}{endpoint_path}"
    cache_key = f"{url}?{sorted(params.items()) if params else ''}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    for attempt in range(2):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                _set_cache(cache_key, data)
                return data
            elif response.status_code == 429:
                logger.warning(f"Jikan API rate limit (429) on attempt {attempt + 1}. Waiting 0.8s...")
                time.sleep(0.8)
                continue
            elif response.status_code in (504, 502, 503):
                logger.warning(f"Jikan API gateway {response.status_code} on {url}. Retrying...")
                time.sleep(0.5)
                continue
            elif response.status_code == 404:
                return None
            else:
                logger.warning(f"Jikan API responded with status {response.status_code} for {url}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to Jikan API at {url}: {e}")
            time.sleep(0.5)

    return None


def get_top_anime(limit=8):
    # Fetch from Jikan pre-cached /top/anime (without query params to avoid 504 on Jikan)
    data = _safe_request("/top/anime")
    items = []
    if data and 'data' in data and data['data']:
        items = data['data']
    else:
        season_data = _safe_request("/seasons/now")
        if season_data and 'data' in season_data and season_data['data']:
            items = season_data['data']

    _register_items(items)
    return items[:limit]


def _fetch_all_top_manga():
    """Fetches real top manga and light novels from Jikan's pre-cached server endpoint."""
    cache_key = "all_top_manga_cached"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    data = _safe_request("/top/manga")
    if data and 'data' in data and data['data']:
        items = data['data']
        _set_cache(cache_key, items)
        _register_items(items)
        return items

    return []


def get_top_manga(limit=8):
    all_items = _fetch_all_top_manga()
    mangas = [
        it for it in all_items
        if it.get('type') in ('Manga', 'Manhwa', 'Manhua', 'One-shot', None, '')
    ]
    return mangas[:limit]


def get_top_lightnovels(limit=8):
    all_items = _fetch_all_top_manga()
    novels = [
        it for it in all_items
        if it.get('type') in ('Novel', 'Lightnovel', 'Light Novel')
    ]
    return novels[:limit]


def search_items(category='anime', query='', genre='', status='', order_by='score', sort='desc', page=1):
    """
    Search mangas, animes or light novels with real-time filters via Jikan API v4.
    """
    # First, ensure baseline catalog is loaded into memory
    if category == 'anime':
        base_pool = get_top_anime(limit=25)
    elif category == 'lightnovel':
        base_pool = get_top_lightnovels(limit=25)
    else:
        base_pool = get_top_manga(limit=25)

    params = {
        'page': page,
        'sfw': 'true',
    }
    if query:
        params['q'] = query
    if genre:
        params['genres'] = genre
    if status:
        params['status'] = status
    if order_by:
        params['order_by'] = order_by
    if sort:
        params['sort'] = sort

    endpoint = "/anime" if category == 'anime' else "/manga"
    data = _safe_request(endpoint, params=params)

    if data and 'data' in data and data['data']:
        items = data['data']
        _register_items(items)
        if category == 'lightnovel':
            items = [it for it in items if it.get('type') in ('Novel', 'Lightnovel', 'Light Novel')]
        elif category == 'manga':
            items = [it for it in items if it.get('type') in ('Manga', 'Manhwa', 'Manhua', 'One-shot', None, '')]

        return {
            'items': items,
            'pagination': data.get('pagination', {}),
        }

    # If live search was rate-limited or timed out, filter the real baseline pool
    filtered = base_pool
    if query:
        q_lower = query.lower()
        filtered = [
            it for it in filtered
            if q_lower in it.get('title', '').lower() or q_lower in str(it.get('title_japanese', '')).lower()
        ]

    if genre:
        filtered = [
            it for it in filtered
            if any(str(g.get('mal_id')) == str(genre) for g in it.get('genres', []))
        ]

    if status:
        filtered = [
            it for it in filtered
            if status.lower() in str(it.get('status', '')).lower()
        ]

    return {
        'items': filtered,
        'pagination': {'has_next_page': False, 'current_page': page, 'items': {'count': len(filtered)}}
    }


def get_item_detail(item_type, mal_id):
    str_id = str(mal_id)
    # Check in-memory registry of real items first
    if str_id in _ITEMS_REGISTRY:
        return _ITEMS_REGISTRY[str_id]

    # Query endpoint without /full (fastest and cached on Jikan)
    endpoint = f"/anime/{mal_id}" if item_type == 'anime' else f"/manga/{mal_id}"
    data = _safe_request(endpoint)
    if data and 'data' in data:
        item = data['data']
        _ITEMS_REGISTRY[str_id] = item
        return item

    # Query /full endpoint if standard endpoint did not return
    data_full = _safe_request(f"{endpoint}/full")
    if data_full and 'data' in data_full:
        item = data_full['data']
        _ITEMS_REGISTRY[str_id] = item
        return item

    return None


def get_common_genres():
    return [
        {'id': 1, 'name': 'Acción'},
        {'id': 2, 'name': 'Aventura'},
        {'id': 4, 'name': 'Comedia'},
        {'id': 8, 'name': 'Drama'},
        {'id': 10, 'name': 'Fantasía'},
        {'id': 14, 'name': 'Horror'},
        {'id': 7, 'name': 'Misterio'},
        {'id': 22, 'name': 'Romance'},
        {'id': 24, 'name': 'Ciencia Ficción'},
        {'id': 36, 'name': 'Recuentos de la Vida'},
        {'id': 30, 'name': 'Deportes'},
        {'id': 37, 'name': 'Sobrenatural'},
        {'id': 62, 'name': 'Isekai'},
    ]
