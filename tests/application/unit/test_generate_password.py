"""
Tests for Password  Generation
"""
# pylint: disable=duplicate-code

import pytest

from app.services import (
    generate_password,
    NUMBERS,
    LOWER_CASE_CHARS,
    UPPER_CASE_CHARS,
    SPECIAL_SYMBOLS,
    GeneratePasswordError,
    GeneratePasswordInvalidFlagsError,
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

    :param password_length: int
    :param password_numbers: bool
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return:
    """
    # pylint: disable=too-many-branches

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
        with pytest.raises(GeneratePasswordInvalidFlagsError):
            generate_password(
                password_length,
                password_numbers,
                password_lower_case_chars,
                password_upper_case_chars,
                password_special_symbols,
            )
        return

    # Test all the other successful cases
    password: str = generate_password(
        password_length,
        password_numbers,
        password_lower_case_chars,
        password_upper_case_chars,
        password_special_symbols,
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


@pytest.mark.parametrize("password_numbers", [True, False])
@pytest.mark.parametrize("password_lower_case_chars", [True, False])
@pytest.mark.parametrize("password_upper_case_chars", [True, False])
@pytest.mark.parametrize("password_special_symbols", [True, False])
def test_generate_too_short_password(
    password_numbers,
    password_lower_case_chars,
    password_upper_case_chars,
    password_special_symbols,
):
    """
    Test for failed password generation.

    :param password_numbers: int
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return:
    """
    with pytest.raises(GeneratePasswordError):
        generate_password(
            5,
            password_numbers,
            password_lower_case_chars,
            password_upper_case_chars,
            password_special_symbols,
        )


@pytest.mark.parametrize("password_numbers", [True, False])
@pytest.mark.parametrize("password_lower_case_chars", [True, False])
@pytest.mark.parametrize("password_upper_case_chars", [True, False])
@pytest.mark.parametrize("password_special_symbols", [True, False])
def test_generate_too_long_password(
    password_numbers,
    password_lower_case_chars,
    password_upper_case_chars,
    password_special_symbols,
):
    """
    Test for failed password generation.

    :param password_numbers: int
    :param password_lower_case_chars: bool
    :param password_upper_case_chars: bool
    :param password_special_symbols: bool
    :return:
    """
    with pytest.raises(GeneratePasswordError):
        generate_password(
            500,
            password_numbers,
            password_lower_case_chars,
            password_upper_case_chars,
            password_special_symbols,
        )
