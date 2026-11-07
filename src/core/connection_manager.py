from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts the incoming WebSocket connection and adds it to the active pool."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection from the active pool."""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Sends a message to a specific WebSocket connection."""
        await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        """Sends a message to all active WebSocket connections."""
        for connection in self.active_connections:
            await connection.send_text(message)
