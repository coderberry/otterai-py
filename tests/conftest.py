"""
Pytest configuration and fixtures for OtterAI tests.
"""

import os
import warnings

import pytest
import requests
from dotenv import load_dotenv

from otterai.otterai import OtterAI

load_dotenv(dotenv_path=".env")


def pytest_configure(config):
    """Configure pytest to handle integration test warnings."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests that hit real API"
    )
    config.addinivalue_line("markers", "slow: marks tests as slow running")


def pytest_collection_modifyitems(config, items):
    """Add markers to tests and warn about running integration tests together."""
    integration_tests = []
    for item in items:
        if "authenticated_otterai_instance" in item.fixturenames:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)
            integration_tests.append(item.name)

    # Warn if multiple integration tests are being run
    if len(integration_tests) > 1:
        warnings.warn(
            f"\n⚠️  WARNING: Running {len(integration_tests)} integration tests together!\n"
            f"This will likely result in 429 rate limit errors from the Otter.ai API.\n\n"
            f"Better alternatives:\n"
            f"  • Run unit tests only: pytest tests/ -m 'not integration'\n"
            f"  • Run one integration test: pytest tests/test_otterai.py::test_get_user -s\n"
            f"  • Run with delay: pytest tests/ -m integration --tb=short -x\n"
            f"  • Use mocked tests for CI/CD\n\n"
            f"Integration tests found: {integration_tests}\n",
            UserWarning,
            stacklevel=2,
        )


@pytest.fixture
def otterai_instance():
    """Create a non-authenticated OtterAI instance for unit tests."""
    return OtterAI()


@pytest.fixture
def authenticated_otterai_instance():
    """Create an authenticated OtterAI instance for integration tests."""
    otter = OtterAI()
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")

    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otter.login(username, password)
    assert response["status"] == requests.codes.ok, "Failed to log in"

    return otter


@pytest.fixture(scope="module", autouse=True)
def setup_download_dir():
    """Set up and clean up download directory for tests."""
    download_dir = "test_downloads"
    os.makedirs(download_dir, exist_ok=True)
    yield
    # Uncomment to clean up after tests
    # shutil.rmtree(download_dir)
