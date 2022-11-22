"""Application Settings

All settings for the application.
"""
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    """
    This class provides the configuration for the application. It also
    provides the defaults for the configuration options.

    It loads automatically all environments variables and overrides the
    defaults.

    This way we save a lot of boilerplate code. This is why I choose to use it.

    Docs: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=duplicate-code

    application_name: str = "Password Generator"
    application_description: str = (
        "A FastApi example project providing a password generator."
    )
    api_version: str = "1.0.0"
    api_major_version_path: str = "/api/v1"
    # I took the minimum password length from NIST recommendation. This is one
    # of the very few official recommendations:
    # https://pages.nist.gov/800-63-3/sp800-63b.html
    # See section 5.1.1.1: for machine generated passwords a minimum length of
    # six chars is recommended.
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

        # Configuration for loading the environment variables. Priority:
        # 1. From .env file for local development
        # 2. From /run/secrets/env_file when run with docker compose locally
        #    (.env is configured as Docker secret)
        env_file = ".env", "/run/secrets/env_file"


application_settings: ApplicationSettings = ApplicationSettings()
