"""
Tests for Password  Generation
"""
import pytest

from app.services.exceptions import PasswordToShortError, PasswordToLongError
from app.services.password import (
    generate_password,
    NUMBERS,
    LOWER_CASE_CHARS,
    UPPER_CASE_CHARS,
    SPECIAL_SYMBOLS,
)


@pytest.mark.parametrize("password_length", [8, 15, 50, 100, 200])
@pytest.mark.parametrize("password_numbers", [True, False])
@pytest.mark.parametrize("password_lower_case_chars", [True, False])
@pytest.mark.parametrize("password_upper_case_chars", [True, False])
@pytest.mark.parametrize("password_special_symbols", [True, False])
def test_generate_password(
    password_length,
    password_numbers,
    password_lower_case_chars,
    password_upper_case_chars,
    password_special_symbols,
):
    """
    Parameterised test for successful password generation.

    :param password_length:
    :param password_numbers:
    :param password_lower_case_chars:
    :param password_upper_case_chars:
    :param password_special_symbols:
    :return:
    """
    # pylint: disable=duplicate-code
    # pylint: disable=unsupported-membership-test
    # pylint: disable=too-many-branches

    password: str = generate_password(
        password_length=password_length,
        password_numbers=password_numbers,
        password_lower_case_chars=password_lower_case_chars,
        password_upper_case_chars=password_upper_case_chars,
        password_special_symbols=password_special_symbols,
    )

    assert password_length == len(password)

    if password_numbers:
        assert any(number in password for number in NUMBERS)
    else:
        assert not any(number in password for number in NUMBERS)

    if password_lower_case_chars:
        assert any(char in password for char in LOWER_CASE_CHARS)
    else:
        assert not any(char in password for char in LOWER_CASE_CHARS)

    if password_upper_case_chars:
        assert any(char in password for char in UPPER_CASE_CHARS)
    else:
        assert not any(char in password for char in UPPER_CASE_CHARS)

    if password_special_symbols:
        assert any(char in password for char in SPECIAL_SYMBOLS)
    else:
        assert not any(char in password for char in SPECIAL_SYMBOLS)


def test_generate_too_short_password():
    """
    Test for failed password generation.

    :return:
    """
    with pytest.raises(PasswordToShortError):
        generate_password(password_length=5)


def test_generate_too_long_password():
    """
    Test for failed password generation.

    :return:
    """
    with pytest.raises(PasswordToLongError):
        generate_password(password_length=500)
