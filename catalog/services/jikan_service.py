import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BASE_URL = settings.JIKAN_API_BASE_URL.rstrip('/')
CACHE_TTL = settings.JIKAN_CACHE_TTL
DEFAULT_TIMEOUT = settings.JIKAN_API_TIMEOUT
TOP_LIMIT = settings.JIKAN_TOP_LIMIT
SEARCH_LIMIT = settings.JIKAN_SEARCH_LIMIT

# In-memory simple cache with TTL
_CACHE = {}


def _get_cache(key):
    if key in _CACHE:
        data, expire_at = _CACHE[key]
        if time.time() < expire_at:
            return data
        del _CACHE[key]
    return None


def _set_cache(key, data):
    _CACHE[key] = (data, time.time() + CACHE_TTL)


def _safe_request(url, params=None, timeout=DEFAULT_TIMEOUT):
    cache_key = f"{url}?{sorted(params.items()) if params else ''}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    try:
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            _set_cache(cache_key, data)
            return data
        if response.status_code == 429:
            logger.warning("Jikan API rate limit (429) hit.")
            return None

        logger.warning("Jikan API request failed with status %s for %s", response.status_code, url)
    except requests.RequestException as exc:
        logger.error("Error connecting to Jikan API: %s", exc)

    return None


def get_top_anime(limit=TOP_LIMIT, filter_type=None):
    params = {'limit': limit}
    if filter_type:
        params['filter'] = filter_type
    data = _safe_request(f"{BASE_URL}/top/anime", params=params)
    return data.get('data', []) if data else []


def get_top_manga(limit=TOP_LIMIT):
    params = {'limit': limit, 'type': 'manga'}
    data = _safe_request(f"{BASE_URL}/top/manga", params=params)
    return data.get('data', []) if data else []


def get_top_lightnovels(limit=TOP_LIMIT):
    params = {'limit': limit, 'type': 'lightnovel'}
    data = _safe_request(f"{BASE_URL}/top/manga", params=params)
    return data.get('data', []) if data else []


def search_items(category='anime', query='', genre='', status='', order_by='score', sort='desc', page=1):
    """
    Search mangas, animes or light novels with extensive filters:
    category: 'anime' | 'manga' | 'lightnovel'
    """
    params = {
        'page': page,
        'limit': SEARCH_LIMIT,
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
        endpoint = f"{BASE_URL}/anime"
    elif category == 'lightnovel':
        endpoint = f"{BASE_URL}/manga"
        params['type'] = 'lightnovel'
    else:
        endpoint = f"{BASE_URL}/manga"
        params['type'] = 'manga'

    data = _safe_request(endpoint, params=params)
    if not data:
        return {
            'items': [],
            'pagination': {'has_next_page': False, 'current_page': 1, 'items': {'count': 0}},
        }

    return {
        'items': data.get('data', []),
        'pagination': data.get('pagination', {}),
    }


def get_item_detail(item_type, mal_id):
    endpoint = f"{BASE_URL}/anime/{mal_id}/full" if item_type == 'anime' else f"{BASE_URL}/manga/{mal_id}/full"
    data = _safe_request(endpoint)
    return data.get('data') if data else None


def get_common_genres():
    data = _safe_request(f"{BASE_URL}/genres/anime")
    if not data:
        return []

    genres = []
    for item in data.get('data', []):
        mal_id = item.get('mal_id')
        name = item.get('name')
        if mal_id and name:
            genres.append({'id': mal_id, 'name': name})
    return genres
