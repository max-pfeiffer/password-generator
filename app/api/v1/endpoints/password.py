"""
Password API Endpoints
"""
# pylint: disable=duplicate-code

from fastapi import APIRouter, Query, status

from app.api.decorators import api_error_handler
from app.app_settings import application_settings
from app.models import Password, HTTPExceptionResponseModel
from app.services import generate_password

router = APIRouter()


# Using HTTP method get here as we are only requesting (generated) data and
# not creating a resource: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET
# Pluralising the resource name is a good practice:
# https://opensource.zalando.com/restful-api-guidelines/#134
@router.get(
    "/passwords",
    response_model=Password,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionResponseModel},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HTTPExceptionResponseModel
        },
    },
)
@api_error_handler
def get_password(
    password_length: int = Query(
        default=application_settings.default_password_length,
        ge=application_settings.min_password_length,
        le=application_settings.max_password_length,
    ),
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
    password_string: str = generate_password(
        password_length,
        password_numbers,
        password_lower_case_chars,
        password_upper_case_chars,
        password_special_symbols,
    )
    password: Password = Password(password=password_string)
    return password
