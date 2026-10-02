import os
import time
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Base URL strictly configured through .env via Django settings
def get_base_url():
    url = getattr(settings, 'JIKAN_API_BASE_URL', os.getenv('JIKAN_API_BASE_URL', ''))
    if not url:
        url = os.getenv('JIKAN_API_BASE_URL', '')
    return url.rstrip('/')

# In-memory simple cache with TTL (15 minutes)
_CACHE = {}
CACHE_TTL = 900


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


def _safe_request(endpoint_path, params=None, timeout=8):
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
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                _set_cache(cache_key, data)
                return data
            elif response.status_code == 429:
                logger.warning(f"Jikan API rate limit (429) on attempt {attempt + 1}. Waiting 0.6s...")
                time.sleep(0.6)
                continue
            elif response.status_code == 404:
                logger.info(f"Jikan resource not found (404): {url}")
                return None
            else:
                logger.warning(f"Jikan API responded with status {response.status_code} for {url}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to Jikan API at {url}: {e}")
            return None

    return None


def get_top_anime(limit=12, filter_type=None):
    params = {'limit': limit}
    if filter_type:
        params['filter'] = filter_type
    data = _safe_request("/top/anime", params=params)
    if data and 'data' in data:
        return data['data']
    return []


def get_top_manga(limit=12):
    params = {'limit': limit, 'type': 'manga'}
    data = _safe_request("/top/manga", params=params)
    if data and 'data' in data:
        return data['data']
    return []


def get_top_lightnovels(limit=12):
    params = {'limit': limit, 'type': 'lightnovel'}
    data = _safe_request("/top/manga", params=params)
    if data and 'data' in data:
        return data['data']
    return []


def search_items(category='anime', query='', genre='', status='', order_by='score', sort='desc', page=1):
    """
    Search mangas, animes or light novels with real-time filters via Jikan API v4:
    category: 'anime' | 'manga' | 'lightnovel'
    """
    params = {
        'page': page,
        'limit': 18,
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

    if category == 'anime':
        endpoint = "/anime"
    elif category == 'lightnovel':
        endpoint = "/manga"
        params['type'] = 'lightnovel'
    else:
        endpoint = "/manga"
        params['type'] = 'manga'

    data = _safe_request(endpoint, params=params)
    if data and 'data' in data:
        return {
            'items': data.get('data', []),
            'pagination': data.get('pagination', {}),
        }

    return {
        'items': [],
        'pagination': {'has_next_page': False, 'current_page': page, 'items': {'count': 0}}
    }


def get_item_detail(item_type, mal_id):
    endpoint = f"/anime/{mal_id}/full" if item_type == 'anime' else f"/manga/{mal_id}/full"
    data = _safe_request(endpoint)
    if data and 'data' in data:
        return data['data']
    return None


def get_common_genres():
    """
    Standard MyAnimeList canonical genre taxonomy for filtering
    """
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
