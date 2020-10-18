from channels.generic.websocket import WebsocketConsumer
import json

class CamConsumer(WebsocketConsumer):
    def websocket_connect(self, event):
        self.accept()
        self.send(text_data=json.dumps({ 
            'message': 'something'
         }))
    
    def websocket_receive(self, data):
       text_json = json.loads(data)
       message = data['message']
       print(message)
    
    def websocket_disconnect(self, text_data):
        pass

