"""Services

Services for the application. Services are used to separate functionality
and/or business logic from the API. They sit between API and the
persistence layer: API - Service - Repository
"""
# pylint: disable=duplicate-code

import string
from secrets import choice

from app.app_settings import application_settings

NUMBERS: str = string.digits
LOWER_CASE_CHARS: str = string.ascii_lowercase
UPPER_CASE_CHARS: str = string.ascii_uppercase
SPECIAL_SYMBOLS: str = string.punctuation


class GeneratePasswordError(Exception):
    """
    Exception which is raised when there is a problem with the password_length.
    """


class GeneratePasswordInvalidFlagsError(Exception):
    """
    Exception which is raised in case of invalid flags.
    """


def generate_password(
    password_length: int,
    password_numbers: bool,
    password_lower_case_chars: bool,
    password_upper_case_chars: bool,
    password_special_symbols: bool,
) -> str:
    """Service for password generation.

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
    :return: the password string
    """
    # pylint: disable=too-many-branches

    # Safeguard invalid password_length
    if password_length < application_settings.min_password_length:
        raise GeneratePasswordError(
            "Specified password_length is less than min_password_length."
        )

    if password_length > application_settings.max_password_length:
        raise GeneratePasswordError(
            "Specified password_length is greater than max_password_length."
        )

    # Check for invalid flag combination
    flags: list[bool] = [
        password_numbers,
        password_lower_case_chars,
        password_upper_case_chars,
        password_special_symbols,
    ]
    flags_set: int = sum(flags)

    if flags_set == 0:
        raise GeneratePasswordInvalidFlagsError(
            "At least one flag needs to be specified: password_numbers, "
            "password_lower_case_chars, password_upper_case_chars or "
            "password_special_symbols"
        )

    # Generate the password
    alphabet: str = ""

    if password_numbers:
        alphabet += NUMBERS

    if password_lower_case_chars:
        alphabet += LOWER_CASE_CHARS

    if password_upper_case_chars:
        alphabet += UPPER_CASE_CHARS

    if password_special_symbols:
        alphabet += SPECIAL_SYMBOLS

    while True:
        password = "".join(choice(alphabet) for index in range(password_length))

        tests: list = []
        if password_numbers:
            tests.append(any(number in password for number in NUMBERS))

        if password_lower_case_chars:
            tests.append(any(char in password for char in LOWER_CASE_CHARS))

        if password_upper_case_chars:
            tests.append(any(char in password for char in UPPER_CASE_CHARS))

        if password_special_symbols:
            tests.append(any(char in password for char in SPECIAL_SYMBOLS))

        if all(tests):
            break

    return password
