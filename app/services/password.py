"""
Service for Password Generation
"""
# pylint: disable=duplicate-code

import string
from random import choice, choices, shuffle

from app.main import application_settings

NUMBERS: list[str] = list(string.digits)
LOWER_CASE_CHARS: list[str] = list(string.ascii_lowercase)
UPPER_CASE_CHARS: list[str] = list(string.ascii_uppercase)
SPECIAL_SYMBOLS: list[str] = list(string.punctuation)


class GeneratePasswordError(Exception):
    """
    Exception which is raise in case the password is too short.
    """


def generate_password(
    password_length: int = None,
    password_numbers: bool = None,
    password_lower_case_chars: bool = None,
    password_upper_case_chars: bool = None,
    password_special_symbols: bool = None,
) -> str:
    """
    Service for generation of passwords.

    :param password_length:
    :param password_numbers:
    :param password_lower_case_chars:
    :param password_upper_case_chars:
    :param password_special_symbols:
    :return: the password string
    """
    # pylint: disable=too-many-branches

    if password_length is None:
        password_length = application_settings.default_password_length

    if password_numbers is None:
        password_numbers = application_settings.password_numbers

    if password_lower_case_chars is None:
        password_lower_case_chars = (
            application_settings.password_lower_case_chars
        )

    if password_upper_case_chars is None:
        password_upper_case_chars = (
            application_settings.password_upper_case_chars
        )

    if password_special_symbols is None:
        password_special_symbols = application_settings.password_special_symbols

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
        raise GeneratePasswordError(
            "At least one flag needs to be specified: password_numbers, "
            "password_lower_case_chars, password_upper_case_chars, "
            "password_special_symbols"
        )

    # Generate the password
    chars: int = password_length // flags_set
    chars_remainder: int = password_length % flags_set
    password: str = ""
    fills: list[str] = []

    if password_numbers:
        password += "".join(choices(NUMBERS, k=chars))
        fills.append("".join(choices(NUMBERS, k=chars_remainder)))

    if password_lower_case_chars:
        password += "".join(choices(LOWER_CASE_CHARS, k=chars))
        fills.append("".join(choices(LOWER_CASE_CHARS, k=chars_remainder)))

    if password_upper_case_chars:
        password += "".join(choices(UPPER_CASE_CHARS, k=chars))
        fills.append("".join(choices(UPPER_CASE_CHARS, k=chars_remainder)))

    if password_special_symbols:
        password += "".join(choices(SPECIAL_SYMBOLS, k=chars))
        fills.append("".join(choices(SPECIAL_SYMBOLS, k=chars_remainder)))

    # Fill up the password to it's full length requirement
    fill_up: str = choice(fills)
    password += fill_up

    # Shuffle the password chars so no pattern is recognizable
    password_list: list[str] = list(password)
    shuffle(password_list)
    password = "".join(password_list)

    return password
