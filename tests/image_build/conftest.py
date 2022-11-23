"""Fixtures for Testing the Docker Image Build"""
# pylint: disable=redefined-outer-name
# pylint: disable=duplicate-code

from random import randrange

import docker
import pytest
from docker.models.images import Image
from semver import VersionInfo

from image_build.image import DockerImage


@pytest.fixture(scope="session")
def docker_client() -> docker.client:
    """Provides Docker client

    :return: docker.client
        Docker client
    """
    return docker.client.from_env()


@pytest.fixture(scope="session")
def version() -> str:
    """Provides a semantic version string

    :return: str
        Semantic version string
    """
    # Using semver here is a bit of an overkill but convenient and explicit
    version_info: VersionInfo = VersionInfo(
        major=randrange(100), minor=randrange(100), patch=randrange(100)
    )
    version_string: str = str(version_info)
    return version_string


@pytest.fixture(scope="session")
def docker_image(docker_client: docker.client, version: str) -> str:
    """Provides the Docker image for tests

    :param docker_client:
    :param version:
    :return: str
        The image tag for the image
    """
    docker_image: Image = DockerImage(docker_client).build(version)
    image_tag: str = docker_image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def cleaned_up_test_container(docker_client: docker.client, request) -> None:
    """This fixture for Docker context clean up

    This fixture cleans up the Docker context after the tests are run.
    It's scoped to the test session because there is only this one image
    used in tests.

    :param docker_client:
    :param request:
    :return:
    """
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
