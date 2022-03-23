from fastapi import APIRouter
from .handlers import user, training, service

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(service.router, prefix="/service", tags=["service"])
