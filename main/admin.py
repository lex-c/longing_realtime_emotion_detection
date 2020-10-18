from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Photo, Album, FaceToUser

# Register your models here.

class AlbumPhotosInline(admin.StackedInline):
    model = Photo
    extra = 5

class UserAlbumsInline(admin.TabularInline):
    model = Album
    extra = 3


class UserAdminr(UserAdmin):
    inlines = [UserAlbumsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdminr)
admin.site.register(Photo)
admin.site.register(FaceToUser)