"""
Fixtures for Application Tests
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """
    Test client fixture
    :return: TestClient
    """
    return TestClient(app)
