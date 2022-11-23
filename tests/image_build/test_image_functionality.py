"""Tests for Docker Image Functionality"""
# pylint: disable=duplicate-code

from time import sleep
from uuid import uuid4

import docker
import pytest
from fastapi import status
from furl import furl
from httpx import get, Response

from app.app_settings import application_settings
from app.models import Password
from tests.image_build.constants import (
    APPLICATION_SERVER_PORT,
    EXPOSED_CONTAINER_PORT,
    SLEEP_TIME,
)


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_image_functionality(
    docker_client: docker.client,
    docker_image: str,
    cleaned_up_test_container: str,
) -> None:
    """Testing the image functionality

    :param docker_client: docker.client
    :param docker_image: str
    :param cleaned_up_test_container: str
    :return:
    """
    docker_client.containers.run(
        docker_image,
        name=cleaned_up_test_container,
        ports={APPLICATION_SERVER_PORT: EXPOSED_CONTAINER_PORT},
        detach=True,
    )

    sleep(SLEEP_TIME)

    furl_item: furl = furl("http://127.0.0.1")
    furl_item.port = EXPOSED_CONTAINER_PORT
    furl_item.path /= application_settings.api_major_version_path
    furl_item.path /= "passwords"
    furl_item.args["password_length"] = 8
    furl_item.args["password_numbers"] = True
    furl_item.args["password_lower_case_chars"] = False
    furl_item.args["password_upper_case_chars"] = True
    furl_item.args["password_special_symbols"] = False
    url: str = furl_item.url

    response: Response = get(url)
    password: Password = Password.parse_obj(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert len(password.password) == 8
