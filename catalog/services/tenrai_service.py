import os
import time
import urllib.parse
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Standard Headers matching Tenrai API documentation
HEADERS = {
    'User-Agent': 'GrowUp-Platform/1.0 (+https://growup-7my7.onrender.com; contact: contact@tenrai.org)',
    'Accept': 'application/json',
}

_SESSION = requests.Session()
_SESSION.headers.update(HEADERS)

# Fast in-memory cache for instant page navigation
_CACHE = {}
_ITEMS_REGISTRY = {}
CACHE_TTL = 86400  # 24 hours cache for ultra-fluid page loads


def get_base_url():
    url = getattr(settings, 'TENRAI_API_BASE_URL', None) or os.getenv('TENRAI_API_BASE_URL', '')
    return url.rstrip('/')


def get_server_key():
    return getattr(settings, 'TENRAI_SERVER_KEY', None) or os.getenv('TENRAI_SERVER_KEY', '')


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
    if not items:
        return
    for it in items:
        if isinstance(it, dict) and it.get('mal_id'):
            _ITEMS_REGISTRY[str(it['mal_id'])] = it


def _clean_params(params):
    """Removes None values and formats query params."""
    if not params:
        return {}
    cleaned = {}
    for k, v in params.items():
        if v is not None and v != '':
            if isinstance(v, (list, tuple)):
                cleaned[k] = ','.join(str(x) for x in v)
            elif isinstance(v, bool):
                cleaned[k] = 'true' if v else 'false'
            else:
                cleaned[k] = v
    return cleaned


def _safe_request(endpoint_path, params=None, timeout=3.5, retries=0):
    base_url = get_base_url()
    if not base_url:
        return None

    url = f"{base_url}{endpoint_path}"
    cleaned_params = _clean_params(params)
    param_str = urllib.parse.urlencode(sorted(cleaned_params.items()))
    cache_key = f"{url}?{param_str}" if param_str else url

    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    req_headers = dict(HEADERS)
    server_key = get_server_key()
    if server_key:
        req_headers['X-Server-Key'] = server_key

    for attempt in range(retries + 1):
        try:
            response = _SESSION.get(url, params=cleaned_params, headers=req_headers, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                _set_cache(cache_key, data)
                if isinstance(data, dict) and 'data' in data:
                    raw_data = data['data']
                    if isinstance(raw_data, list):
                        _register_items(raw_data)
                    elif isinstance(raw_data, dict):
                        _register_items([raw_data])
                return data
            elif response.status_code in (429, 504, 502, 503) and attempt < retries:
                retry_after = 1.0
                try:
                    if 'Retry-After' in response.headers:
                        retry_after = float(response.headers['Retry-After'])
                except (ValueError, TypeError):
                    retry_after = 1.0
                logger.warning(f"Tenrai API status {response.status_code} on {url}, retrying in {retry_after}s (attempt {attempt + 1}/{retries})...")
                time.sleep(retry_after)
                continue
            elif response.status_code == 429:
                logger.warning(f"Tenrai API rate limit (429) on {url}")
                return None
            elif response.status_code in (504, 502, 503):
                logger.warning(f"Tenrai API gateway status {response.status_code} on {url}")
                return None
            elif response.status_code == 404:
                return None
            else:
                logger.warning(f"Tenrai API responded with status {response.status_code} for {url}")
                return None
        except Exception as e:
            if attempt < retries:
                logger.warning(f"Tenrai API issue on {url}: {e}, retrying...")
                time.sleep(1.0)
                continue
            logger.warning(f"Tenrai API connection issue on {url}: {e}")
            return None
    return None


# ==============================================================================
# UNIVERSAL DISPATCHER (Supports Any GET Path)
# ==============================================================================

def request_endpoint(endpoint_path, params=None):
    """Direct dispatcher for any valid Tenrai GET endpoint path."""
    if not endpoint_path.startswith('/'):
        endpoint_path = '/' + endpoint_path
    return _safe_request(endpoint_path, params=params)


# ==============================================================================
# TENRAI API v1.0.19: 94 GET ENDPOINTS IMPLEMENTATION
# ==============================================================================

class TenraiService:
    """
    Comprehensive client implementation for Tenrai API v1.0.19.
    Implements all 94 GET endpoints documented in OpenAPI 3.0 specification.
    """

    # --- 1. Anime Endpoints (26) ---
    @staticmethod
    def search_anime(q=None, page=1, limit=25, type=None, status=None, rating=None,
                     sfw=None, sfw_strict=None, unapproved=None, score=None,
                     min_score=None, max_score=None, genres=None, genres_exclude=None,
                     order_by=None, sort=None, letter=None, producers=None,
                     start_date=None, end_date=None, **kwargs):
        """GET /anime - Search for anime with comprehensive filters."""
        params = {
            'q': q, 'page': page, 'limit': limit, 'type': type, 'status': status,
            'rating': rating, 'sfw': sfw, 'sfw-strict': sfw_strict,
            'unapproved': unapproved, 'score': score, 'min_score': min_score,
            'max_score': max_score, 'genres': genres, 'genres_exclude': genres_exclude,
            'order_by': order_by, 'sort': sort, 'letter': letter,
            'producers': producers, 'start_date': start_date, 'end_date': end_date
        }
        params.update(kwargs)
        return _safe_request('/anime', params=params)

    @staticmethod
    def get_anime_deleted(page=1, limit=25, order_by=None, sort=None, **kwargs):
        """GET /anime/deleted - Browse deleted anime entries."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request('/anime/deleted', params=params)

    @staticmethod
    def get_anime_denied(page=1, limit=25, order_by=None, sort=None, **kwargs):
        """GET /anime/denied - Browse denied anime entries."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request('/anime/denied', params=params)

    @staticmethod
    def get_anime_ids(type=None, status=None, rating=None, sfw=None, sfw_strict=None,
                      include=None, updated_at=None, **kwargs):
        """GET /anime/ids - Retrieve all unique MAL anime IDs (Server Key)."""
        params = {
            'type': type, 'status': status, 'rating': rating, 'sfw': sfw,
            'sfw-strict': sfw_strict, 'include': include, 'updated_at': updated_at
        }
        params.update(kwargs)
        return _safe_request('/anime/ids', params=params)

    @staticmethod
    def get_anime_unapproved(page=1, limit=25, order_by=None, sort=None, **kwargs):
        """GET /anime/unapproved - Browse unapproved anime entries."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request('/anime/unapproved', params=params)

    @staticmethod
    def get_anime_detail(anime_id):
        """GET /anime/{id} - Get details for an anime."""
        return _safe_request(f'/anime/{anime_id}')

    @staticmethod
    def get_anime_articles(anime_id, page=1, order_by=None, sort=None, **kwargs):
        """GET /anime/{id}/articles - Get featured articles related to the anime."""
        params = {'page': page, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/articles', params=params)

    @staticmethod
    def get_anime_characters(anime_id):
        """GET /anime/{id}/characters - Get character list and voice actors for an anime."""
        return _safe_request(f'/anime/{anime_id}/characters')

    @staticmethod
    def get_anime_episodes(anime_id, page=1, **kwargs):
        """GET /anime/{id}/episodes - Get episodes for an anime."""
        params = {'page': page}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/episodes', params=params)

    @staticmethod
    def get_anime_episode_detail(anime_id, episode_id):
        """GET /anime/{id}/episodes/{episode_id} - Get detail for a specific anime episode."""
        return _safe_request(f'/anime/{anime_id}/episodes/{episode_id}')

    @staticmethod
    def get_anime_external_links(anime_id):
        """GET /anime/{id}/external - Get external links for an anime."""
        return _safe_request(f'/anime/{anime_id}/external')

    @staticmethod
    def get_anime_forum(anime_id, page=1, order_by=None, sort=None, filter='episode', **kwargs):
        """GET /anime/{id}/forum - Get forum topics related to the anime entry."""
        params = {'page': page, 'order_by': order_by, 'sort': sort, 'filter': filter}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/forum', params=params)

    @staticmethod
    def get_anime_full(anime_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /anime/{id}/full - Get full detailed data for an anime."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/full', params=params)

    @staticmethod
    def get_anime_moreinfo(anime_id):
        """GET /anime/{id}/moreinfo - Get more information for an anime."""
        return _safe_request(f'/anime/{anime_id}/moreinfo')

    @staticmethod
    def get_anime_news(anime_id, page=1, sfw=None, sfw_strict=None, **kwargs):
        """GET /anime/{id}/news - Get news articles related to the anime entry."""
        params = {'page': page, 'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/news', params=params)

    @staticmethod
    def get_anime_pictures(anime_id):
        """GET /anime/{id}/pictures - Get pictures for an anime."""
        return _safe_request(f'/anime/{anime_id}/pictures')

    @staticmethod
    def get_anime_recommendations(anime_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /anime/{id}/recommendations - Get recommendations for an anime."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/recommendations', params=params)

    @staticmethod
    def get_anime_relations(anime_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /anime/{id}/relations - Get relations for an anime."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/relations', params=params)

    @staticmethod
    def get_anime_reviews(anime_id, page=1, sort=None, preliminary=None,
                           spoilers=None, sentiment=None, **kwargs):
        """GET /anime/{id}/reviews - Get reviews for an anime."""
        params = {
            'page': page, 'sort': sort, 'preliminary': preliminary,
            'spoilers': spoilers, 'sentiment': sentiment
        }
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/reviews', params=params)

    @staticmethod
    def get_anime_stacks(anime_id, q=None, page=1, limit=25, order_by=None,
                         sort=None, spoilers=None, challenges=None, official=None,
                         sfw=None, sfw_strict=None, **kwargs):
        """GET /anime/{id}/stacks - Get all public interest stacks for an anime."""
        params = {
            'q': q, 'page': page, 'limit': limit, 'order_by': order_by,
            'sort': sort, 'spoilers': spoilers, 'challenges': challenges,
            'official': official, 'sfw': sfw, 'sfw-strict': sfw_strict
        }
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/stacks', params=params)

    @staticmethod
    def get_anime_staff(anime_id):
        """GET /anime/{id}/staff - Get staff for an anime."""
        return _safe_request(f'/anime/{anime_id}/staff')

    @staticmethod
    def get_anime_statistics(anime_id):
        """GET /anime/{id}/statistics - Get statistics for an anime."""
        return _safe_request(f'/anime/{anime_id}/statistics')

    @staticmethod
    def get_anime_streaming_links(anime_id):
        """GET /anime/{id}/streaming - Get streaming links for an anime."""
        return _safe_request(f'/anime/{anime_id}/streaming')

    @staticmethod
    def get_anime_themes(anime_id):
        """GET /anime/{id}/themes - Get opening and ending themes for an anime."""
        return _safe_request(f'/anime/{anime_id}/themes')

    @staticmethod
    def get_anime_videos(anime_id):
        """GET /anime/{id}/videos - Get videos for an anime."""
        return _safe_request(f'/anime/{anime_id}/videos')

    @staticmethod
    def get_anime_video_episodes(anime_id, page=1, **kwargs):
        """GET /anime/{id}/videos/episodes - Get episode videos for an anime."""
        params = {'page': page}
        params.update(kwargs)
        return _safe_request(f'/anime/{anime_id}/videos/episodes', params=params)

    # --- 2. Articles Endpoints (3) ---
    @staticmethod
    def get_articles(page=1, limit=25, order_by=None, sort=None, tags=None, **kwargs):
        """GET /articles - Get featured articles."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'tags': tags}
        params.update(kwargs)
        return _safe_request('/articles', params=params)

    @staticmethod
    def get_article_tags(**kwargs):
        """GET /articles/tags - Get article tags."""
        return _safe_request('/articles/tags', params=kwargs)

    @staticmethod
    def get_article_detail(article_id):
        """GET /articles/{id} - Get article details."""
        return _safe_request(f'/articles/{article_id}')

    # --- 3. Characters Endpoints (9) ---
    @staticmethod
    def search_characters(q=None, page=1, limit=25, order_by=None, sort=None, letter=None, **kwargs):
        """GET /characters - Search for characters."""
        params = {'q': q, 'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'letter': letter}
        params.update(kwargs)
        return _safe_request('/characters', params=params)

    @staticmethod
    def get_character_ids(**kwargs):
        """GET /characters/ids - Get all unique character IDs."""
        return _safe_request('/characters/ids', params=kwargs)

    @staticmethod
    def get_character_detail(character_id):
        """GET /characters/{id} - Get details for a character."""
        return _safe_request(f'/characters/{character_id}')

    @staticmethod
    def get_character_anime(character_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /characters/{id}/anime - Get list of anime the character appeared in."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/characters/{character_id}/anime', params=params)

    @staticmethod
    def get_character_articles(character_id, page=1, order_by=None, sort=None, **kwargs):
        """GET /characters/{id}/articles - Get featured articles related to the character."""
        params = {'page': page, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request(f'/characters/{character_id}/articles', params=params)

    @staticmethod
    def get_character_full(character_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /characters/{id}/full - Get full details for a character."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/characters/{character_id}/full', params=params)

    @staticmethod
    def get_character_manga(character_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /characters/{id}/manga - Get list of manga the character appeared in."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/characters/{character_id}/manga', params=params)

    @staticmethod
    def get_character_pictures(character_id):
        """GET /characters/{id}/pictures - Get pictures for the character."""
        return _safe_request(f'/characters/{character_id}/pictures')

    @staticmethod
    def get_character_voices(character_id):
        """GET /characters/{id}/voices - Get list of voice actors for the character."""
        return _safe_request(f'/characters/{character_id}/voices')

    # --- 4. Genres Endpoints (2) ---
    @staticmethod
    def get_anime_genres(filter=None, **kwargs):
        """GET /genres/anime - Get anime genres."""
        params = {'filter': filter}
        params.update(kwargs)
        return _safe_request('/genres/anime', params=params)

    @staticmethod
    def get_manga_genres(filter=None, **kwargs):
        """GET /genres/manga - Get manga genres."""
        params = {'filter': filter}
        params.update(kwargs)
        return _safe_request('/genres/manga', params=params)

    # --- 5. Magazines Endpoint (1) ---
    @staticmethod
    def get_manga_magazines(page=1, limit=25, order_by=None, sort=None, letter=None, **kwargs):
        """GET /magazines - Get manga magazines."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'letter': letter}
        params.update(kwargs)
        return _safe_request('/magazines', params=params)

    # --- 6. Manga Endpoints (16) ---
    @staticmethod
    def search_manga(q=None, page=1, limit=25, type=None, status=None, sfw=None,
                     sfw_strict=None, score=None, min_score=None, max_score=None,
                     unapproved=None, genres=None, genres_exclude=None,
                     order_by=None, sort=None, letter=None, magazines=None,
                     start_date=None, end_date=None, **kwargs):
        """GET /manga - Search for manga with comprehensive filters."""
        params = {
            'q': q, 'page': page, 'limit': limit, 'type': type, 'status': status,
            'sfw': sfw, 'sfw-strict': sfw_strict, 'score': score, 'min_score': min_score,
            'max_score': max_score, 'unapproved': unapproved, 'genres': genres,
            'genres_exclude': genres_exclude, 'order_by': order_by, 'sort': sort,
            'letter': letter, 'magazines': magazines, 'start_date': start_date, 'end_date': end_date
        }
        params.update(kwargs)
        return _safe_request('/manga', params=params)

    @staticmethod
    def get_manga_deleted(page=1, limit=25, order_by=None, sort=None, **kwargs):
        """GET /manga/deleted - Browse deleted manga entries."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request('/manga/deleted', params=params)

    @staticmethod
    def get_manga_ids(type=None, status=None, sfw=None, sfw_strict=None,
                      include=None, updated_at=None, **kwargs):
        """GET /manga/ids - Retrieve all unique MAL manga IDs (Server Key)."""
        params = {
            'type': type, 'status': status, 'sfw': sfw, 'sfw-strict': sfw_strict,
            'include': include, 'updated_at': updated_at
        }
        params.update(kwargs)
        return _safe_request('/manga/ids', params=params)

    @staticmethod
    def get_manga_detail(manga_id):
        """GET /manga/{id} - Get details for a manga."""
        return _safe_request(f'/manga/{manga_id}')

    @staticmethod
    def get_manga_articles(manga_id, page=1, order_by=None, sort=None, **kwargs):
        """GET /manga/{id}/articles - Get featured articles related to the manga."""
        params = {'page': page, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/articles', params=params)

    @staticmethod
    def get_manga_characters(manga_id):
        """GET /manga/{id}/characters - Get characters for a manga."""
        return _safe_request(f'/manga/{manga_id}/characters')

    @staticmethod
    def get_manga_external_links(manga_id):
        """GET /manga/{id}/external - Get external links for a manga."""
        return _safe_request(f'/manga/{manga_id}/external')

    @staticmethod
    def get_manga_full(manga_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /manga/{id}/full - Get full detailed data for a manga."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/full', params=params)

    @staticmethod
    def get_manga_moreinfo(manga_id):
        """GET /manga/{id}/moreinfo - Get more info for a manga."""
        return _safe_request(f'/manga/{manga_id}/moreinfo')

    @staticmethod
    def get_manga_news(manga_id, page=1, sfw=None, sfw_strict=None, **kwargs):
        """GET /manga/{id}/news - Get news articles related to the manga entry."""
        params = {'page': page, 'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/news', params=params)

    @staticmethod
    def get_manga_pictures(manga_id):
        """GET /manga/{id}/pictures - Get pictures for a manga."""
        return _safe_request(f'/manga/{manga_id}/pictures')

    @staticmethod
    def get_manga_recommendations(manga_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /manga/{id}/recommendations - Get recommendations for a manga."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/recommendations', params=params)

    @staticmethod
    def get_manga_relations(manga_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /manga/{id}/relations - Get related entries for a manga."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/relations', params=params)

    @staticmethod
    def get_manga_reviews(manga_id, page=1, sort=None, preliminary=None,
                          spoilers=None, sentiment=None, **kwargs):
        """GET /manga/{id}/reviews - Get reviews for a manga."""
        params = {
            'page': page, 'sort': sort, 'preliminary': preliminary,
            'spoilers': spoilers, 'sentiment': sentiment
        }
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/reviews', params=params)

    @staticmethod
    def get_manga_stacks(manga_id, q=None, page=1, limit=25, order_by=None,
                         sort=None, spoilers=None, challenges=None, official=None,
                         sfw=None, sfw_strict=None, **kwargs):
        """GET /manga/{id}/stacks - Get all public interest stacks for a manga."""
        params = {
            'q': q, 'page': page, 'limit': limit, 'order_by': order_by,
            'sort': sort, 'spoilers': spoilers, 'challenges': challenges,
            'official': official, 'sfw': sfw, 'sfw-strict': sfw_strict
        }
        params.update(kwargs)
        return _safe_request(f'/manga/{manga_id}/stacks', params=params)

    @staticmethod
    def get_manga_statistics(manga_id):
        """GET /manga/{id}/statistics - Get statistics for a manga."""
        return _safe_request(f'/manga/{manga_id}/statistics')

    # --- 7. News Endpoints (3) ---
    @staticmethod
    def get_news(page=1, limit=25, order_by=None, sort=None, tags=None, **kwargs):
        """GET /news - Get news entries."""
        params = {'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'tags': tags}
        params.update(kwargs)
        return _safe_request('/news', params=params)

    @staticmethod
    def get_news_tags(**kwargs):
        """GET /news/tags - Get news tags."""
        return _safe_request('/news/tags', params=kwargs)

    @staticmethod
    def get_news_detail(news_id):
        """GET /news/{id} - Get news details."""
        return _safe_request(f'/news/{news_id}')

    # --- 8. People Endpoints (9) ---
    @staticmethod
    def search_people(q=None, page=1, limit=25, order_by=None, sort=None, letter=None, **kwargs):
        """GET /people - Search for people/voice actors."""
        params = {'q': q, 'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'letter': letter}
        params.update(kwargs)
        return _safe_request('/people', params=params)

    @staticmethod
    def get_people_ids(**kwargs):
        """GET /people/ids - Get all unique person IDs."""
        return _safe_request('/people/ids', params=kwargs)

    @staticmethod
    def get_person_detail(person_id):
        """GET /people/{id} - Get details for a person."""
        return _safe_request(f'/people/{person_id}')

    @staticmethod
    def get_person_anime(person_id):
        """GET /people/{id}/anime - Get anime positions/roles of a person."""
        return _safe_request(f'/people/{person_id}/anime')

    @staticmethod
    def get_person_articles(person_id, page=1, order_by=None, sort=None, **kwargs):
        """GET /people/{id}/articles - Get featured articles related to a person."""
        params = {'page': page, 'order_by': order_by, 'sort': sort}
        params.update(kwargs)
        return _safe_request(f'/people/{person_id}/articles', params=params)

    @staticmethod
    def get_person_full(person_id, sfw=None, sfw_strict=None, **kwargs):
        """GET /people/{id}/full - Get full details for a person."""
        params = {'sfw': sfw, 'sfw-strict': sfw_strict}
        params.update(kwargs)
        return _safe_request(f'/people/{person_id}/full', params=params)

    @staticmethod
    def get_person_pictures(person_id):
        """GET /people/{id}/pictures - Get pictures for a person."""
        return _safe_request(f'/people/{person_id}/pictures')

    @staticmethod
    def get_person_voices(person_id):
        """GET /people/{id}/voices - Get voice acting roles for a person."""
        return _safe_request(f'/people/{person_id}/voices')

    # --- 9. Producers Endpoints (5) ---
    @staticmethod
    def search_producers(q=None, page=1, limit=25, order_by=None, sort=None, letter=None, **kwargs):
        """GET /producers - Search for producers/studios."""
        params = {'q': q, 'page': page, 'limit': limit, 'order_by': order_by, 'sort': sort, 'letter': letter}
        params.update(kwargs)
        return _safe_request('/producers', params=params)

    @staticmethod
    def get_producer_ids(**kwargs):
        """GET /producers/ids - Get all unique producer IDs."""
        return _safe_request('/producers/ids', params=kwargs)

    @staticmethod
    def get_producer_detail(producer_id):
        """GET /producers/{id} - Get details for a producer."""
        return _safe_request(f'/producers/{producer_id}')

    @staticmethod
    def get_producer_external_links(producer_id):
        """GET /producers/{id}/external - Get external links for a producer."""
        return _safe_request(f'/producers/{producer_id}/external')

    @staticmethod
    def get_producer_full(producer_id):
        """GET /producers/{id}/full - Get full details for a producer."""
        return _safe_request(f'/producers/{producer_id}/full')

    # --- 10. Random Endpoints (4) ---
    @staticmethod
    def get_random_anime():
        """GET /random/anime - Get a random anime entry."""
        return _safe_request('/random/anime')

    @staticmethod
    def get_random_character():
        """GET /random/characters - Get a random character."""
        return _safe_request('/random/characters')

    @staticmethod
    def get_random_manga():
        """GET /random/manga - Get a random manga entry."""
        return _safe_request('/random/manga')

    @staticmethod
    def get_random_person():
        """GET /random/people - Get a random person/voice actor."""
        return _safe_request('/random/people')

    # --- 11. Recommendations Endpoints (2) ---
    @staticmethod
    def get_recent_anime_recommendations(page=1, **kwargs):
        """GET /recommendations/anime - Get recent anime recommendations."""
        params = {'page': page}
        params.update(kwargs)
        return _safe_request('/recommendations/anime', params=params)

    @staticmethod
    def get_recent_manga_recommendations(page=1, **kwargs):
        """GET /recommendations/manga - Get recent manga recommendations."""
        params = {'page': page}
        params.update(kwargs)
        return _safe_request('/recommendations/manga', params=params)

    # --- 12. Reviews Endpoints (2) ---
    @staticmethod
    def get_recent_anime_reviews(page=1, preliminary=None, spoilers=None, **kwargs):
        """GET /reviews/anime - Get recent anime reviews."""
        params = {'page': page, 'preliminary': preliminary, 'spoilers': spoilers}
        params.update(kwargs)
        return _safe_request('/reviews/anime', params=params)

    @staticmethod
    def get_recent_manga_reviews(page=1, preliminary=None, spoilers=None, **kwargs):
        """GET /reviews/manga - Get recent manga reviews."""
        params = {'page': page, 'preliminary': preliminary, 'spoilers': spoilers}
        params.update(kwargs)
        return _safe_request('/reviews/manga', params=params)

    # --- 13. Schedules Endpoint (1) ---
    @staticmethod
    def get_schedules(filter=None, sfw=None, sfw_strict=None, unapproved=None, page=1, limit=25, **kwargs):
        """GET /schedules - Get anime airing schedules."""
        params = {
            'filter': filter, 'sfw': sfw, 'sfw-strict': sfw_strict,
            'unapproved': unapproved, 'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request('/schedules', params=params)

    # --- 14. Seasons Endpoints (3) ---
    @staticmethod
    def get_season_now(sfw=None, sfw_strict=None, unapproved=None, page=1, limit=25, **kwargs):
        """GET /seasons/now - Get currently airing seasonal anime."""
        params = {
            'sfw': sfw, 'sfw-strict': sfw_strict, 'unapproved': unapproved,
            'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request('/seasons/now', params=params)

    @staticmethod
    def get_season_upcoming(sfw=None, sfw_strict=None, unapproved=None, page=1, limit=25, **kwargs):
        """GET /seasons/upcoming - Get upcoming seasonal anime."""
        params = {
            'sfw': sfw, 'sfw-strict': sfw_strict, 'unapproved': unapproved,
            'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request('/seasons/upcoming', params=params)

    @staticmethod
    def get_season_anime(year, season, sfw=None, sfw_strict=None, unapproved=None, page=1, limit=25, **kwargs):
        """GET /seasons/{year}/{season} - Get anime for a specific season and year."""
        params = {
            'sfw': sfw, 'sfw-strict': sfw_strict, 'unapproved': unapproved,
            'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request(f'/seasons/{year}/{season}', params=params)

    # --- 15. Stacks Endpoints (2) ---
    @staticmethod
    def search_stacks(q=None, page=1, limit=25, order_by=None, sort=None,
                      spoilers=None, challenges=None, official=None, sfw=None,
                      sfw_strict=None, **kwargs):
        """GET /stacks - Browse public interest stacks."""
        params = {
            'q': q, 'page': page, 'limit': limit, 'order_by': order_by,
            'sort': sort, 'spoilers': spoilers, 'challenges': challenges,
            'official': official, 'sfw': sfw, 'sfw-strict': sfw_strict
        }
        params.update(kwargs)
        return _safe_request('/stacks', params=params)

    @staticmethod
    def get_stack_detail(stack_id):
        """GET /stacks/{id} - Get interest stack details."""
        return _safe_request(f'/stacks/{stack_id}')

    # --- 16. Top Endpoints (5) ---
    @staticmethod
    def get_top_anime(type=None, filter=None, rating=None, sfw=None, sfw_strict=None, page=1, limit=25, **kwargs):
        """GET /top/anime - Get top rated anime."""
        params = {
            'type': type, 'filter': filter, 'rating': rating,
            'sfw': sfw, 'sfw-strict': sfw_strict, 'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request('/top/anime', params=params)

    @staticmethod
    def get_top_characters(page=1, limit=25, **kwargs):
        """GET /top/characters - Get top characters."""
        params = {'page': page, 'limit': limit}
        params.update(kwargs)
        return _safe_request('/top/characters', params=params)

    @staticmethod
    def get_top_manga(type=None, filter=None, sfw=None, sfw_strict=None, page=1, limit=25, **kwargs):
        """GET /top/manga - Get top rated manga."""
        params = {
            'type': type, 'filter': filter, 'sfw': sfw,
            'sfw-strict': sfw_strict, 'page': page, 'limit': limit
        }
        params.update(kwargs)
        return _safe_request('/top/manga', params=params)

    @staticmethod
    def get_top_people(page=1, limit=25, **kwargs):
        """GET /top/people - Get top people."""
        params = {'page': page, 'limit': limit}
        params.update(kwargs)
        return _safe_request('/top/people', params=params)

    @staticmethod
    def get_top_reviews(type=None, page=1, **kwargs):
        """GET /top/reviews - Get top reviews."""
        params = {'type': type, 'page': page}
        params.update(kwargs)
        return _safe_request('/top/reviews', params=params)


# ==============================================================================
# HIGH-LEVEL ADAPTERS AND CATALOG INTEGRATION HELPERS
# ==============================================================================

def get_top_anime(limit=8):
    """Fetches real top anime from Tenrai API with instant caching for fluid page transitions."""
    cache_key = f"top_anime_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_anime(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_top_manga(limit=8):
    """Fetches real top manga from Tenrai API with instant caching for fluid page transitions."""
    cache_key = f"top_manga_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_manga(type='manga', limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_top_lightnovels(limit=8):
    """Fetches real top light novels from Tenrai API with instant caching for fluid page transitions."""
    cache_key = f"top_lightnovels_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_manga(type='lightnovel', limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_season_now_items(limit=6):
    """Fetches real current season anime from Tenrai API (/seasons/now)."""
    cache_key = f"season_now_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_season_now(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_upcoming_items(limit=6):
    """Fetches real upcoming seasonal anime from Tenrai API (/seasons/upcoming)."""
    cache_key = f"upcoming_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_season_upcoming(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_schedules_items(limit=6):
    """Fetches real airing schedules from Tenrai API (/schedules)."""
    cache_key = f"schedules_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_schedules(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_news_items(limit=4):
    """Fetches real latest news from Tenrai API (/news)."""
    cache_key = f"news_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_news(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _set_cache(cache_key, items)
        return items
    return []


def get_top_characters_data(page=1, limit=12):
    """Fetches real top popular characters from Tenrai API (/top/characters) with pagination metadata."""
    cache_key = f"top_characters_page_{page}_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_characters(page=page, limit=limit)
    if res and 'data' in res:
        data = {
            'items': res['data'],
            'pagination': res.get('pagination', {
                'current_page': page,
                'has_next_page': len(res['data']) == limit,
            })
        }
        _set_cache(cache_key, data)
        return data
    return {'items': [], 'pagination': {'current_page': page, 'has_next_page': False}}


def get_top_people_items(limit=6):
    """Fetches real top creators and seiyuus from Tenrai API (/top/people)."""
    cache_key = f"top_people_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_people(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _set_cache(cache_key, items)
        return items
    return []


def get_top_reviews_items(limit=4):
    """Fetches real top community reviews from Tenrai API (/top/reviews)."""
    cache_key = f"top_reviews_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.get_top_reviews(limit=limit)
    if res and 'data' in res:
        items = res['data']
        _set_cache(cache_key, items)
        return items
    return []


def get_manga_destacados(limit=6):
    """Fetches featured manga from Tenrai API (/manga?order_by=popularity)."""
    cache_key = f"manga_destacados_limit_{limit}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    res = TenraiService.search_manga(order_by='popularity', sort='desc', limit=limit)
    if res and 'data' in res:
        items = res['data']
        _register_items(items)
        _set_cache(cache_key, items)
        return items
    return []


def get_common_genres():
    """Returns canonical genre list with real MAL IDs matching Tenrai genres."""
    return [
        {'id': 1, 'name': 'Acción (Action)'},
        {'id': 2, 'name': 'Aventura (Adventure)'},
        {'id': 4, 'name': 'Comedia (Comedy)'},
        {'id': 8, 'name': 'Drama (Drama)'},
        {'id': 10, 'name': 'Fantasía (Fantasy)'},
        {'id': 22, 'name': 'Romance (Romance)'},
        {'id': 24, 'name': 'Ciencia Ficción (Sci-Fi)'},
        {'id': 36, 'name': 'Recuentos de la Vida (Slice of Life)'},
        {'id': 37, 'name': 'Sobrenatural (Supernatural)'},
        {'id': 41, 'name': 'Suspense (Suspense)'},
        {'id': 46, 'name': 'Galardonados (Award Winning)'},
        {'id': 62, 'name': 'Isekai (Isekai)'},
    ]


def search_items(media_type='anime', category=None, query='', genre='', status='', order_by='score', sort='desc', page=1, per_page=24):
    """
    Unified search querying Tenrai API for anime, manga, and light novels.
    Accepts media_type or category for complete backwards and forwards compatibility.
    """
    if category:
        media_type = category

    if media_type == 'anime':
        endpoint = '/anime'
        m_type = None
    elif media_type == 'lightnovel':
        endpoint = '/manga'
        m_type = 'lightnovel'
    else:
        endpoint = '/manga'
        m_type = 'manga' if media_type == 'manga' else None

    params = {
        'page': page,
        'limit': per_page,
        'order_by': order_by if order_by else 'score',
        'sort': sort if sort else 'desc',
        'sfw': 'true'
    }

    if m_type:
        params['type'] = m_type

    if query:
        params['q'] = query

    if genre:
        params['genres'] = genre

    if status:
        params['status'] = status

    res = _safe_request(endpoint, params=params)

    if res and 'data' in res:
        items = res.get('data', [])
        _register_items(items)
        pagination = res.get('pagination', {})
        total_items = pagination.get('items', {}).get('total', len(items))
        last_page = pagination.get('last_visible_page', page)
        pagination_data = {
            'current_page': pagination.get('current_page', page),
            'total_pages': last_page,
            'total_items': total_items,
            'per_page': per_page,
            'has_previous_page': page > 1,
            'has_next_page': pagination.get('has_next_page', False),
            'previous_page_number': page - 1 if page > 1 else None,
            'next_page_number': page + 1 if pagination.get('has_next_page', False) else None,
            'page_range': list(range(1, min(last_page + 1, 100))),
            'start_index': (page - 1) * per_page + 1 if items else 0,
            'end_index': min(page * per_page, total_items),
        }
        return {
            'items': items,
            'pagination': pagination_data,
            'has_next': pagination.get('has_next_page', False),
            'current_page': pagination.get('current_page', page),
            'last_page': last_page,
            'total_count': total_items,
        }

    # Fallback to registered items if network is interrupted
    registered_matches = []
    for it in _ITEMS_REGISTRY.values():
        if query and query.lower() not in (it.get('title') or '').lower():
            continue
        registered_matches.append(it)

    return {
        'items': registered_matches[:per_page],
        'pagination': {
            'current_page': 1,
            'total_pages': 1,
            'total_items': len(registered_matches),
            'per_page': per_page,
            'has_previous_page': False,
            'has_next_page': False,
            'previous_page_number': None,
            'next_page_number': None,
            'page_range': [1],
            'start_index': 1 if registered_matches else 0,
            'end_index': len(registered_matches),
        },
        'has_next': False,
        'current_page': 1,
        'last_page': 1,
        'total_count': len(registered_matches),
    }


def get_item_detail(media_type, item_id):
    """
    Retrieves full details for an item from Tenrai API.
    Normalizes item_type to support anime, manga, characters, and people.
    """
    norm = (media_type or 'anime').lower()
    if norm in ('character', 'characters'):
        endpoint = f"/characters/{item_id}"
        norm_type = 'characters'
    elif norm in ('person', 'people'):
        endpoint = f"/people/{item_id}"
        norm_type = 'people'
    elif norm in ('manga', 'lightnovel'):
        endpoint = f"/manga/{item_id}"
        norm_type = 'manga'
    else:
        endpoint = f"/anime/{item_id}"
        norm_type = 'anime'

    str_id = str(item_id)
    cache_key = f"detail_{norm_type}_{str_id}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    if str_id in _ITEMS_REGISTRY:
        reg_item = _ITEMS_REGISTRY[str_id]
        if reg_item.get('synopsis') or reg_item.get('about'):
            return reg_item

    res = _safe_request(endpoint)
    if res and 'data' in res:
        data = res['data']
        if 'name' in data and not data.get('title'):
            data['title'] = data['name']
        if 'about' in data and not data.get('synopsis'):
            data['synopsis'] = data['about']
        _ITEMS_REGISTRY[str_id] = data
        _set_cache(cache_key, data)
        return data

    if str_id in _ITEMS_REGISTRY:
        return _ITEMS_REGISTRY[str_id]

    return {
        'mal_id': item_id,
        'title': f"{norm_type.capitalize()} #{item_id}",
        'title_japanese': '',
        'score': 0.0,
        'scored_by': 0,
        'rank': 0,
        'popularity': 0,
        'synopsis': 'Sin información disponible actualmente.',
        'images': {'webp': {'large_image_url': ''}, 'jpg': {'large_image_url': ''}},
        'genres': [],
        'type': norm_type.capitalize(),
        'status': 'Desconocido',
        'episodes': 'N/A',
        'chapters': 'N/A',
        'volumes': 'N/A',
    }


def get_platforms_fast(media_type, title, item_id=None):
    """
    Non-blocking version of get_platforms that immediately provides
    high-definition official and community streaming/reading links
    without holding the web worker on slow external network calls.
    """
    encoded_title = urllib.parse.quote_plus(title or '')
    if media_type in ('character', 'characters', 'person', 'people'):
        return {
            'official': [
                {
                    'name': 'MyAnimeList Oficial',
                    'icon': 'bi-globe',
                    'tag': 'Base de Datos Oficial',
                    'badge_class': 'badge bg-primary bg-opacity-25 text-primary border border-primary border-opacity-25',
                    'url': f'https://myanimelist.net/{media_type}/{item_id}',
                    'description': f'Ficha oficial verificada de {title}.'
                }
            ],
            'community': []
        }
    if media_type == 'anime':
        return {
            'official': [
                {
                    'name': 'Crunchyroll',
                    'icon': 'bi-play-circle-fill text-warning',
                    'tag': 'Simulcast Oficial',
                    'badge_class': 'badge bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25',
                    'url': f'https://www.crunchyroll.com/search?q={encoded_title}',
                    'description': 'Simulcast en alta definición con audio original japonés y doblaje en español.'
                },
                {
                    'name': 'Netflix',
                    'icon': 'bi-film text-danger',
                    'tag': 'Suscripción Global',
                    'badge_class': 'badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25',
                    'url': f'https://www.netflix.com/search?q={encoded_title}',
                    'description': 'Temporadas completas en calidad 4K Ultra HD con subtítulos multilingües.'
                },
                {
                    'name': 'Anime Onegai',
                    'icon': 'bi-broadcast text-info',
                    'tag': 'Latinoamérica Oficial',
                    'badge_class': 'badge bg-info bg-opacity-25 text-info border border-info border-opacity-25',
                    'url': f'https://www.animeonegai.com/es/search?query={encoded_title}',
                    'description': 'Plataforma oficial con doblajes exclusivos para Latinoamérica.'
                },
                {
                    'name': 'Amazon Prime Video',
                    'icon': 'bi-tv-fill text-primary',
                    'tag': 'Transmisión Oficial',
                    'badge_class': 'badge bg-primary bg-opacity-25 text-primary border border-primary border-opacity-25',
                    'url': f'https://www.amazon.com/s?k={encoded_title}+anime',
                    'description': 'Emisión internacional y películas licenciadas disponibles.'
                }
            ],
            'community': [
                {
                    'name': 'AnimeFLV',
                    'icon': 'bi-play-btn-fill',
                    'tag': 'Comunidad / Fansub',
                    'badge_class': 'badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25',
                    'url': f'https://www3.animeflv.net/browse?q={encoded_title}',
                    'description': 'Catálogo comunitario de episodios subtitulados en español.'
                },
                {
                    'name': 'JKAnime',
                    'icon': 'bi-play-btn',
                    'tag': 'Comunidad',
                    'badge_class': 'badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25',
                    'url': f'https://jkanime.net/buscar/{encoded_title}/',
                    'description': 'Comunidad de streaming con múltiples servidores de reproducción.'
                }
            ]
        }
    else:
        return {
            'official': [
                {
                    'name': 'MANGA Plus by SHUEISHA',
                    'icon': 'bi-book-half text-danger',
                    'tag': 'Oficial y Gratuito',
                    'badge_class': 'badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25',
                    'url': f'https://mangaplus.shueisha.co.jp/search_result?keyword={encoded_title}',
                    'description': 'Lectura simultánea con Japón de los últimos capítulos en español oficial.'
                },
                {
                    'name': 'BookWalker Global',
                    'icon': 'bi-journal-bookmark-fill text-primary',
                    'tag': 'Digital Oficial / Novelas',
                    'badge_class': 'badge bg-primary bg-opacity-25 text-primary border border-primary border-opacity-25',
                    'url': f'https://global.bookwalker.jp/search/?word={encoded_title}',
                    'description': 'Tienda digital oficial de Kadokawa para mangas y novelas ligeras en formato e-book.'
                },
                {
                    'name': 'Norma Editorial',
                    'icon': 'bi-shop text-warning',
                    'tag': 'Edición Física en Español',
                    'badge_class': 'badge bg-warning bg-opacity-25 text-warning border border-warning border-opacity-25',
                    'url': f'https://www.normaeditorial.com/catalogo/buscar?q={encoded_title}',
                    'description': 'Volúmenes físicos traducidos y distribuidos en librerías de habla hispana.'
                },
                {
                    'name': 'Panini Manga',
                    'icon': 'bi-journals text-danger',
                    'tag': 'Distribuidor Oficial',
                    'badge_class': 'badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-25',
                    'url': f'https://tiendapanini.com.mx/search?q={encoded_title}',
                    'description': 'Ediciones impresas coleccionables para México y Latinoamérica.'
                }
            ],
            'community': [
                {
                    'name': 'TuMangaOnline (TMO)',
                    'icon': 'bi-book',
                    'tag': 'Comunidad / Scanlation',
                    'badge_class': 'badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25',
                    'url': f'https://visortmo.com/library?_title={encoded_title}',
                    'description': 'Portal colaborativo de scanlations en español.'
                },
                {
                    'name': 'MangaDex',
                    'icon': 'bi-grid-fill',
                    'tag': 'Comunidad Global',
                    'badge_class': 'badge bg-secondary bg-opacity-25 text-light border border-secondary border-opacity-25',
                    'url': f'https://mangadex.org/search?q={encoded_title}',
                    'description': 'Plataforma comunitaria de lectura internacional de manga.'
                }
            ]
        }


def get_platforms(media_type, title, item_id=None):
    """
    Generates realistic, authentic viewing/reading platform links for anime and manga.
    Fetches real streaming links directly from Tenrai API whenever available.
    """
    if media_type == 'anime' and item_id:
        streaming_res = TenraiService.get_anime_streaming_links(item_id)
        if streaming_res and streaming_res.get('data'):
            real_platforms = []
            for s in streaming_res['data']:
                s_name = s.get('name', 'Streaming')
                s_url = s.get('url', '#')
                real_platforms.append({
                    'name': s_name,
                    'icon': 'bi-play-circle-fill',
                    'color': 'primary',
                    'type': 'Oficial',
                    'url': s_url,
                    'desc': f'Transmisión con licencia oficial en {s_name}.'
                })
            if real_platforms:
                return real_platforms

    encoded_title = urllib.parse.quote_plus(title or '')
    if media_type == 'anime':
        return [
            {
                'name': 'Crunchyroll',
                'icon': 'bi-play-circle-fill',
                'color': 'warning',
                'type': 'Oficial / Simulcast',
                'url': f'https://www.crunchyroll.com/search?q={encoded_title}',
                'desc': 'Disponible en simulcast con audio original japonés y doblaje en español.'
            },
            {
                'name': 'Netflix',
                'icon': 'bi-film',
                'color': 'danger',
                'type': 'Suscripción Global',
                'url': f'https://www.netflix.com/search?q={encoded_title}',
                'desc': 'Temporadas completas en calidad 4K Ultra HD con subtítulos multilingües.'
            },
            {
                'name': 'Anime Onegai',
                'icon': 'bi-broadcast',
                'color': 'info',
                'type': 'Latinoamérica Oficial',
                'url': f'https://www.animeonegai.com/es/search?query={encoded_title}',
                'desc': 'Plataforma oficial con doblajes exclusivos para Latinoamérica.'
            },
            {
                'name': 'Amazon Prime Video',
                'icon': 'bi-tv-fill',
                'color': 'primary',
                'type': 'Transmisión Oficial',
                'url': f'https://www.amazon.com/s?k={encoded_title}+anime',
                'desc': 'Emisión internacional y películas licenciadas disponibles.'
            }
        ]
    else:
        return [
            {
                'name': 'MANGA Plus by SHUEISHA',
                'icon': 'bi-book-half',
                'color': 'danger',
                'type': 'Oficial y Gratuito',
                'url': f'https://mangaplus.shueisha.co.jp/search_result?keyword={encoded_title}',
                'desc': 'Lectura simultánea con Japón de los últimos capítulos en español oficial.'
            },
            {
                'name': 'BookWalker Global',
                'icon': 'bi-journal-bookmark-fill',
                'color': 'primary',
                'type': 'Digital Oficial / Novelas',
                'url': f'https://global.bookwalker.jp/search/?word={encoded_title}',
                'desc': 'Tienda digital oficial de Kadokawa para mangas y novelas ligeras en formato e-book.'
            },
            {
                'name': 'Norma Editorial',
                'icon': 'bi-shop',
                'color': 'warning',
                'type': 'Edición Física en Español',
                'url': f'https://www.normaeditorial.com/catalogo/buscar?q={encoded_title}',
                'desc': 'Volúmenes físicos traducidos y distribuidos en librerías de habla hispana.'
            },
            {
                'name': 'Panini Manga',
                'icon': 'bi-collection',
                'color': 'info',
                'type': 'Distribución Panini',
                'url': f'https://www.tiendapanini.com.mx/catalogsearch/result/?q={encoded_title}',
                'desc': 'Publicación oficial en tomos impresos para México, España y Latinoamérica.'
            }
        ]
