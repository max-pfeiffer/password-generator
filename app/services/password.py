"""
Service for Password Generation
"""
import string

from app.main import application_settings
from app.services.exceptions import PasswordToShortError, PasswordToLongError

NUMBERS: list[str] = list(string.digits)
LOWER_CASE_CHARS: list[str] = list(string.ascii_lowercase)
UPPER_CASE_CHARS: list[str] = list(string.ascii_uppercase)
SPECIAL_SYMBOLS: list[str] = list(string.punctuation)


def generate_password(
    password_length: int = application_settings.default_password_length,
    password_numbers: bool = application_settings.password_numbers,
    password_lower_case_chars: bool = application_settings.password_lower_case_chars,
    password_upper_case_chars: bool = application_settings.password_upper_case_chars,
    password_special_symbols: bool = application_settings.password_special_symbols,
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
    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument

    if password_length < application_settings.min_password_length:
        raise PasswordToShortError()

    if password_length > application_settings.max_password_length:
        raise PasswordToLongError()
