"""Script for publishing the Docker image on Docker Hub"""
# pylint: disable=duplicate-code

import os

import docker
from dotenv import load_dotenv

from image_build.constants import IMAGE_NAME
from image_build.image import DockerImage

environment_variables_loaded: bool = load_dotenv()

docker_hub_username: str = os.getenv("DOCKER_HUB_USERNAME")
docker_hub_password: str = os.getenv("DOCKER_HUB_PASSWORD")
version_tag: str = os.getenv("GIT_TAG_NAME")


def publish_docker_image() -> None:
    """Publishes the Docker image

    :return:
    """
    docker_client: docker.client = docker.from_env()

    new_image: DockerImage = DockerImage(docker_client)

    # Delete all old images with the same name
    for old_image in docker_client.images.list(new_image.image_name):
        for tag in old_image.tags:
            docker_client.images.remove(tag, force=True)

    new_image.build(version_tag)

    # Log into Docker account
    # docker_client.login(
    #     username=docker_hub_username, password=docker_hub_password
    # )

    # Push the image to Docker Hub
    for line in docker_client.images.push(
        IMAGE_NAME,
        tag=new_image.image_tag,
        stream=True,
        decode=True,
    ):
        print(line)

    # Clean up
    docker_client.close()


if __name__ == "__main__":
    publish_docker_image()
