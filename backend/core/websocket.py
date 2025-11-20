"""
WebSocket Configuration for EMAS Backend
Minimal implementation for development

Author: Cavin Otieno
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

# Global WebSocket connections
connected_clients: List[WebSocket] = []

async def handle_websocket_connection(websocket: WebSocket):
    """Handle WebSocket connection"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Echo the message back
            await websocket.send_text(json.dumps({
                "type": "echo",
                "data": message,
                "status": "received"
            }))
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

def setup_websocket_handler(app: FastAPI):
    """Setup WebSocket endpoint"""
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await handle_websocket_connection(websocket)
    
    # Global broadcast function
    app.websocket_broadcast = broadcast_to_all
    
    print("🔌 WebSocket handler configured")

async def broadcast_to_all(message: dict):
    """Broadcast message to all connected clients"""
    if not connected_clients:
        return
    
    message_str = json.dumps(message)
    disconnected = []
    
    for client in connected_clients:
        try:
            await client.send_text(message_str)
        except Exception:
            disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)