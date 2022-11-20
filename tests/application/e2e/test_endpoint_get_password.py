"""
Tests for /passwords endpoint
"""
# pylint: disable=duplicate-code

import pytest
from furl import furl
from httpx import Response
from fastapi import status

from app.app_settings import application_settings


@pytest.mark.parametrize("password_length", [8, 15, 50, 100, 200])
@pytest.mark.parametrize("password_numbers", [True, False])
@pytest.mark.parametrize("password_lower_case_chars", [True, False])
@pytest.mark.parametrize("password_upper_case_chars", [True, False])
@pytest.mark.parametrize("password_special_symbols", [True, False])
def test_get_password(
    test_client,
    password_length,
    password_numbers,
    password_lower_case_chars,
    password_upper_case_chars,
    password_special_symbols,
):
    """
    End-to-end test for /password endpoint.

    :param test_client: TestClient
    :param password_length: int
    :param password_numbers: bool
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return:
    """
    # pylint: disable=too-many-arguments

    # Using a URL manipulation library here as URL tinkering is a bit error-
    # prone because of syntax and character encoding
    furl_item = furl(application_settings.api_major_version_path)
    furl_item.path /= "passwords"
    furl_item.args["password_length"] = password_length
    furl_item.args["password_numbers"] = password_numbers
    furl_item.args["password_lower_case_chars"] = password_lower_case_chars
    furl_item.args["password_upper_case_chars"] = password_upper_case_chars
    furl_item.args["password_special_symbols"] = password_special_symbols
    url: str = furl_item.url

    response: Response = test_client.get(url)

    # Test handling of invalid flag combination
    if (
        sum(
            [
                password_numbers,
                password_lower_case_chars,
                password_upper_case_chars,
                password_special_symbols,
            ]
        )
        == 0
    ):
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    else:
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "password_length", [1, 2, 3, 4, 5, 201, 202, 203, 204, 205]
)
@pytest.mark.parametrize("password_numbers", [True, False])
@pytest.mark.parametrize("password_lower_case_chars", [True, False])
@pytest.mark.parametrize("password_upper_case_chars", [True, False])
@pytest.mark.parametrize("password_special_symbols", [True, False])
def test_get_password_invalid_password_length(
    test_client,
    password_length,
    password_numbers,
    password_lower_case_chars,
    password_upper_case_chars,
    password_special_symbols,
):
    """
    End-to-end test for /password endpoint.

    :param test_client: TestClient
    :param password_length: int
    :param password_numbers: bool
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return:
    """
    # pylint: disable=too-many-arguments

    # Using a URL manipulation library here as URL tinkering is a bit error-
    # prone because of syntax and character encoding
    furl_item = furl(application_settings.api_major_version_path)
    furl_item.path /= "passwords"
    furl_item.args["password_length"] = password_length
    furl_item.args["password_numbers"] = password_numbers
    furl_item.args["password_lower_case_chars"] = password_lower_case_chars
    furl_item.args["password_upper_case_chars"] = password_upper_case_chars
    furl_item.args["password_special_symbols"] = password_special_symbols
    url: str = furl_item.url

    response: Response = test_client.get(url)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
