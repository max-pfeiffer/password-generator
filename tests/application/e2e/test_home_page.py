"""Test for Home Page"""
from httpx import Response
from fastapi import status


def test_home_page(test_client):
    """Test for Home Page

    :param test_client:
    :return:
    """
    response: Response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
