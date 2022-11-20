"""
Fast API Application
"""
from fastapi import FastAPI

from app.app_settings import ApplicationSettings

app = FastAPI(
    title=ApplicationSettings().application_name,
    description=ApplicationSettings().application_description,
    version=ApplicationSettings().api_version,
)
