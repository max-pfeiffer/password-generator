"""Password API Endpoints"""
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
    description="Returns a generated password. Please specify at least one of "
    "these flags: password_numbers, password_lower_case_chars, "
    "password_upper_case_chars or password_special_symbols. "
    "Otherwise an error is raised.",
)
@api_error_handler
def get_password(
    password_length: int = Query(
        default=application_settings.default_password_length,
        ge=application_settings.min_password_length,
        le=application_settings.max_password_length,
        description="Length of the password",
    ),
    password_numbers: bool = Query(
        default=application_settings.password_numbers,
        description="Flag, true if the password should contain numbers",
    ),
    password_lower_case_chars: bool = Query(
        default=application_settings.password_lower_case_chars,
        description="Flag, true if the password should contain lower case chars",
    ),
    password_upper_case_chars: bool = Query(
        default=application_settings.password_upper_case_chars,
        description="Flag, true if the password should contain upper case chars",
    ),
    password_special_symbols: bool = Query(
        default=application_settings.password_special_symbols,
        description="Flag, true if the password should contain special symbols",
    ),
) -> Password:
    """Returns a generated password.

    :param password_length: int
        Length of the password
    :param password_numbers: bool
        Flag, True if the password should contain numbers
    :param password_lower_case_chars: bool
        Flag, True if the password should contain lower case chars
    :param password_upper_case_chars: bool
        Flag, True if the password should contain upper case chars
    :param password_special_symbols: bool
        Flag, True if the password should contain special symbols
    :return: password: Password
        Model containing the password
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
