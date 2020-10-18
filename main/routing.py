from django.urls import path
from . import consumers2

websocket_urlpatterns = [
    path('', consumers2.BlahConsumer)
]