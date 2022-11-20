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
