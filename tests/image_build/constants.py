"""Constants for Tests"""
# pylint: disable=duplicate-code

SLEEP_TIME: float = 3.0
APPLICATION_SERVER_PORT: str = "8000"
EXPOSED_CONTAINER_PORT: str = "8000"

DEFAULT_UVICORN_CONFIG: dict[str, str] = {
    "workers": "1",
    "host": "0.0.0.0",
    "port": APPLICATION_SERVER_PORT,
}
