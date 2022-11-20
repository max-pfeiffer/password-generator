"""
Fast API Application
"""
from fastapi import FastAPI

from app.app_settings import ApplicationSettings

application_settings: ApplicationSettings = ApplicationSettings()

# pylint: disable=duplicate-code
app = FastAPI(
    title=application_settings.application_name,
    description=application_settings.application_description,
    version=application_settings.api_version,
)
