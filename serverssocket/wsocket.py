from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from managers.connectionManager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

@router.websocket("/ws")
async def ws_ep(websocket: WebSocket):
    print(f"ws server is running")
    print(websocket)
    await manager.connect(websocket)
    
    if manager.q and len(manager.q) > 1:
        peer_ws = manager.q.popleft()
        peer_ws = manager.q.popleft()
        manager.conn_list[websocket] = peer_ws
        manager.conn_list[peer_ws] = websocket

        # await websocket.send_text("Paired with a random user!")
        # await peer_ws.send_text("Paired with a random user!")

        # await  manager.send_message(f"Connected with random user {websocket}", websocket)
        # await manager.send_message(f"connected with random user {peer_ws}", peer_ws)
    else:
        manager.q.append(websocket)
        await manager.send_message("waiting for a peer", websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if websocket in manager.conn_list:
                peer_ws = manager.conn_list[websocket]
                await manager.send_message(data, peer_ws)
    except WebSocketDisconnect:
        if websocket in manager.q:
            manager.q.remove(websocket)
        if websocket in manager.conn_list:
            peer_websocket = manager.conn_list.pop(websocket)
            manager.conn_list.pop(peer_websocket, None)
            await manager.send_message("Your peer has disconnected.", peer_websocket)


@router.get("/totaluser")    
async def get_total_user():
    return manager.get_total_users()


