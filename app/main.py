"""Application

Instantiation and configuration of the FastApi application.
"""
# pylint: disable=duplicate-code

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from furl import furl

from app.api.v1.api import api_router
from app.app_settings import application_settings

app = FastAPI(
    title=application_settings.application_name,
    description=application_settings.application_description,
    version=application_settings.api_version,
)


# Just doing a forward to the API autodocs here because the application
# does not contain any other functionality than this one API endpoint.
@app.get("/", include_in_schema=False)
def redirect_to_autodocs(request: Request) -> RedirectResponse:
    """Home Page

    :param request:
    :return: RedirectResponse
    """
    furl_item: furl = furl(request.base_url)
    furl_item.path /= app.docs_url
    return RedirectResponse(furl_item.url)


app.include_router(
    api_router, prefix=application_settings.api_major_version_path
)
