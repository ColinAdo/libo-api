import os

from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore
from channels.security.websocket import AllowedHostsOriginValidator # type: ignore
from django.core.asgi import get_asgi_application
from books import routing
from books.middleware.jwt_auth_middleware import JWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(routing.websocket_urlpatterns)
        )
    ),
})
