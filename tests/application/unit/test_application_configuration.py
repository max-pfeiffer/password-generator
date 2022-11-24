"""Tests for Application Configuration"""
# pylint: disable=duplicate-code

from app.app_settings import ApplicationSettings
from app.main import app, application_settings


def test_app_settings_defaults():
    """
    Test for ApplicationSettings defaults

    :param monkeypatch:
    :return:
    """
    settings: ApplicationSettings = ApplicationSettings()

    assert "Password Generator" == settings.application_name
    assert (
        "A FastApi example project providing a password generator."
        == settings.application_description
    )
    assert "1.0.0" == application_settings.api_version
    assert application_settings.min_password_length == 6
    assert application_settings.max_password_length == 200


def test_app_settings_config(monkeypatch):
    """
    Test for ApplicationSettings overrides

    :param monkeypatch:
    :return:
    """
    # This test works because actual environment variables have a higher
    # loading priority in pydantic BaseSettings.
    # See: https://pydantic-docs.helpmanual.io/usage/settings/#field-value-priority
    monkeypatch.setenv("DEFAULT_PASSWORD_LENGTH", "15")
    monkeypatch.setenv("PASSWORD_NUMBERS", "0")
    monkeypatch.setenv("PASSWORD_LOWER_CASE_CHARS", "0")
    monkeypatch.setenv("PASSWORD_UPPER_CASE_CHARS", "0")
    monkeypatch.setenv("PASSWORD_SPECIAL_SYMBOLS", "0")

    settings: ApplicationSettings = ApplicationSettings()

    assert settings.default_password_length == 15
    assert not settings.password_numbers
    assert not settings.password_lower_case_chars
    assert not settings.password_upper_case_chars
    assert not settings.password_special_symbols


def test_fastapi_app_config():
    """
    Test for Fast API application settings
    :return:
    """
    fastapi_application: app = app

    assert "Password Generator" == fastapi_application.title
    assert (
        "A FastApi example project providing a password generator."
        == fastapi_application.description
    )
    assert "1.0.0" == fastapi_application.version
