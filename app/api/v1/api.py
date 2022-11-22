"""API: Version 1"""
from fastapi import APIRouter

from app.api.v1.endpoints import password

api_router = APIRouter()
api_router.include_router(password.router, tags=["Passwords"])
