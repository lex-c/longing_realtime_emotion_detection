import json
# import cv2
import os
import io
import base64
from PIL import Image
import numpy as np
import main.views as views
from channels.consumer import AsyncConsumer, async_to_sync

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

# image_url = None
# is_album_open = False
# in_auth = False
# message = None
# face_added = False
# signup_count = 0
# emotion = {'Type': 'NONE'}
# img = None


class CamConsumer(AsyncConsumer):
    # smile_cascade = cv2.CascadeClassifier('main/static/main/haarcascade_smile.xml')
    image_url = None
    is_album_open = False
    in_auth = False
    message = None
    face_added = False
    signup_count = 0
    emotion = {'Type': 'NONE'}
    img = None

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_disconnect(self, code):
        pass

    async def websocket_receive(self, text_data):
        if text_data['text'] == 'close_album':
            self.is_album_open = False
            return
        elif text_data['text'] == 'album_open':
            self.is_album_open = True
            return
        elif text_data['text'][0:1] == '{':
            text_to_json = json.loads(text_data['text'])
            if (text_to_json['send_pics']):
                user_id = text_to_json['send_pics']
                if self.is_album_open:
                    await self.send_pics(user_id)
                    return
        elif text_data['text'] == 'auth_detect':
            print('auth')
            is_not_first = bool(self.in_auth)
            self.in_auth = True
            if is_not_first:
                user_id_if_authed = await views.search_face(self.img)
                if user_id_if_authed:
                    self.in_auth = False
                    confirm_json = json.dumps({ 'f_confirmed': user_id_if_authed })
                    await self.send({ 'type': 'websocket.send', 'text': confirm_json })
            return
        elif text_data['text'] == 'sign_up_pic':
            print('signup')
            self.in_auth = True
            if not self.face_added:
                if self.signup_count == 2:
                    face_info = await views.add_face(self.img)
                    if face_info:
                        self.face_added = True
                        face_info_json = json.dumps({'face_info': face_info })
                        await self.send({ 'type': 'websocket.send', 'text': face_info_json})
                        self.in_auth = False
                    else: self.signup_count = 0
                else: self.signup_count += 1
        elif self.is_album_open or self.in_auth:
            print('album open or auth', self.is_album_open, self.in_auth)
            img_buf = base64.b64decode(text_data['text'])
            nparr = np.frombuffer(img_buf, dtype=np.uint8)
            if len(nparr) > 0:
                # cv2.imwrite('image.png', img)
                self.img = io.BytesIO(img_buf).getvalue()
                if self.is_album_open:
                    self.emotion = await views.get_emotion_expression(self.img)
                    if not self.emotion:
                        self.emotion = { 'Type': 'None' }
                    emotion_json = json.dumps({ 'emotion': self.emotion['Type'] })
                    await self.send({ 'type': 'websocket.send', 'text': emotion_json })
        else:
            print(f'in the receive no album open and no auth')

    async def send_pics(self, user_id):
    # global is_album_open, emotion, image_url
        if self.image_url:
            if self.emotion['Type'] in ['HAPPY', 'SAD', 'NOSTALGIA', 'LONGING']:
                album_name = self.emotion['Type']
                if self.emotion['Type'] == 'HAPPY': album_name = 'HAPPINESS'
                albums_if_new = await views.save_photo_to_album(self.image_url, album_name, user_id)
                albums_json = json.dumps({ 'new_album': albums_if_new })
                if albums_if_new: await self.send({ 'type': 'websocket.send', 'text': albums_json })
        self.image_url = views.bing_search()
        if self.is_album_open:
            await self.send({ 'type': 'websocket.send', 'text': self.image_url })


