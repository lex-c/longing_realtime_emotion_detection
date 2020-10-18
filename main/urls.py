from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('album_detail/<str:album_name>/', views.album_detail, name='album_detail'),
    path('remove_photo/<int:album_id>/<int:photo_id>/', views.remove_photo, name='remove_photo'),
    path('f_login/<int:user_id>/', views.f_login, name='f_login'),
    path('accounts/signup', views.signup, name='signup'),
]