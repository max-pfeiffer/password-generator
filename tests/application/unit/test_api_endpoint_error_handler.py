"""
Tests for api_error_handler Decorator
"""
# pylint: disable=duplicate-code

import pytest
from fastapi import HTTPException
from fastapi import status

from app.api.decorators import api_error_handler
from app.services import GeneratePasswordInvalidFlagsError

TEST_DATA: list = [
    {
        "exception": GeneratePasswordInvalidFlagsError(),
        "status_code": status.HTTP_400_BAD_REQUEST,
    },
    {
        "exception": HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
    {
        "exception": Exception(),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_decorator(test_data):
    """
    Test for sync functionality.

    :param test_data: dict
    :return:
    """
    exception = test_data["exception"]
    status_code = test_data["status_code"]

    @api_error_handler
    def throw_exception():
        raise exception

    with pytest.raises(HTTPException) as excinfo:
        throw_exception()

    assert status_code == excinfo.value.status_code


@pytest.mark.parametrize("test_data", TEST_DATA)
@pytest.mark.asyncio
async def test_async_decorator(test_data):
    """
    Test for async functionality.

    :param test_data: dict
    :return:
    """

    exception = test_data["exception"]
    status_code = test_data["status_code"]

    @api_error_handler
    async def throw_exception():
        raise exception

    with pytest.raises(HTTPException) as excinfo:
        await throw_exception()

    assert status_code == excinfo.value.status_code
