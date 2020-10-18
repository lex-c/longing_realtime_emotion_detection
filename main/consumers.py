from channels.generic.websocket import WebsocketConsumer
import json

class CamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({ 
            'message': 'something'
         }))
    
    def disconnect(self, code):
        pass

    def receive(self, text_data):
       text_json = json.loads(text_data)
       message = text_json['message']
       print(message)
    

