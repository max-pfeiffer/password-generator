"""
Tests for Application Configuration
"""
from app.app_settings import ApplicationSettings
from app.main import app, application_settings


def test_app_settings_defaults(monkeypatch):
    """
    Test for ApplicationSettings defaults

    :param monkeypatch:
    :return:
    """
    # pylint: disable=duplicate-code

    monkeypatch.delenv("DEFAULT_PASSWORD_LENGTH", raising=False)
    monkeypatch.delenv("PASSWORD_NUMBERS", raising=False)
    monkeypatch.delenv("PASSWORD_LOWER_CASE_CHARS", raising=False)
    monkeypatch.delenv("PASSWORD_UPPER_CASE_CHARS", raising=False)
    monkeypatch.delenv("PASSWORD_SPECIAL_SYMBOLS", raising=False)

    settings: ApplicationSettings = application_settings

    assert "Password Generator" == settings.application_name
    assert (
        "A FastApi example project providing a password generator."
        == settings.application_description
    )
    assert "1.0.0" == settings.api_version
    assert 6 == settings.min_password_length
    assert 200 == settings.max_password_length
    assert 10 == settings.default_password_length
    assert settings.password_numbers
    assert settings.password_lower_case_chars
    assert settings.password_upper_case_chars
    assert settings.password_special_symbols


def test_app_settings_config(monkeypatch):
    """
    Test for ApplicationSettings overrides

    :param monkeypatch:
    :return:
    """
    # pylint: disable=duplicate-code

    monkeypatch.setenv("DEFAULT_PASSWORD_LENGTH", "15")
    monkeypatch.setenv("PASSWORD_NUMBERS", "0")
    monkeypatch.setenv("PASSWORD_LOWER_CASE_CHARS", "0")
    monkeypatch.setenv("PASSWORD_UPPER_CASE_CHARS", "0")
    monkeypatch.setenv("PASSWORD_SPECIAL_SYMBOLS", "0")

    settings: ApplicationSettings = application_settings

    assert 15 == settings.default_password_length
    assert not settings.password_numbers
    assert not settings.password_lower_case_chars
    assert not settings.password_upper_case_chars
    assert not settings.password_special_symbols


def test_fastapi_app_config():
    """
    Test for Fast API application settings
    :return:
    """
    # pylint: disable=duplicate-code

    fastapi_application: app = app

    assert "Password Generator" == fastapi_application.title
    assert (
        "A FastApi example project providing a password generator."
        == fastapi_application.description
    )
    assert "1.0.0" == fastapi_application.version
