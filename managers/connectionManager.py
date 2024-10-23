from fastapi import WebSocket
from .userManger import Users
import json

class ConnectionManager(Users):
    def __init__(self):
        super().__init__()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(websocket)
        if(len(self.q) < 2):
            self.q.append(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        for clien in self.conn_list:
            if(clien == websocket):
                await websocket.send_text(message)
        
    def disconnect(self, websocket: WebSocket):
        self.q.remove(websocket)
        self.conn_list.remove(websocket)


