import os
import time
import urllib.parse
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Request Headers matching realistic anime community client
HEADERS = {
    'User-Agent': 'GrowUp-App/1.0 (+https://growup-7my7.onrender.com; contact: growup.anime@gmail.com)',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

# Shared HTTP session with connection pooling for extreme fluidity
_SESSION = requests.Session()
_SESSION.headers.update(HEADERS)

# Fast in-memory cache for instant page navigation
_CACHE = {}
_ITEMS_REGISTRY = {}
CACHE_TTL = 3600  # 1 hour cache for ultra-fluid page loads

DISK_CACHE_FILE = os.path.join(os.path.dirname(__file__), 'jikan_disk_cache.json')


def get_base_url():
    url = getattr(settings, 'JIKAN_API_BASE_URL', None) or os.getenv('JIKAN_API_BASE_URL', '')
    if not url:
        url = 'https://api.jikan.moe/v4'
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
    if not items:
        return
    for it in items:
        if isinstance(it, dict) and it.get('mal_id'):
            _ITEMS_REGISTRY[str(it['mal_id'])] = it


def _load_disk_cache():
    import json
    if os.path.exists(DISK_CACHE_FILE):
        try:
            with open(DISK_CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, list):
                            _set_cache(k, v)
                            _register_items(v)
        except Exception as e:
            logger.warning(f"Could not load jikan_disk_cache.json: {e}")


def _save_disk_cache(key, items):
    import json
    try:
        current = {}
        if os.path.exists(DISK_CACHE_FILE):
            try:
                with open(DISK_CACHE_FILE, 'r', encoding='utf-8') as f:
                    current = json.load(f)
            except Exception:
                current = {}
        current[key] = items
        with open(DISK_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"Could not save jikan_disk_cache.json: {e}")


# Initialize disk cache on startup
_load_disk_cache()


def _safe_request(endpoint_path, params=None, timeout=8, retries=1):
    base_url = get_base_url()
    if not base_url:
        return None

    url = f"{base_url}{endpoint_path}"
    cache_key = f"{url}?{sorted(params.items()) if params else ''}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached

    for attempt in range(retries + 1):
        try:
            response = _SESSION.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                _set_cache(cache_key, data)
                return data
            elif response.status_code in (429, 504, 502, 503) and attempt < retries:
                logger.warning(f"Jikan API status {response.status_code} on {url}, retrying in 1s (attempt {attempt + 1}/{retries})...")
                time.sleep(1.0)
                continue
            elif response.status_code == 429:
                logger.warning(f"Jikan API rate limit (429) on {url}")
                return None
            elif response.status_code in (504, 502, 503):
                logger.warning(f"Jikan API gateway status {response.status_code} on {url}")
                return None
            elif response.status_code == 404:
                return None
            else:
                logger.warning(f"Jikan API responded with status {response.status_code} for {url}")
                return None
        except Exception as e:
            if attempt < retries:
                logger.warning(f"Jikan API issue on {url}: {e}, retrying...")
                time.sleep(1.0)
                continue
            logger.warning(f"Jikan API connection issue on {url}: {e}")
            return None
    return None


def get_top_anime(limit=8):
    """Fetches real top anime from Jikan with instant caching for fluid page transitions."""
    cached = _get_cache('real_top_anime_list')
    if cached is not None:
        return cached[:limit]

    data = _safe_request('/top/anime', params={'limit': 24, 'sfw': 'true'})
    if data and isinstance(data, dict) and data.get('data'):
        items = data['data']
        _register_items(items)
        _set_cache('real_top_anime_list', items)
        _save_disk_cache('real_top_anime_list', items)
        return items[:limit]

    # If API call returned None, return any previously registered anime
    registered = [it for it in _ITEMS_REGISTRY.values() if it.get('type') in ('TV', 'Movie', 'OVA', 'Special')]
    return registered[:limit]


def get_top_manga(limit=8):
    """Fetches real top manga from Jikan with instant caching for fluid page transitions."""
    cached = _get_cache('real_top_manga_list')
    if cached is not None:
        return cached[:limit]

    data = _safe_request('/top/manga', params={'type': 'manga', 'limit': 24, 'sfw': 'true'})
    if data and isinstance(data, dict) and data.get('data'):
        items = data['data']
        _register_items(items)
        _set_cache('real_top_manga_list', items)
        _save_disk_cache('real_top_manga_list', items)
        return items[:limit]

    registered = [it for it in _ITEMS_REGISTRY.values() if it.get('type') in ('Manga', 'Manhwa', 'Manhua', 'One-shot')]
    return registered[:limit]


def get_top_lightnovels(limit=8):
    """Fetches real top light novels from Jikan with instant caching for fluid page transitions."""
    cached = _get_cache('real_top_ln_list')
    if cached is not None:
        return cached[:limit]

    data = _safe_request('/top/manga', params={'type': 'lightnovel', 'limit': 24, 'sfw': 'true'})
    if data and isinstance(data, dict) and data.get('data'):
        items = data['data']
        _register_items(items)
        _set_cache('real_top_ln_list', items)
        _save_disk_cache('real_top_ln_list', items)
        return items[:limit]

    registered = [it for it in _ITEMS_REGISTRY.values() if it.get('type') in ('Novel', 'Lightnovel', 'Light Novel')]
    return registered[:limit]


def get_all_anime_pool():
    cached = _get_cache('real_top_anime_list')
    if cached is not None:
        return cached
    return get_top_anime(limit=24)


def get_all_manga_and_novels_pool():
    mangas = get_top_manga(limit=24)
    lns = get_top_lightnovels(limit=24)
    return mangas + lns


def search_items(category='anime', query='', genre='', status='', order_by='score', sort='desc', page=1, per_page=24):
    """
    Search mangas, animes or light novels with real-time filters and 24-record pagination.
    """
    if category == 'anime':
        pool = list(get_all_anime_pool())
    elif category == 'lightnovel':
        all_mn = get_all_manga_and_novels_pool()
        pool = [it for it in all_mn if it.get('type') in ('Novel', 'Lightnovel', 'Light Novel')]
    else:
        all_mn = get_all_manga_and_novels_pool()
        pool = [it for it in all_mn if it.get('type') in ('Manga', 'Manhwa', 'Manhua', 'One-shot', None, '')]

    # Filter by text query
    if query:
        q_lower = query.lower()
        pool = [
            it for it in pool
            if q_lower in str(it.get('title', '')).lower() or q_lower in str(it.get('title_japanese', '')).lower()
        ]

    # Filter by genre
    if genre:
        pool = [
            it for it in pool
            if any(str(g.get('mal_id')) == str(genre) for g in it.get('genres', []))
        ]

    # Filter by status
    if status:
        status_lower = status.lower()
        pool = [
            it for it in pool
            if status_lower in str(it.get('status', '')).lower()
        ]

    # Sorting
    if order_by == 'title':
        pool.sort(key=lambda x: str(x.get('title', '')).lower(), reverse=(sort == 'desc'))
    elif order_by == 'popularity':
        pool.sort(key=lambda x: x.get('members') or x.get('popularity') or 0, reverse=(sort == 'desc'))
    else:  # default 'score'
        pool.sort(key=lambda x: float(x.get('score') or 0), reverse=(sort != 'asc'))

    # Pagination calculation (24 records per page)
    total_items = len(pool)
    total_pages = max(1, (total_items + per_page - 1) // per_page)
    current_page = max(1, min(page, total_pages)) if total_items > 0 else 1

    start = (current_page - 1) * per_page
    end = start + per_page
    page_items = pool[start:end]

    pagination = {
        'current_page': current_page,
        'total_pages': total_pages,
        'total_items': total_items,
        'per_page': per_page,
        'has_previous_page': current_page > 1,
        'has_next_page': current_page < total_pages,
        'previous_page_number': current_page - 1 if current_page > 1 else None,
        'next_page_number': current_page + 1 if current_page < total_pages else None,
        'page_range': list(range(1, total_pages + 1)),
        'start_index': start + 1 if total_items > 0 else 0,
        'end_index': min(end, total_items),
    }

    return {
        'items': page_items,
        'pagination': pagination,
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


def get_platforms(item_type, title, mal_id=None):
    """
    Returns official and community streaming/reading platform links for an anime, manga or light novel.
    """
    title_enc = urllib.parse.quote(str(title).strip())
    platforms = {
        'official': [],
        'community': []
    }

    if item_type == 'anime':
        platforms['official'] = [
            {
                'name': 'Crunchyroll',
                'url': f'https://www.crunchyroll.com/es/search?q={title_enc}',
                'icon': 'bi-play-circle-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Simulcast oficial con doblaje y subtitulos'
            },
            {
                'name': 'Netflix',
                'url': f'https://www.netflix.com/search?q={title_enc}',
                'icon': 'bi-film',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Catalogo global en alta definicion'
            },
            {
                'name': 'Prime Video',
                'url': f'https://www.primevideo.com/search/ref=atv_nb_sr?phrase={title_enc}',
                'icon': 'bi-play-btn-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Transmision oficial de Amazon Studios'
            },
            {
                'name': 'Anime Onegai',
                'url': f'https://www.animeonegai.com/es/search?q={title_enc}',
                'icon': 'bi-tv-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Doblaje y transmision para Latinoamerica'
            },
            {
                'name': 'HIDIVE',
                'url': f'https://www.hidive.com/search?q={title_enc}',
                'icon': 'bi-camera-reels-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Emisiones exclusivas de Sentai Filmworks'
            }
        ]
        platforms['community'] = [
            {
                'name': 'AnimeFLV',
                'url': f'https://www3.animeflv.net/browse?q={title_enc}',
                'icon': 'bi-broadcast',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Portal alternativo de transmision en espanol'
            },
            {
                'name': 'JKAnime',
                'url': f'https://jkanime.net/buscar/{title_enc}/',
                'icon': 'bi-collection-play-fill',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Servidor veloz de episodios online'
            },
            {
                'name': 'AnimeID',
                'url': f'https://www.animeid.tv/buscar?q={title_enc}',
                'icon': 'bi-display-fill',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Directorio comunitario de series en emision'
            },
            {
                'name': 'MonosChinos',
                'url': f'https://monoschinos2.com/buscar?q={title_enc}',
                'icon': 'bi-play-circle',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Streaming alternativo con multiples reproductores'
            }
        ]
    elif item_type == 'manga':
        platforms['official'] = [
            {
                'name': 'MANGA Plus (Shueisha)',
                'url': f'https://mangaplus.shueisha.co.jp/search_result?keyword={title_enc}',
                'icon': 'bi-book-half',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Lanzamiento oficial y simultaneo de Shonen Jump'
            },
            {
                'name': 'VIZ Media',
                'url': f'https://www.viz.com/search?search={title_enc}',
                'icon': 'bi-journal-bookmark-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Editor y distribuidor oficial de manga en occidente'
            },
            {
                'name': 'Comick',
                'url': f'https://comick.io/search?q={title_enc}',
                'icon': 'bi-book',
                'tag': 'Oficial / Lector',
                'badge_class': 'platform-tag-official',
                'description': 'Lector moderno de obras oficiales y scanlations'
            }
        ]
        platforms['community'] = [
            {
                'name': 'TuMangaOnline (TMO)',
                'url': f'https://visortmo.com/library?_pg=1&title={title_enc}',
                'icon': 'bi-eyeglasses',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'La mayor plataforma comunitaria de lectura en espanol'
            },
            {
                'name': 'MangaDex',
                'url': f'https://mangadex.org/search?q={title_enc}',
                'icon': 'bi-collection-fill',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Repositorio global y colaborativo de scanlations'
            },
            {
                'name': 'InManga',
                'url': f'https://inmanga.com/search?query={title_enc}',
                'icon': 'bi-journal-richtext',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Lector alternativo rapido sin recarga de pagina'
            },
            {
                'name': 'Lectormanga',
                'url': f'https://lectormanga.com/library?_pg=1&title={title_enc}',
                'icon': 'bi-book-fill',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Comunidad de fansub y traduccion de mangas'
            }
        ]
    else:  # lightnovel
        platforms['official'] = [
            {
                'name': 'BookWalker Global',
                'url': f'https://global.bookwalker.jp/search/?word={title_enc}',
                'icon': 'bi-journal-text',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Tienda y visor digital oficial de Kadokawa'
            },
            {
                'name': 'Yen Press',
                'url': f'https://yenpress.com/search-list/?q={title_enc}',
                'icon': 'bi-bookmark-star-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Editorial lider en novelas ligeras en occidente'
            },
            {
                'name': 'J-Novel Club',
                'url': f'https://j-novel.club/series?search={title_enc}',
                'icon': 'bi-journal-check',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Publicacion digital capitulo a capitulo directa de Japon'
            },
            {
                'name': 'Amazon Kindle',
                'url': f'https://www.amazon.com/s?k={title_enc}+light+novel',
                'icon': 'bi-cart-fill',
                'tag': 'Oficial',
                'badge_class': 'platform-tag-official',
                'description': 'Ediciones digitales certificadas en Kindle Store'
            }
        ]
        platforms['community'] = [
            {
                'name': 'NovelUpdates',
                'url': f'https://www.novelupdates.com/?s={title_enc}',
                'icon': 'bi-translate',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Directorio internacional de traducciones de novelas'
            },
            {
                'name': 'TuNovelaLigera',
                'url': f'https://tunovelaligera.com/?s={title_enc}',
                'icon': 'bi-journal-code',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Comunidad de traduccion de novelas ligeras al espanol'
            },
            {
                'name': 'Skythewood',
                'url': f'https://skythewood.blogspot.com/search?q={title_enc}',
                'icon': 'bi-feather',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Traducciones comunitarias y notas de autor'
            },
            {
                'name': 'Einherjar Project',
                'url': f'https://einherjarproject.net/?s={title_enc}',
                'icon': 'bi-book-half',
                'tag': 'Comunidad',
                'badge_class': 'platform-tag-community',
                'description': 'Grupo hispano de lectura y localizacion de novelas'
            }
        ]

    return platforms
