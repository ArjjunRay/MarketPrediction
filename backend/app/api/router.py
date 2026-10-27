from fastapi import APIRouter

from app.api.routes import capabilities, health, instruments, public_data, websocket

router = APIRouter()
router.include_router(health.router)
router.include_router(capabilities.router)
router.include_router(instruments.router)
router.include_router(public_data.router)
router.include_router(websocket.router)
