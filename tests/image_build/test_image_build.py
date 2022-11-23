"""Tests for Docker Image Build"""
# pylint: disable=duplicate-code

from time import sleep
from uuid import uuid4

import docker
import pytest
from docker.models.containers import Container
from fastapi import status
from httpx import get, Response

from tests.image_build.constants import (
    APPLICATION_SERVER_PORT,
    EXPOSED_CONTAINER_PORT,
    SLEEP_TIME,
    DEFAULT_UVICORN_CONFIG,
)
from tests.image_build.utils import get_uvicorn_config


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_image_build(
    docker_client: docker.client,
    docker_image: str,
    cleaned_up_test_container: str,
) -> None:
    """Testing the image build

    :param docker_client: docker.client
    :param docker_image: str
    :param cleaned_up_test_container: str
    :return:
    """

    def verify_configuration(config_data: dict[str, str]):
        assert config_data["workers"] == DEFAULT_UVICORN_CONFIG["workers"]
        assert config_data["host"] == DEFAULT_UVICORN_CONFIG["host"]
        assert config_data["port"] == DEFAULT_UVICORN_CONFIG["port"]

        response: Response = get(f"http://127.0.0.1:{EXPOSED_CONTAINER_PORT}")
        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY

    test_container: Container = docker_client.containers.run(
        docker_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    )

    sleep(SLEEP_TIME)

    # Verify configuration
    config_data: dict[str, str] = get_uvicorn_config(test_container)
    verify_configuration(config_data)

    # Test restarting the container
    test_container.stop()
    test_container.start()
    sleep(SLEEP_TIME)
    verify_configuration(config_data)
