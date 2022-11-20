"""
Models
"""

# pylint: disable=no-name-in-module
from pydantic import BaseModel, constr


class Password(BaseModel):
    """
    Model class for returning the password in a standardised way. We get a lot
    "for free" with subclassing Basemodel:
    * Data validation
    * JSON serialisation
    """

    # pylint: disable=too-few-public-methods

    password: constr(max_length=200)


class HTTPExceptionResponseModel(BaseModel):
    """
    This class is used to unify the error messages for Fast API HTTPExceptions.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=duplicate-code

    type: str
    message: str

    @classmethod
    def create_from_exception(cls, exc: Exception):
        """
        Factory function to create am instance.

        :param exc:
        :return:
        """
        type_text: str = type(exc).__name__
        message: str = str(exc)
        return cls(type=type_text, message=message)
