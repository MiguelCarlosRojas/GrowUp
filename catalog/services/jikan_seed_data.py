"""
Curated fallback seed data from Jikan API v4.
Provides zero-downtime resilience when Jikan API encounters 504 Gateway Timeouts,
Cloudflare rate limiting, or network latency during cloud deployments.
"""

SEED_ANIMES = [
    {
        'mal_id': 52991,
        'title': "Sousou no Frieren (Frieren: Beyond Journey's End)",
        'title_english': "Frieren: Beyond Journey's End",
        'title_japanese': "葬送のフリーレン",
        'type': 'TV',
        'episodes': 28,
        'status': 'Finished Airing',
        'score': 9.38,
        'scored_by': 450000,
        'rank': 1,
        'popularity': 120,
        'members': 950000,
        'synopsis': "El rey demonio ha sido derrotado y el grupo de héroes victorioso regresa a casa antes de disolverse. Los cuatro (la maga Frieren, el héroe Himmel, el sacerdote Heiter y el guerrero Eisen) recuerdan su viaje de una década mientras llega el momento de despedirse. Pero el paso del tiempo es diferente para los elfos, por lo que Frieren es testigo de cómo sus compañeros van falleciendo lentamente. Antes de su muerte, Heiter logra encargarle a Frieren una joven aprendiz humana llamada Fern. Impulsadas por la pasión del elfo por recolectar una infinidad de hechizos mágicos, la pareja se embarca en un viaje aparentemente sin rumbo, revisitando los lugares que los héroes habían visitado alguna vez. A lo largo de sus viajes, Frieren confronta lentamente su arrepentimiento por las oportunidades perdidas de forjar vínculos más profundos con sus camaradas ahora fallecidos.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1015/138075.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1015/138075l.jpg'
            }
        },
        'genres': [
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 10, 'name': 'Fantasía'}
        ],
        'aired': {'string': 'Sep 29, 2023 to Mar 22, 2024'},
        'duration': '24 min per ep',
        'rating': 'PG-13 - Teens 13 or older'
    },
    {
        'mal_id': 5114,
        'title': 'Fullmetal Alchemist: Brotherhood',
        'title_english': 'Fullmetal Alchemist: Brotherhood',
        'title_japanese': '鋼の錬金術師 FULLMETAL ALCHEMIST',
        'type': 'TV',
        'episodes': 64,
        'status': 'Finished Airing',
        'score': 9.10,
        'scored_by': 2100000,
        'rank': 2,
        'popularity': 3,
        'members': 3300000,
        'synopsis': "Para que algo se obtenga, algo de igual valor debe perderse. La alquimia está unida por esta Ley del Intercambio Equivalente, algo que los jóvenes hermanos Edward y Alphonse Elric descubren después de intentar la transmutación humana: el único acto prohibido de la alquimia. En un intento desesperado por resucitar a su difunta madre, Edward pierde su pierna izquierda y Alphonse su cuerpo físico completo. A costa de su brazo derecho, Edward sella el alma de Alphonse en una armadura. Tres años más tarde, Edward busca la legendaria Piedra Filosofal.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1208/94745.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1208/94745l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 10, 'name': 'Fantasía'}
        ],
        'aired': {'string': 'Apr 5, 2009 to Jul 4, 2010'},
        'duration': '24 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    },
    {
        'mal_id': 9253,
        'title': 'Steins;Gate',
        'title_english': 'Steins;Gate',
        'title_japanese': 'STEINS;GATE',
        'type': 'TV',
        'episodes': 24,
        'status': 'Finished Airing',
        'score': 9.07,
        'scored_by': 1400000,
        'rank': 3,
        'popularity': 13,
        'members': 2500000,
        'synopsis': "Rintarou Okabe es un científico loco autoproclamado que alquila una habitación en Akihabara para inventar artilugios del futuro con sus amigos Mayuri Shiina e Itaru Hashida. A pesar de sus pretensiones, su invento más notable es un microondas capaz de enviar mensajes de texto al pasado, alterando el flujo del tiempo y las líneas temporales del mundo.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1935/127974.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1935/127974l.jpg'
            }
        },
        'genres': [
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 24, 'name': 'Ciencia Ficción'},
            {'mal_id': 41, 'name': 'Suspense'}
        ],
        'aired': {'string': 'Apr 6, 2011 to Sep 14, 2011'},
        'duration': '24 min per ep',
        'rating': 'PG-13 - Teens 13 or older'
    },
    {
        'mal_id': 16498,
        'title': 'Shingeki no Kyojin (Attack on Titan)',
        'title_english': 'Attack on Titan',
        'title_japanese': '進撃の巨人',
        'type': 'TV',
        'episodes': 25,
        'status': 'Finished Airing',
        'score': 8.55,
        'scored_by': 2800000,
        'rank': 105,
        'popularity': 1,
        'members': 3900000,
        'synopsis': "Durante siglos, la humanidad ha sido cazada por gigantescas criaturas humanoides conocidas como titanes. Forzados a refugiarse tras inmensos muros concéntricos, la paz se rompe cuando un titán colosal destruye la defensa exterior, impulsando a Eren Yeager a jurar erradicar a todos los titanes de la faz de la tierra.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/10/47347.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/10/47347l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 14, 'name': 'Horror'},
            {'mal_id': 41, 'name': 'Suspense'}
        ],
        'aired': {'string': 'Apr 7, 2013 to Sep 29, 2013'},
        'duration': '24 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    },
    {
        'mal_id': 38000,
        'title': 'Kimetsu no Yaiba (Demon Slayer)',
        'title_english': 'Demon Slayer: Kimetsu no Yaiba',
        'title_japanese': '鬼滅の刃',
        'type': 'TV',
        'episodes': 26,
        'status': 'Finished Airing',
        'score': 8.48,
        'scored_by': 2200000,
        'rank': 130,
        'popularity': 5,
        'members': 3100000,
        'synopsis': "Tanjirou Kamado es un muchacho de buen corazón que vive con su familia en las montañas y se gana la vida vendiendo carbón. Todo cambia cuando su familia es masacrada por demonios y su hermana Nezuko es la única superviviente, transformada en un demonio. Tanjirou emprende un duro camino como cazador de demonios para devolver a su hermana a la humanidad.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1286/99889.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1286/99889l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 37, 'name': 'Sobrenatural'}
        ],
        'aired': {'string': 'Apr 6, 2019 to Sep 28, 2019'},
        'duration': '23 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    },
    {
        'mal_id': 40748,
        'title': 'Jujutsu Kaisen',
        'title_english': 'Jujutsu Kaisen',
        'title_japanese': '呪術廻戦',
        'type': 'TV',
        'episodes': 24,
        'status': 'Finished Airing',
        'score': 8.60,
        'scored_by': 1700000,
        'rank': 75,
        'popularity': 9,
        'members': 2800000,
        'synopsis': "Yuuji Itadori es un estudiante de secundaria con un talento atlético descomunal que, para salvar a sus amigos de una maldición voraz, ingiere el dedo del Rey de las Maldiciones, Ryomen Sukuna, ingresando de lleno en el peligroso mundo de la hechicería jujutsu.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1171/109222.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1171/109222l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 37, 'name': 'Sobrenatural'}
        ],
        'aired': {'string': 'Oct 3, 2020 to Mar 27, 2021'},
        'duration': '23 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    },
    {
        'mal_id': 52299,
        'title': 'Ore dake Level Up na Ken (Solo Leveling)',
        'title_english': 'Solo Leveling',
        'title_japanese': '俺だけレベルアップな件',
        'type': 'TV',
        'episodes': 12,
        'status': 'Finished Airing',
        'score': 8.35,
        'scored_by': 500000,
        'rank': 210,
        'popularity': 45,
        'members': 1200000,
        'synopsis': "En un mundo donde portales conectan la Tierra con mazmorras plagadas de monstruos, los cazadores despiertan habilidades sobrehumanas. Sung Jinwoo, conocido como el cazador más débil de la humanidad, recibe una misión misteriosa de un 'Sistema' que le permite subir de nivel sin límites.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1487/141042.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1487/141042l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 10, 'name': 'Fantasía'}
        ],
        'aired': {'string': 'Jan 7, 2024 to Mar 31, 2024'},
        'duration': '23 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    },
    {
        'mal_id': 41467,
        'title': 'Bleach: Sennen Kessen-hen (Thousand-Year Blood War)',
        'title_english': 'Bleach: Thousand-Year Blood War',
        'title_japanese': 'BLEACH 千年血戦篇',
        'type': 'TV',
        'episodes': 13,
        'status': 'Finished Airing',
        'score': 9.03,
        'scored_by': 280000,
        'rank': 8,
        'popularity': 320,
        'members': 580000,
        'synopsis': "La Sociedad de Almas es invadida repentinamente por el Wandenreich, un imperio secreto del ejército Quincy liderado por Yhwach. Ichigo Kurosaki vuelve a empuñar su Zanpakutou para defender el balance de los mundos en una batalla definitiva.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/anime/1764/126627.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/anime/1764/126627l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 37, 'name': 'Sobrenatural'}
        ],
        'aired': {'string': 'Oct 11, 2022 to Dec 27, 2022'},
        'duration': '24 min per ep',
        'rating': 'R - 17+ (violence & profanity)'
    }
]

SEED_MANGAS = [
    {
        'mal_id': 2,
        'title': 'Berserk',
        'title_english': 'Berserk',
        'title_japanese': 'ベルセルク',
        'type': 'Manga',
        'chapters': 380,
        'volumes': 42,
        'status': 'Publishing',
        'score': 9.47,
        'scored_by': 360000,
        'rank': 1,
        'popularity': 1,
        'members': 700000,
        'synopsis': "Guts, conocido como el Espadachín Negro, busca refugio de las fuerzas demoníacas atraídas por la marca en su cuello y venganza contra el hombre al que una vez consideró un amigo y que le arrebató todo lo que amaba. Armado con la colosal espada Matadragones y un brazo mecánico, viaja por un mundo despiadado de fantasía oscura.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/1/157897.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/157897l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 14, 'name': 'Horror'}
        ],
        'authors': [{'name': 'Miura, Kentarou'}]
    },
    {
        'mal_id': 13,
        'title': 'One Piece',
        'title_english': 'One Piece',
        'title_japanese': 'ONE PIECE',
        'type': 'Manga',
        'chapters': 1120,
        'volumes': 109,
        'status': 'Publishing',
        'score': 9.22,
        'scored_by': 400000,
        'rank': 3,
        'popularity': 2,
        'members': 650000,
        'synopsis': "Gol D. Roger, el Rey de los Piratas, reveló antes de su ejecución que su mayor tesoro, el One Piece, espera en algún lugar de la Grand Line. Décadas más tarde, Monkey D. Luffy zarpa junto a su tripulación de los Piratas de Sombrero de Paja en busca de la libertad y el legendario tesoro.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/2/253146.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/253146l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 10, 'name': 'Fantasía'}
        ],
        'authors': [{'name': 'Oda, Eiichiro'}]
    },
    {
        'mal_id': 656,
        'title': 'Vagabond',
        'title_english': 'Vagabond',
        'title_japanese': 'バガボンド',
        'type': 'Manga',
        'chapters': 327,
        'volumes': 37,
        'status': 'On Hiatus',
        'score': 9.35,
        'scored_by': 175000,
        'rank': 2,
        'popularity': 6,
        'members': 420000,
        'synopsis': "En el Japón del siglo XVI, Shinmen Takezou es un joven impulsivo y violento temido por su aldea. Tras sobrevivir a la sangrienta batalla de Sekigahara, renace con el nombre de Miyamoto Musashi e inicia una senda de iluminación espiritual y dominio incomparable de la espada.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/1/259070.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/259070l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 13, 'name': 'Histórico'}
        ],
        'authors': [{'name': 'Inoue, Takehiko'}]
    },
    {
        'mal_id': 1,
        'title': 'Monster',
        'title_english': 'Monster',
        'title_japanese': 'MONSTER',
        'type': 'Manga',
        'chapters': 162,
        'volumes': 18,
        'status': 'Finished',
        'score': 9.15,
        'scored_by': 100000,
        'rank': 5,
        'popularity': 12,
        'members': 280000,
        'synopsis': "Kenzou Tenma es un brillante neurocirujano japonés radicado en Alemania que decide operar a un niño huérfano con una herida de bala en vez de salvar al alcalde de la ciudad. Años después descubre que aquel niño al que le devolvió la vida se ha convertido en un frío asesino sociópata.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/3/258224.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/3/258224l.jpg'
            }
        },
        'genres': [
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 7, 'name': 'Misterio'},
            {'mal_id': 41, 'name': 'Suspense'}
        ],
        'authors': [{'name': 'Urasawa, Naoki'}]
    }
]

SEED_LIGHTNOVELS = [
    {
        'mal_id': 70261,
        'title': 'Mushoku Tensei: Isekai Ittara Honki Dasu',
        'title_english': 'Mushoku Tensei: Jobless Reincarnation',
        'title_japanese': '無職転生 ～異世界行ったら本気だす～',
        'type': 'Novel',
        'chapters': 260,
        'volumes': 26,
        'status': 'Finished',
        'score': 9.02,
        'scored_by': 60000,
        'rank': 7,
        'popularity': 18,
        'members': 140000,
        'synopsis': "Un nini de 34 años muere atropellado por un camión al salvar a unos estudiantes y reencarna en un mundo de magia y espadas conservando sus recuerdos. Bautizado como Rudeus Greyrat, jura no volver a desperdiciar su existencia y vivir al máximo su segunda oportunidad.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/1/121111.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/121111l.jpg'
            }
        },
        'genres': [
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 62, 'name': 'Isekai'}
        ],
        'authors': [{'name': 'Rifujin na Magonote'}]
    },
    {
        'mal_id': 60037,
        'title': 'Tensei shitara Slime Datta Ken',
        'title_english': 'That Time I Got Reincarnated as a Slime',
        'title_japanese': '転生したらスライムだった件',
        'type': 'Novel',
        'chapters': 300,
        'volumes': 22,
        'status': 'Publishing',
        'score': 8.88,
        'scored_by': 45000,
        'rank': 14,
        'popularity': 24,
        'members': 110000,
        'synopsis': "Satoru Mikami, un oficinista soltero apuñalado en plena calle, se reencarna en una caverna subterránea con el cuerpo gelatinoso de un slime. Dotado con la habilidad de 'Depredador' y 'Gran Sabio', Rimuru Tempest forjará una nación de monstruos en armonía con los humanos.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/2/189332.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/189332l.jpg'
            }
        },
        'genres': [
            {'mal_id': 1, 'name': 'Acción'},
            {'mal_id': 2, 'name': 'Aventura'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 62, 'name': 'Isekai'}
        ],
        'authors': [{'name': 'Fuse'}]
    },
    {
        'mal_id': 89357,
        'title': 'Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e (Classroom of the Elite)',
        'title_english': 'Classroom of the Elite',
        'title_japanese': 'ようこそ実力至上主義の教室へ',
        'type': 'Novel',
        'chapters': 180,
        'volumes': 14,
        'status': 'Finished',
        'score': 8.92,
        'scored_by': 55000,
        'rank': 11,
        'popularity': 15,
        'members': 130000,
        'synopsis': "La Escuela Metropolitana Avanzada de Tokio garantiza el 100% de ingreso universitario o empleo de elite a sus graduados, evaluando a sus estudiantes mediante puntos. Kiyotaka Ayanokouji oculta su asombrosa inteligencia y destrezas para mantenerse en la clase D, reservada para los estudiantes considerados defectuosos.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/2/177958.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/177958l.jpg'
            }
        },
        'genres': [
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 41, 'name': 'Suspense'},
            {'mal_id': 23, 'name': 'Escolar'}
        ],
        'authors': [{'name': 'Kinugasa, Shougo'}]
    },
    {
        'mal_id': 74697,
        'title': 'Re:Zero kara Hajimeru Isekai Seikatsu',
        'title_english': 'Re:ZERO -Starting Life in Another World-',
        'title_japanese': 'Re:ゼロから始める異世界生活',
        'type': 'Novel',
        'chapters': 400,
        'volumes': 37,
        'status': 'Publishing',
        'score': 8.85,
        'scored_by': 50000,
        'rank': 16,
        'popularity': 20,
        'members': 120000,
        'synopsis': "Subaru Natsuki es transportado súbitamente a un mundo de fantasía medieval al salir de una tienda de conveniencia. Sin magia ni habilidades físicas especiales, descubre que posee el 'Regreso por Muerte', permitiéndole retroceder en el tiempo cada vez que muere trágicamente.",
        'images': {
            'jpg': {
                'image_url': 'https://cdn.myanimelist.net/images/manga/2/150493.jpg',
                'large_image_url': 'https://cdn.myanimelist.net/images/manga/2/150493l.jpg'
            }
        },
        'genres': [
            {'mal_id': 8, 'name': 'Drama'},
            {'mal_id': 10, 'name': 'Fantasía'},
            {'mal_id': 41, 'name': 'Suspense'},
            {'mal_id': 62, 'name': 'Isekai'}
        ],
        'authors': [{'name': 'Nagatsuki, Tappei'}]
    }
]
