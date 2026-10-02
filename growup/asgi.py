"""
ASGI config for growup project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growup.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_http_app = get_asgi_application()


async def application(scope, receive, send):
    """
    Unified ASGI application router handling both HTTP and WebSockets.
    """
    if scope['type'] == 'http':
        await django_http_app(scope, receive, send)
    elif scope['type'] == 'websocket':
        from catalog.websocket_service import websocket_application
        await websocket_application(scope, receive, send)
    elif scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:
        raise NotImplementedError(f"Protocol scope {scope['type']} is not supported.")

