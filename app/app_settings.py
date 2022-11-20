"""
Application Settings
"""
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    """
    This class provides the configuration for the application. It also
    provides the defaults for the configuration options.

    It loads automatically all environments variables and overrides the
    defaults.

    Docs: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=duplicate-code

    application_name: str = "Password Generator"
    application_description: str = (
        "A FastApi example project providing a password generator."
    )
    api_version: str = "1.0.0"
    api_major_version_path: str = "/v1"
    min_password_length: int = 6
    max_password_length: int = 200
    default_password_length: int = 10
    password_numbers: bool = True
    password_lower_case_chars: bool = True
    password_upper_case_chars: bool = True
    password_special_symbols: bool = True

    class Config:
        """
        This class configures the .env file to load via python-dotenv
        library.
        """

        env_file = ".env"


application_settings: ApplicationSettings = ApplicationSettings()
