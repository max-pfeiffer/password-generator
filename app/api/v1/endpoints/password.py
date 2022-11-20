"""
Password API Endpoints
"""

from fastapi import APIRouter

from app.app_settings import application_settings
from app.models import Password

router = APIRouter()


# Using HTTP method get here as we are only requesting (generated) data and
# not creating a resource: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET
# Pluralising the resource name is a good practice:
# https://opensource.zalando.com/restful-api-guidelines/#134
# pylint: disable=unused-argument
@router.get("/passwords", response_model=Password)
def get_password(
    password_length: int = application_settings.default_password_length,
    password_numbers: bool = application_settings.password_numbers,
    password_lower_case_chars: bool = application_settings.password_lower_case_chars,
    password_upper_case_chars: bool = application_settings.password_upper_case_chars,
    password_special_symbols: bool = application_settings.password_special_symbols,
) -> Password:
    """
    Returns a generated password.

    :param password_length: int
    :param password_numbers: bool
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return: password: str
    """
