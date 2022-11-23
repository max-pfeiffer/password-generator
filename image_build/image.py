"""Docker Image"""
from pathlib import Path
from typing import Optional

import docker
from docker.models.images import Image

from image_build.constants import IMAGE_NAME


class DockerImage:
    """Class for building a Docker Image"""

    # pylint: disable=too-few-public-methods

    def __init__(self, docker_client: docker.client):
        self.docker_client: docker.client = docker_client
        self.image_name: str = IMAGE_NAME
        self.image_tag: Optional[str] = None
        self.dockerfile_name: str = "Dockerfile"
        self.absolute_docker_image_directory_path: Path = (
            Path(__file__).parent.resolve().parent.resolve()
        )

    def build(self, version: str) -> Image:
        """Builds Docker Image

        :param version: str
        :return: Image
            The Docker Image
        """
        tag: str = f"{self.image_name}:{version}"

        image: Image = self.docker_client.images.build(
            path=str(self.absolute_docker_image_directory_path),
            dockerfile=self.dockerfile_name,
            tag=tag,
        )[0]
        return image
