from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Photo, Album, FaceToUser
from .bing import search
from . import faces
import json
from asgiref.sync import sync_to_async

photo_cache = []
wait_cap = 0
# Create your views here.

@login_required(login_url='../../accounts/login/')
def index(request):
    return render(request, 'main/index.html', {'user': request.user, 'user_albums': list(request.user.album_set.values_list('name', flat=True))})

@sync_to_async
def save_photo_to_album(image_url, album_name, user_id):
    print(f'in the save photo with album {album_name}, and user_id {user_id}')
    is_new_album = False
    user = User.objects.get(pk=user_id)
    if Photo.objects.filter(img_url=image_url).count() == 0:
        photo = Photo.objects.create(img_url=image_url)
    else:
        photo = list(Photo.objects.filter(img_url=image_url))[0]
    if Album.objects.filter(name=album_name).count() == 0:
        is_new_album = True
        album = Album.objects.create(name=album_name, user=user)
    else:
        album = list(Album.objects.filter(name=album_name))[0]
    photo.user.add(user_id)
    photo.save()
    album.photos.add(photo)
    album.save()
    user.album_set.add(album)
    user.save()
    if is_new_album: return list(user.album_set.values_list('name', flat=True))
    else: return False

def album_detail(request, album_name):
    albums = request.user.album_set.all()
    if isinstance(album_name, int):
        album = albums.filter(pk=album_name)[0]
    else:
        album = albums.filter(name=album_name)[0]
    return render(request, 'main/album_detail.html', {'user': request.user, 'album': album})

def remove_photo(request, album_id, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    album = Album.objects.get(pk=album_id)
    album.photos.remove(photo)
    album.save()
    if album.photos.count() > 0:
        return redirect('main:album_detail', album.name)
    else:
        album.delete()
        return redirect('main:index')

@sync_to_async
def add_face(img):
    face_info_if_exists = faces.search_face_in_faces(img)
    print('face_info from add_face search', face_info_if_exists)
    if face_info_if_exists:
        return face_info_if_exists
    else:
        face_info = faces.add_faces_to_collection(img)
        if not face_info: raise Exception('no face info')
        print('added face with info', face_info)
        return face_info

@sync_to_async
def search_face(img):
    face_info_if_found = faces.search_face_in_faces(img)
    print('face_info_from_search_auth', face_info_if_found)
    if face_info_if_found:
        print('in the found')
        if FaceToUser.objects.filter(FaceId=face_info_if_found[1]).count() > 0:
            print('in the Face to user found')
            face_user = list(FaceToUser.objects.filter(FaceId=face_info_if_found[1]))[0]
            username = list(face_user.user.all())[0].username
            user = User.objects.get(username=username)
            return user.id
        else: return None

def check_face_login(user):
    return FaceToUser.objects.filter(user__username=user.username).count() > 0

def f_login(request, user_id):
    user = User.objects.get(pk=user_id)
    if check_face_login(user):
        login(request, user)
        return redirect('main:index')
    else:
        return redirect('login')

def bing_search():
    global photo_cache
    if len(photo_cache) < 4:
        new_photos = search()
        for photo in new_photos:
            photo_cache.append(photo)
        print(len(photo_cache))
    photo_cache.pop(0)
    return photo_cache[0]

@sync_to_async
def get_emotion_expression(img):
    emotions_if_face = faces.aws_detect(img)
    if emotions_if_face:
        map_emotions = {  }
        for emotion in emotions_if_face:
            map_emotions[emotion['Type']] = emotion['Confidence']
            print(map_emotions)
        if emotions_if_face[0]['Confidence'] >= 95:
            return emotions_if_face[0]
        elif float(map_emotions['CALM']) >= 40.0 and (float(map_emotions['CONFUSED']) + float(map_emotions['SURPRISED']) >= 17):
            print('LUST', map_emotions)
            return { 'Type': 'LUST', 'Confidence': 99 }
        elif int(map_emotions['CALM']) >= 50 and float(map_emotions['HAPPY']) >= 5 and float(map_emotions['SAD']) >= 5:
            print('NOSTALGIA', map_emotions)
            return { 'Type': 'NOSTALGIA', 'Confidence': 99 }
        elif int(map_emotions['CALM']) >= 35 and int(map_emotions['SAD']) >= 30:
            print('LONGING', map_emotions)
            return { 'Type': 'LONGING', 'Confidence': 99 }
        elif emotions_if_face[0]['Confidence'] >= 60: return emotions_if_face[0]
        else: return None
    else: return None

def signup(request):
    if request.method == 'POST':
        new_user = User(username=request.POST['username'])
        if len(request.POST['first_name']) > 0:
            new_user.first_name = request.POST['first_name']
        if len(request.POST['last_name']) > 0:
            new_user.last_name = request.POST['last_name']
        new_user.set_password(request.POST['password1'])
        new_user.save()
        if request.POST['faceInfo']:
            face_info = list(request.POST['faceInfo'].split(' ')[0].split(','))
            face_user = FaceToUser(ExternalImageId=face_info[0], FaceId=face_info[1])
            face_user.save()
            face_user.user.add(new_user)
        login(request, new_user)
        print('new username:  ', new_user.username, 'id:  ', new_user.id, 'face info:  ', request.POST['faceInfo'])
        return redirect('main:index')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
