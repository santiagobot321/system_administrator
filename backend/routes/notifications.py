from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

# Create a single instance of the manager to be used across the application
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    The main WebSocket endpoint that handles connections from clients
    (both the dashboard and attendees' phones).
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive, waiting for messages if needed.
            # For this use case, we mainly care about broadcasting from the server.
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
