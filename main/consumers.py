import json
# import cv2
import os
import io
import base64
import numpy as np
import main
from channels.generic.websocket import WebsocketConsumer

# image_url = None
# is_album_open = False
# in_auth = False
# message = None
# face_added = False
# signup_count = 0
# emotion = {'Type': 'NONE'}
# img = None


class CamConsumer(WebsocketConsumer):
    # smile_cascade = cv2.CascadeClassifier('main/static/main/haarcascade_smile.xml')
    image_url = None
    is_album_open = False
    in_auth = False
    message = None
    face_added = False
    signup_count = 0
    emotion = {'Type': 'NONE'}
    img = None

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        # global is_album_open, message, in_auth, emotion, face_added, signup_count, img
        if text_data[0:1] == '{':
            self.message = json.loads(text_data)['message']
            print(self.message[0])
            if self.message[0] == 'close_album':
                self.is_album_open = False
                return
            elif self.message[0] == 'album_open':
                self.is_album_open = True
            elif self.message[0] == 'send_pics':
                user_id = self.message[1]
                if self.is_album_open:
                    self.send_pics(self, user_id)
                    return
            elif self.message[0] == 'auth_detect':
                print('auth')
                is_not_first = bool(self.in_auth)
                self.in_auth = True
                if is_not_first:
                    isAuthed = views.search_face(self, img)
                    if isAuthed: self.in_auth = False
                return
            elif self.message[0] == 'sign_up_pic':
                print('signup')
                self.in_auth = True
                if not self.face_added:
                    if self.signup_count == 2:
                        face_info = views.add_face(img)
                        if face_info:
                            self.face_added = True
                            self.send(text_data=json.dumps({ 'message': ['face_info', face_info] }))
                            self.in_auth = False
                        else: self.signup_count = 0
                    else: self.signup_count += 1
        elif self.is_album_open or self.in_auth:
            print('album open or auth', self.is_album_open, self.in_auth)
            img_buf = base64.b64decode(text_data)
            nparr = np.frombuffer(img_buf, dtype=np.uint8)
            if len(nparr) > 0:
                # cv2.imwrite('image.png', img)
                self.img = io.BytesIO(img_buf).read()
                if self.is_album_open:
                    self.emotion = views.get_emotion_expression(img)
                    if not self.emotion:
                        self.emotion = { 'Type': 'None' }
        else:
            print(f'in the receive no album open and no auth')

    def send_pics(self, user_id):
    # global is_album_open, emotion, image_url
        if self.image_url:
            if self.emotion['Type'] in ['HAPPINESS', 'SAD', 'NOSTALGIA', 'LONGING']:
                album_name = self.emotion['Type']
                albums_if_new = views.save_photo_to_album(image_url, album_name, user_id)
                if albums_if_new: self.send(text_data=json.dumps({'message': ['new_album', albums_if_new]}))
        self.image_url = views.bing_search()
        if self.is_album_open:
            self.send(text_data=json.dumps({
                'message': self.image_url
            }))


