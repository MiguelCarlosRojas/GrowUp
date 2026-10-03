import json
import logging
import asyncio
from django.conf import settings
from django.db.models import Count, Sum
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

# Active connected WebSocket clients registry
CONNECTED_CLIENTS = set()


@sync_to_async
def get_live_metrics_data():
    """
    Executes a single consolidated query to fetch only necessary live metrics
    avoiding multiple roundtrips to the database.
    """
    from novels.models import Novel, Chapter
    from catalog.models import ItemDiscussion

    # 1 consolidated query for novel aggregate
    novel_stats = Novel.objects.exclude(status='draft').aggregate(
        total_novels=Count('id'),
        total_views=Sum('views_count')
    )

    # 1 query for latest discussions fetching only necessary fields
    latest_discussions = list(
        ItemDiscussion.objects.filter(parent__isnull=True)
        .select_related('user', 'user__profile')
        .only('id', 'item_title', 'content', 'created_at', 'user__username', 'user__profile__uid')
        .order_by('-created_at')[:3]
        .values('id', 'item_title', 'content', 'created_at', 'user__username', 'user__profile__uid')
    )

    for d in latest_discussions:
        d['uid'] = str(d.pop('user__profile__uid', ''))
        d['username'] = d.pop('user__username', 'anon')
        d['created_at'] = d['created_at'].isoformat() if d.get('created_at') else ''

    return {
        'total_novels': novel_stats.get('total_novels') or 0,
        'total_views': novel_stats.get('total_views') or 0,
        'active_connections': len(CONNECTED_CLIENTS),
        'latest_discussions': latest_discussions,
    }


@sync_to_async
def get_live_notifications_data():
    """
    Consolidated query returning 2 real-time notifications with role-differentiated
    icons (bi-star-fill text-warning for reviews, bi-chat-left-dots-fill text-info for discussions).
    Fetches only strictly required fields.
    """
    from catalog.models import ItemReview, ItemDiscussion

    notifications = []

    # 1 query fetching only needed fields for recent review
    latest_review = ItemReview.objects.select_related('user').only(
        'id', 'item_title', 'rating', 'headline', 'user__username'
    ).order_by('-created_at').first()

    if latest_review:
        notifications.append({
            'type': 'review',
            'icon': 'bi-star-fill text-warning',
            'title': 'Nueva Calificación / Reseña',
            'text': f"@{latest_review.user.username} calificó '{latest_review.item_title}' con {latest_review.rating} estrellas: \"{latest_review.headline}\"",
            'duration': 5000
        })

    # 1 query fetching only needed fields for recent discussion/question
    latest_discussion = ItemDiscussion.objects.select_related('user').only(
        'id', 'item_title', 'discussion_type', 'content', 'user__username'
    ).order_by('-created_at').first()

    if latest_discussion:
        disc_type = 'Pregunta' if latest_discussion.discussion_type == 'question' else 'Debate'
        notifications.append({
            'type': 'discussion',
            'icon': 'bi-chat-left-dots-fill text-info',
            'title': f'Nueva Participación ({disc_type})',
            'text': f"@{latest_discussion.user.username} en '{latest_discussion.item_title}': \"{latest_discussion.content[:65]}...\"",
            'duration': 5000
        })

    return notifications


async def websocket_application(scope, receive, send):
    """
    Native ASGI 3.0 WebSocket application.
    Handles real-time communication without requiring heavyweight Redis brokers.
    """
    client_id = f"{scope.get('client', ['unknown'])[0]}_{id(receive)}"
    CONNECTED_CLIENTS.add(client_id)

    try:
        while True:
            event = await receive()
            event_type = event.get('type')

            if event_type == 'websocket.connect':
                await send({'type': 'websocket.accept'})

                # Push initial live metrics using 1 single consolidated query
                metrics = await get_live_metrics_data()
                await send({
                    'type': 'websocket.send',
                    'text': json.dumps({
                        'event': 'live_metrics',
                        'data': metrics,
                    })
                })

                # Push real-time notifications with role-differentiated icons
                notifications = await get_live_notifications_data()
                await send({
                    'type': 'websocket.send',
                    'text': json.dumps({
                        'event': 'live_notifications',
                        'notifications': notifications,
                    })
                })

            elif event_type == 'websocket.receive':
                text_data = event.get('text', '{}')
                try:
                    msg = json.loads(text_data)
                except Exception:
                    msg = {}

                action = msg.get('action')

                if action == 'ping':
                    await send({
                        'type': 'websocket.send',
                        'text': json.dumps({'event': 'pong'})
                    })
                elif action == 'get_metrics':
                    metrics = await get_live_metrics_data()
                    await send({
                        'type': 'websocket.send',
                        'text': json.dumps({
                            'event': 'live_metrics',
                            'data': metrics,
                        })
                    })
                elif action == 'get_notifications':
                    notifications = await get_live_notifications_data()
                    await send({
                        'type': 'websocket.send',
                        'text': json.dumps({
                            'event': 'live_notifications',
                            'notifications': notifications,
                        })
                    })
                elif action == 'subscribe':
                    topic = msg.get('topic', 'global')
                    await send({
                        'type': 'websocket.send',
                        'text': json.dumps({
                            'event': 'subscribed',
                            'topic': topic,
                            'status': 'active'
                        })
                    })

            elif event_type == 'websocket.disconnect':
                break

    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
    finally:
        CONNECTED_CLIENTS.discard(client_id)
