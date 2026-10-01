import time
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.jikan.moe/v4"

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


def _safe_request(url, params=None, timeout=6):
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
        elif response.status_code == 429:
            logger.warning("Jikan API rate limit (429) hit. Returning empty or cached data.")
            return None
    except Exception as e:
        logger.error(f"Error connecting to Jikan API: {e}")
        return None
    return None


def get_top_anime(limit=12, filter_type=None):
    params = {'limit': limit}
    if filter_type:
        params['filter'] = filter_type
    data = _safe_request(f"{BASE_URL}/top/anime", params=params)
    if data and 'data' in data:
        return data['data']
    return _get_fallback_anime()


def get_top_manga(limit=12):
    params = {'limit': limit, 'type': 'manga'}
    data = _safe_request(f"{BASE_URL}/top/manga", params=params)
    if data and 'data' in data:
        return data['data']
    return _get_fallback_manga()


def get_top_lightnovels(limit=12):
    params = {'limit': limit, 'type': 'lightnovel'}
    data = _safe_request(f"{BASE_URL}/top/manga", params=params)
    if data and 'data' in data:
        return data['data']
    return _get_fallback_novels()


def search_items(category='anime', query='', genre='', status='', order_by='score', sort='desc', page=1):
    """
    Search mangas, animes or light novels with extensive filters:
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
        endpoint = f"{BASE_URL}/anime"
    elif category == 'lightnovel':
        endpoint = f"{BASE_URL}/manga"
        params['type'] = 'lightnovel'
    else:
        endpoint = f"{BASE_URL}/manga"
        params['type'] = 'manga'

    data = _safe_request(endpoint, params=params)
    if data and 'data' in data:
        return {
            'items': data.get('data', []),
            'pagination': data.get('pagination', {}),
        }

    # Fallback if API has connection issue
    if category == 'anime':
        items = _get_fallback_anime()
    elif category == 'lightnovel':
        items = _get_fallback_novels()
    else:
        items = _get_fallback_manga()

    if query:
        items = [i for i in items if query.lower() in i.get('title', '').lower()]

    return {
        'items': items,
        'pagination': {'has_next_page': False, 'current_page': 1, 'items': {'count': len(items)}}
    }


def get_item_detail(item_type, mal_id):
    endpoint = f"{BASE_URL}/anime/{mal_id}/full" if item_type == 'anime' else f"{BASE_URL}/manga/{mal_id}/full"
    data = _safe_request(endpoint)
    if data and 'data' in data:
        return data['data']

    # Fallback search
    if item_type == 'anime':
        all_items = _get_fallback_anime()
    else:
        all_items = _get_fallback_manga() + _get_fallback_novels()

    for it in all_items:
        if str(it.get('mal_id')) == str(mal_id):
            return it
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


# Safe fallbacks with high quality real metadata in case MAL/Jikan is unreachable or rate-limited
def _get_fallback_anime():
    return [
        {
            'mal_id': 5114,
            'title': 'Fullmetal Alchemist: Brotherhood',
            'title_japanese': '鋼の錬金術師 FULLMETAL ALCHEMIST',
            'score': 9.10,
            'type': 'TV',
            'episodes': 64,
            'status': 'Finished Airing',
            'synopsis': 'Después de un terrible accidente al intentar revivir a su madre mediante alquimia, Edward y Alphonse Elric emprenden un viaje para encontrar la legendaria Piedra Filosofal.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/1208/94745l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Aventura'}, {'name': 'Drama'}, {'name': 'Fantasía'}],
            'year': 2009,
        },
        {
            'mal_id': 16498,
            'title': 'Shingeki no Kyojin (Attack on Titan)',
            'title_japanese': '進撃の巨人',
            'score': 8.55,
            'type': 'TV',
            'episodes': 25,
            'status': 'Finished Airing',
            'synopsis': 'Hace siglos, la humanidad fue llevada casi a la extinción por monstruosas criaturas humanoides llamadas titanes, obligando a los supervivientes a resguardarse tras gigantescas murallas.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/10/47347l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Drama'}, {'name': 'Misterio'}],
            'year': 2013,
        },
        {
            'mal_id': 52991,
            'title': 'Sousou no Frieren (Frieren: Beyond Journey\'s End)',
            'title_japanese': '葬送のフリーレン',
            'score': 9.35,
            'type': 'TV',
            'episodes': 28,
            'status': 'Finished Airing',
            'synopsis': 'El Rey Demonio ha sido derrotado y el grupo victorioso de héroes se disuelve. Frieren, una maga elfa inmortal, emprende un viaje para comprender el valor de las conexiones humanas.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/1015/138006l.jpg'}},
            'genres': [{'name': 'Aventura'}, {'name': 'Drama'}, {'name': 'Fantasía'}],
            'year': 2023,
        },
        {
            'mal_id': 38000,
            'title': 'Kimetsu no Yaiba (Demon Slayer)',
            'title_japanese': '鬼滅の刃',
            'score': 8.50,
            'type': 'TV',
            'episodes': 26,
            'status': 'Finished Airing',
            'synopsis': 'Tanjiro Kamado emprende un peligroso camino para convertirse en cazador de demonios y devolverle la humanidad a su hermana Nezuko, convertida en demonio.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/1286/99889l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Fantasía'}, {'name': 'Sobrenatural'}],
            'year': 2019,
        },
        {
            'mal_id': 40748,
            'title': 'Jujutsu Kaisen',
            'title_japanese': '呪術廻戦',
            'score': 8.60,
            'type': 'TV',
            'episodes': 24,
            'status': 'Finished Airing',
            'synopsis': 'Yuji Itadori traga un dedo maldito perteneciente a Ryomen Sukuna para salvar a sus amigos, convirtiéndose en el recipiente del Rey de las Maldiciones.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/1171/109222l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Fantasía'}, {'name': 'Sobrenatural'}],
            'year': 2020,
        },
        {
            'mal_id': 30276,
            'title': 'One Punch Man',
            'title_japanese': 'ワンパンマン',
            'score': 8.51,
            'type': 'TV',
            'episodes': 12,
            'status': 'Finished Airing',
            'synopsis': 'Saitama es un superhéroe que derrota a cualquier enemigo de un solo golpe, buscando desesperadamente un rival que le devuelva la emoción del combate.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/12/76049l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Comedia'}, {'name': 'Ciencia Ficción'}],
            'year': 2015,
        }
    ]


def _get_fallback_manga():
    return [
        {
            'mal_id': 2,
            'title': 'Berserk',
            'title_japanese': 'ベルセルク',
            'score': 9.47,
            'type': 'Manga',
            'chapters': 380,
            'status': 'Publishing',
            'synopsis': 'Guts, conocido como el Espadachín Negro, busca venganza contra su antiguo amigo y comandante Griffith, quien sacrificó a sus camaradas por poder divino.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/157897l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Aventura'}, {'name': 'Fantasía Oscura'}],
            'year': 1989,
        },
        {
            'mal_id': 13,
            'title': 'One Piece',
            'title_japanese': 'ONE PIECE',
            'score': 9.22,
            'type': 'Manga',
            'chapters': 1120,
            'status': 'Publishing',
            'synopsis': 'Monkey D. Luffy y su tripulación de Sombreros de Paja navegan los mares en busca del legendario tesoro One Piece para convertirse en el Rey de los Piratas.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/253146l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Aventura'}, {'name': 'Fantasía'}],
            'year': 1997,
        },
        {
            'mal_id': 656,
            'title': 'Vagabond',
            'title_japanese': 'バガボンド',
            'score': 9.25,
            'type': 'Manga',
            'chapters': 327,
            'status': 'On Hiatus',
            'synopsis': 'La épica historia del legendario espadachín japonés Miyamoto Musashi en su camino hacia el autodescubrimiento y la iluminación a través de la espada.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/259087l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Aventura'}, {'name': 'Histórico'}],
            'year': 1998,
        },
        {
            'mal_id': 70345,
            'title': 'Tokyo Ghoul',
            'title_japanese': '東京喰種トーキョーグール',
            'score': 8.53,
            'type': 'Manga',
            'chapters': 144,
            'status': 'Finished',
            'synopsis': 'Ken Kaneki, un tímido estudiante universitario, se ve transformado en mitad ghoul tras sobrevivir a un encuentro mortal en Tokio.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/3/85055l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Drama'}, {'name': 'Horror'}],
            'year': 2011,
        }
    ]


def _get_fallback_novels():
    return [
        {
            'mal_id': 89337,
            'title': 'Solo Leveling (Only I Level Up)',
            'title_japanese': '나 혼자만 레벨업',
            'score': 8.65,
            'type': 'Light Novel',
            'chapters': 270,
            'status': 'Finished',
            'synopsis': 'Sung Jin-Woo, el cazador más débil de la humanidad, despierta con una misteriosa interfaz de jugador que le permite subir de nivel ilimitadamente.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/3/222295l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Aventura'}, {'name': 'Fantasía'}],
            'year': 2016,
        },
        {
            'mal_id': 58149,
            'title': 'Mushoku Tensei: Isekai Ittara Honki Dasu',
            'title_japanese': '無職転生 ～異世界行ったら本気だす～',
            'score': 8.82,
            'type': 'Light Novel',
            'chapters': 260,
            'status': 'Finished',
            'synopsis': 'Un hombre desempleado de 34 años reencarna como Rudeus Greyrat en un mundo de espadas y magia, decidiendo vivir esta nueva vida sin arrepentimientos.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/3/178553l.jpg'}},
            'genres': [{'name': 'Drama'}, {'name': 'Fantasía'}, {'name': 'Isekai'}],
            'year': 2014,
        },
        {
            'mal_id': 70461,
            'title': 'Overlord',
            'title_japanese': 'オーバーロード',
            'score': 8.70,
            'type': 'Light Novel',
            'chapters': 160,
            'status': 'Publishing',
            'synopsis': 'Momonga se queda conectado al videojuego Yggdrasil hasta el cierre de sus servidores, solo para descubrir que ha sido transportado al juego con su gremio.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/3/161407l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Fantasía'}, {'name': 'Isekai'}],
            'year': 2012,
        },
        {
            'mal_id': 85737,
            'title': 'Re:Zero kara Hajimeru Isekai Seikatsu',
            'title_japanese': 'Re:ゼロから始める異世界生活',
            'score': 8.64,
            'type': 'Light Novel',
            'chapters': 350,
            'status': 'Publishing',
            'synopsis': 'Subaru Natsuki es invocado a otro mundo y descubre que posee el aterrador poder de "Regreso por la Muerte", rebobinando el tiempo cada vez que muere.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/179269l.jpg'}},
            'genres': [{'name': 'Drama'}, {'name': 'Fantasía'}, {'name': 'Isekai'}, {'name': 'Psicológico'}],
            'year': 2014,
        },
        {
            'mal_id': 114798,
            'title': 'Omniscient Reader\'s Viewpoint',
            'title_japanese': '전지적 독자 시점',
            'score': 8.95,
            'type': 'Light Novel',
            'chapters': 551,
            'status': 'Finished',
            'synopsis': 'Kim Dokja es el único lector de una novela web olvidada. Cuando la historia se convierte en la sangrienta realidad, él es el único que sabe cómo terminará el mundo.',
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/240763l.jpg'}},
            'genres': [{'name': 'Acción'}, {'name': 'Fantasía'}, {'name': 'Sobrenatural'}],
            'year': 2018,
        }
    ]
