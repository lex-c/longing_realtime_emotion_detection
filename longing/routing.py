from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing as rout

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rout.websocket_urlpatterns
            )
    )
})