from channels.generic.websocket import WebsocketConsumer
import json

class CamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({ 
            'message': 'something'
         }))
    
    def disconnect(self, text_data):
        pass
    
    def receive(self, data):
       text_json = json.loads(data)
       message = data['message']
       print(message)
    

