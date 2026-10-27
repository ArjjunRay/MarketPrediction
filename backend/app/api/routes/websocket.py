from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.monitoring.metrics import WEBSOCKET_CONNECTIONS

router = APIRouter(tags=["streaming"])


@router.websocket("/ws/market")
async def market_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    WEBSOCKET_CONNECTIONS.inc()
    try:
        await websocket.send_json(
            {
                "type": "connection.status",
                "status": "connected",
                "data_status": "unavailable",
                "message": "No real market-data provider is configured.",
            }
        )
        while True:
            message = await websocket.receive_json()
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif message.get("type") == "subscribe":
                symbol = str(message.get("symbol", "")).upper()[:16]
                await websocket.send_json(
                    {
                        "type": "subscription.status",
                        "symbol": symbol,
                        "status": "unavailable",
                        "message": "Provider credentials are not configured.",
                    }
                )
            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "code": "unsupported_message",
                        "message": "Supported message types are ping and subscribe.",
                    }
                )
    except WebSocketDisconnect:
        pass
    finally:
        WEBSOCKET_CONNECTIONS.dec()
