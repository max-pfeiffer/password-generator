"""Application

Instantiation and configuration of the FastApi application.
"""
# pylint: disable=duplicate-code

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.app_settings import application_settings


app = FastAPI(
    title=application_settings.application_name,
    description=application_settings.application_description,
    version=application_settings.api_version,
)

app.include_router(
    api_router, prefix=application_settings.api_major_version_path
)
