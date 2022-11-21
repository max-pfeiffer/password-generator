"""
Decorators for APIs
"""
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

from fastapi import HTTPException, status

from app.models import HTTPExceptionResponseModel
from app.services import GeneratePasswordInvalidFlagsError


def api_error_handler(function: Callable):
    """
    Decorator to unify error handling on API endpoints. As Fast API
    supports sync and async endpoints it supports this as well.

    :param function: the function to wrap
    :return:
    """
    # pylint: disable=duplicate-code

    if iscoroutinefunction(function):

        @wraps(function)
        async def async_wrapper(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except GeneratePasswordInvalidFlagsError as flags_exc:
                detail: dict = HTTPExceptionResponseModel.create_from_exception(
                    flags_exc
                ).dict()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail,
                ) from flags_exc
            except HTTPException as http_exc:
                raise http_exc
            except Exception as exc:
                detail: dict = HTTPExceptionResponseModel.create_from_exception(
                    exc
                ).dict()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=detail,
                ) from exc

        return async_wrapper

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except GeneratePasswordInvalidFlagsError as flags_exc:
            detail: dict = HTTPExceptionResponseModel.create_from_exception(
                flags_exc
            ).dict()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            ) from flags_exc
        except HTTPException as http_exc:
            raise http_exc
        except Exception as exc:
            detail: dict = HTTPExceptionResponseModel.create_from_exception(
                exc
            ).dict()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail,
            ) from exc

    return wrapper
