import json
from channels.generic.websocket import WebsocketConsumer
import cv2 as cv2
import io
import base64
import numpy as np
# from longing.main import views






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
            message = json.loads(text_data)['message']
            print(message[0])
            if message[0] == 'close_album':
                is_album_open = False
                return
            elif message[0] == 'album_open':
                is_album_open = True
            elif message[0] == 'send_pics':
                user_id = message[1]
                if is_album_open:
                    self.send_pics(self, user_id)
                    return
            elif message[0] == 'auth_detect':
                print('auth')
                is_not_first = bool(in_auth)
                in_auth = True
                if is_not_first:
                    isAuthed = views.search_face(self, img)
                    if isAuthed: in_auth = False
                return
            elif message[0] == 'sign_up_pic':
                print('signup')
                in_auth = True
                if not face_added:
                    if signup_count == 2:
                        face_info = views.add_face(img)
                        if face_info:
                            face_added = True
                            self.send(text_data=json.dumps({ 'message': ['face_info', face_info] }))
                            in_auth = False
                        else: signup_count = 0
                    else: signup_count += 1
        elif is_album_open or in_auth:
            print('album open or auth', is_album_open, in_auth)
            img_buf = base64.b64decode(text_data)
            nparr = np.frombuffer(img_buf, dtype=np.uint8)
            if len(nparr) > 0:
                # cv2.imwrite('image.png', img)
                img = io.BytesIO(img_buf).read()
                if is_album_open:
                    emotion = views.get_emotion_expression(img)
                    if not emotion:
                        emotion = { 'Type': 'None' }
        else:
            print(f'in the receive no album open and no auth')

    def send_pics(socket, user_id):
    # global is_album_open, emotion, image_url
        if image_url:
            if emotion['Type'] in ['HAPPINESS', 'SAD', 'NOSTALGIA', 'LONGING']:
                album_name = emotion['Type']
                albums_if_new = views.save_photo_to_album(image_url, album_name, user_id)
                if albums_if_new: socket.send(text_data=json.dumps({'message': ['new_album', albums_if_new]}))
        image_url = views.bing_search()
        if is_album_open:
            socket.send(text_data=json.dumps({
                'message': image_url
            }))


