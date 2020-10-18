from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import wc

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(wc.routing.websocket_urlpatterns)
    )
})