"""
Async WebSocket Connection Manager and Event Broadcaster.
Supports real-time streaming to React Admin Dashboard clients across multiple channels.
"""

import json
import logging
from typing import Dict, List, Set, Any
from fastapi import WebSocket

logger = logging.getLogger("app.services.websocket")


class WebSocketManager:
    """
    Manages active WebSocket connections across channels and broadcasts real-time telemetry updates.
    """

    def __init__(self):
        self._channels: Dict[str, Set[WebSocket]] = {
            "dashboard": set(),
            "incidents": set(),
            "threats": set(),
            "activity": set(),
            "notifications": set(),
        }

    async def connect(self, websocket: WebSocket, channel: str = "dashboard"):
        await websocket.accept()
        if channel not in self._channels:
            self._channels[channel] = set()
        self._channels[channel].add(websocket)
        logger.info(f"[WebSocketManager] Client connected to channel '{channel}'")

    def disconnect(self, websocket: WebSocket, channel: str = "dashboard"):
        if channel in self._channels and websocket in self._channels[channel]:
            self._channels[channel].remove(websocket)
            logger.info(f"[WebSocketManager] Client disconnected from channel '{channel}'")

    async def broadcast_event(self, event_type: str, data: Dict[str, Any], channel: str = "dashboard"):
        """
        Broadcasts JSON payload to all connected clients in target channel.
        """
        if channel not in self._channels or not self._channels[channel]:
            return

        message_str = json.dumps({"event_type": event_type, "data": data})
        disconnected: Set[WebSocket] = set()

        for ws in self._channels[channel]:
            try:
                await ws.send_text(message_str)
                logger.info(f"EVENT SENT: {event_type} on channel '{channel}'")
            except Exception as exc:
                logger.warning(f"[WebSocketManager] Broadcast failed ({exc}). Queueing client for disconnect.")
                disconnected.add(ws)

        for ws in disconnected:
            self.disconnect(ws, channel)


websocket_manager = WebSocketManager()
