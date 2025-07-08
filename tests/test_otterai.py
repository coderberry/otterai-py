import json
import os
import shutil
import time
from datetime import datetime
from pprint import pprint
from unittest.mock import Mock

import pytest
import requests
from dotenv import load_dotenv
from tenacity import RetryError

from otterai.otterai import OtterAI, OtterAIException
from otterai.models import ContactsResponse, FoldersResponse, MentionCandidatesResponse

load_dotenv(dotenv_path=".env")

TEST_SPEECH_OTID = os.getenv("TEST_OTTERAI_SPEECH_OTID")
assert TEST_SPEECH_OTID is not None, "TEST_OTTERAI_SPEECH_OTID is not set in .env"

DOWNLOAD_DIR = "test_downloads"


# Login Tests
def test_login(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] == requests.codes.ok


def test_login_invalid_username(otterai_instance):
    response = otterai_instance.login("invalid_username", os.getenv("OTTERAI_PASSWORD"))
    assert response["status"] != requests.codes.ok


def test_login_invalid_password(otterai_instance):
    response = otterai_instance.login(os.getenv("OTTERAI_USERNAME"), "invalid_password")
    assert response["status"] != requests.codes.ok


def test_login_invalid_credentials(otterai_instance):
    response = otterai_instance.login("invalid_username", "invalid_password")
    assert response["status"] != requests.codes.ok


def test_login_already_logged_in(authenticated_otterai_instance, capsys):
    assert (
        authenticated_otterai_instance._userid is not None
    ), "User should already be logged in"

    response = authenticated_otterai_instance.login(
        os.getenv("OTTERAI_USERNAME"), os.getenv("OTTERAI_PASSWORD")
    )

    assert response["status"] == requests.codes.ok
    assert response["data"]["userid"] == authenticated_otterai_instance._userid


# User ID Validation Tests
def test_is_userid_none(otterai_instance):
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_empty(otterai_instance):
    otterai_instance._userid = ""
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_valid(otterai_instance):
    otterai_instance._userid = "123456"
    assert otterai_instance._is_userid_invalid() is False


# Response Handling Tests
def test_handle_response_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.return_value = {"key": "value"}

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {"key": "value"}


def test_handle_response_no_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.side_effect = ValueError  # Simulate no JSON
    mock_response.text = "Some plain text"

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {}


def test_handle_response_with_data(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = 201
    additional_data = {"extra": "info"}

    result = otterai_instance._handle_response(mock_response, data=additional_data)
    assert result["status"] == 201
    assert result["data"] == additional_data


# Authenticated Tests


def test_get_user(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_user()
    assert response["status"] == requests.codes.ok


def test_set_speech_title(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID

    response = authenticated_otterai_instance.get_speech(otid)

    title_after = f"Hello, World! {datetime.now()}"

    response = authenticated_otterai_instance.set_speech_title(
        otid=otid,
        title=title_after,
    )

    response = authenticated_otterai_instance.get_speech(otid)
    assert response["data"]["speech"]["title"] == title_after


def test_set_speech_title_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.set_speech_title("otid", "New Title")


def test_get_speakers_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speakers()
    assert result["status"] == requests.codes.ok
    assert "speakers" in result["data"]
    assert isinstance(result["data"]["speakers"], list)


def test_get_speakers_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speakers()


def test_get_speeches_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speeches()


def test_get_speeches_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speeches()
    assert result["status"] == requests.codes.ok
    assert "speeches" in result["data"]
    assert isinstance(result["data"]["speeches"], list)


def test_get_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID
    response = authenticated_otterai_instance.get_speech(otid)
    assert response["status"] == requests.codes.ok
    assert "speech" in response["data"]
    assert response["data"]["speech"]["otid"] == otid


def test_get_speech_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speech("invalid_otid")


def test_query_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID
    query = "test query"
    response = authenticated_otterai_instance.query_speech(query, otid)
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert isinstance(response["data"], dict)


def test_get_notification_settings(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_notification_settings()
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert isinstance(response["data"], dict)


def test_list_groups_success(authenticated_otterai_instance):
    response = authenticated_otterai_instance.list_groups()
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert "groups" in response["data"]


def test_list_groups_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.list_groups()


def test_get_folders_success(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_folders()
    assert "data" in response
    assert "folders" in response["data"]


def test_get_folders_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_folders()


def test_download_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID

    file_extension = "txt"

    file_base_name = os.path.join(DOWNLOAD_DIR, f"{otid}")
    file_full_name = f"{file_base_name}.{file_extension}"

    if os.path.exists(file_base_name):
        os.remove(file_base_name)

    response = authenticated_otterai_instance.download_speech(
        otid=otid,
        name=file_base_name,
        fileformat=file_extension,
    )

    print(f"Response: {response}")
    print(f"Expected file path: {file_base_name}")

    assert response["status"] == requests.codes.ok, "Download request failed"
    assert os.path.exists(file_full_name), "File not downloaded"

    os.remove(file_full_name)


def test_download_speech_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.download_speech("invalid_otid", name="invalid_file")


def test_download_speech_failure(authenticated_otterai_instance, monkeypatch):
    otid = TEST_SPEECH_OTID
    file_extension = "txt"
    file_name = f"failed_download.{file_extension}"

    def mock_failed_request(*args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 500  # Simulate server error
        mock_response.ok = False
        return mock_response

    monkeypatch.setattr(
        authenticated_otterai_instance, "_make_request", mock_failed_request
    )

    with pytest.raises(
        OtterAIException,
        match=f"Got response status 500 when attempting to download {otid}",
    ):
        authenticated_otterai_instance.download_speech(
            otid=otid, name=file_name, fileformat=file_extension
        )


# Structured Data Tests (Phase 2)
def test_get_contacts_structured_success(authenticated_otterai_instance):
    """Test get_contacts_structured returns structured ContactsResponse."""
    response = authenticated_otterai_instance.get_contacts_structured()
    assert isinstance(response, ContactsResponse)
    assert response.status == "OK"
    assert hasattr(response, "contacts")
    assert hasattr(response, "user_id")
    assert hasattr(response, "last_modified_at")
    assert isinstance(response.contacts, list)


def test_get_contacts_structured_invalid_userid(otterai_instance):
    """Test get_contacts_structured raises exception with invalid userid."""
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_contacts_structured()


def test_get_folders_structured_success(authenticated_otterai_instance):
    """Test get_folders_structured returns structured FoldersResponse."""
    response = authenticated_otterai_instance.get_folders_structured()
    assert isinstance(response, FoldersResponse)
    assert response.status == "OK"
    assert hasattr(response, "folders")
    assert hasattr(response, "last_modified_at")
    assert isinstance(response.folders, list)


def test_get_folders_structured_invalid_userid(otterai_instance):
    """Test get_folders_structured raises exception with invalid userid."""
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_folders_structured()


def test_get_speech_mention_candidates_structured_success(
    authenticated_otterai_instance,
):
    """Test get_speech_mention_candidates_structured returns structured MentionCandidatesResponse."""
    otid = TEST_SPEECH_OTID
    response = authenticated_otterai_instance.get_speech_mention_candidates_structured(
        otid
    )
    assert isinstance(response, MentionCandidatesResponse)
    assert response.status == "OK"
    assert hasattr(response, "mention_candidates")
    assert isinstance(response.mention_candidates, list)


# Unit tests for structured models
def test_contacts_response_model():
    """Test ContactsResponse model validation."""
    data = {
        "status": "OK",
        "contacts": [
            {
                "id": 476734168,
                "type": "contact",
                "first_name": "Andres",
                "last_name": "Granda",
                "email": "agranda@giraffemediagroup.com",
                "phone_number": None,
                "avatar_url": None,
            }
        ],
        "user_id": 25462508,
        "last_modified_at": 1752002672,
    }
    response = ContactsResponse(**data)
    assert response.status == "OK"
    assert len(response.contacts) == 1
    assert response.contacts[0].first_name == "Andres"
    assert response.contacts[0].last_name == "Granda"
    assert response.contacts[0].email == "agranda@giraffemediagroup.com"


def test_folders_response_model():
    """Test FoldersResponse model validation."""
    data = {
        "status": "OK",
        "folders": [
            {
                "id": 1702429,
                "created_at": 1751982020,
                "last_modified_at": 1751982020,
                "deleted_at": None,
                "last_speech_added_at": None,
                "speech_count": 0,
                "user_id": 25462508,
                "folder_name": "Video podcasts",
            }
        ],
        "last_modified_at": 1752002685,
    }
    response = FoldersResponse(**data)
    assert response.status == "OK"
    assert len(response.folders) == 1
    assert response.folders[0].folder_name == "Video podcasts"
    assert response.folders[0].speech_count == 0


def test_mention_candidates_response_model():
    """Test MentionCandidatesResponse model validation."""
    data = {
        "status": "OK",
        "mention_candidates": [
            {
                "id": 25462508,
                "name": "Eric Berry",
                "email": "eric@berrydev.ai",
                "first_name": "Eric",
                "last_name": "Berry",
                "avatar_url": "https://profile.otter.ai/AMEQ3WM67T2EEP2Q/AMEQ3WM67T2EET2E",
                "permission": "owner",
            }
        ],
    }
    response = MentionCandidatesResponse(**data)
    assert response.status == "OK"
    assert len(response.mention_candidates) == 1
    assert response.mention_candidates[0].name == "Eric Berry"
    assert response.mention_candidates[0].permission == "owner"
