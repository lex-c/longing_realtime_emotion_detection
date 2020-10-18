from channels.generic.websocket import WebsocketConsumer


class BlahConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self):
        pass

    def receive(self, text_data):
        print('receiving')