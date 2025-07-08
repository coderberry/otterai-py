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

from otterai.models import (AbstractSummaryResponse,  # Phase 4 models
                            ActionItemsResponse, ContactsResponse,
                            FoldersResponse, GroupsResponse,
                            MentionCandidatesResponse, SpeakersResponse,
                            SpeechTemplatesResponse)
from otterai.otterai import OtterAI, OtterAIException

load_dotenv(dotenv_path=".env")

TEST_SPEECH_OTID = os.getenv("TEST_OTTERAI_SPEECH_OTID")
assert TEST_SPEECH_OTID is not None, "TEST_OTTERAI_SPEECH_OTID is not set in .env"

DOWNLOAD_DIR = "test_downloads"


# Login Tests
@pytest.mark.integration
def test_login(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] == requests.codes.ok


@pytest.mark.integration
def test_login_invalid_username(otterai_instance):
    response = otterai_instance.login("invalid_username", os.getenv("OTTERAI_PASSWORD"))
    assert response["status"] != requests.codes.ok


@pytest.mark.integration
def test_login_invalid_password(otterai_instance):
    response = otterai_instance.login(os.getenv("OTTERAI_USERNAME"), "invalid_password")
    assert response["status"] != requests.codes.ok


@pytest.mark.integration
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
                "id": 123456789,
                "type": "contact",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone_number": None,
                "avatar_url": None,
            }
        ],
        "user_id": 987654321,
        "last_modified_at": 1700000000,
    }
    response = ContactsResponse(**data)
    assert response.status == "OK"
    assert len(response.contacts) == 1
    assert isinstance(response.contacts[0].first_name, str)
    assert isinstance(response.contacts[0].last_name, str)
    assert isinstance(response.contacts[0].email, str)
    assert "@" in response.contacts[0].email  # Basic email format check


def test_folders_response_model():
    """Test FoldersResponse model validation."""
    data = {
        "status": "OK",
        "folders": [
            {
                "id": 123456789,
                "created_at": 1700000000,
                "last_modified_at": 1700000000,
                "deleted_at": None,
                "last_speech_added_at": None,
                "speech_count": 0,
                "user_id": 987654321,
                "folder_name": "Test Folder",
            }
        ],
        "last_modified_at": 1700000000,
    }
    response = FoldersResponse(**data)
    assert response.status == "OK"
    assert len(response.folders) == 1
    assert isinstance(response.folders[0].folder_name, str)
    assert isinstance(response.folders[0].speech_count, int)
    assert response.folders[0].speech_count >= 0


def test_mention_candidates_response_model():
    """Test MentionCandidatesResponse model validation."""
    data = {
        "status": "OK",
        "mention_candidates": [
            {
                "id": 123456789,
                "name": "Test User",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "avatar_url": "https://profile.otter.ai/EXAMPLE123/EXAMPLE456",
                "permission": "owner",
            }
        ],
    }
    response = MentionCandidatesResponse(**data)
    assert response.status == "OK"
    assert len(response.mention_candidates) == 1
    assert isinstance(response.mention_candidates[0].name, str)
    assert isinstance(response.mention_candidates[0].permission, str)
    assert "@" in response.mention_candidates[0].email


# Phase 3: Complex Models Tests (TEMP.md endpoints)
def test_list_groups_structured_success(authenticated_otterai_instance):
    """Test list_groups_structured returns structured GroupsResponse for TEMP.md endpoint."""
    response = authenticated_otterai_instance.list_groups_structured()
    assert isinstance(response, GroupsResponse)
    assert response.status == "OK"
    assert hasattr(response, "groups")
    assert hasattr(response, "last_load_ts")
    assert isinstance(response.groups, list)


def test_list_groups_structured_invalid_userid(otterai_instance):
    """Test list_groups_structured raises exception with invalid userid."""
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.list_groups_structured()


def test_get_speakers_structured_success(authenticated_otterai_instance):
    """Test get_speakers_structured returns structured SpeakersResponse for TEMP.md endpoint."""
    response = authenticated_otterai_instance.get_speakers_structured()
    assert isinstance(response, SpeakersResponse)
    assert response.status == "OK"
    assert hasattr(response, "speakers")
    assert isinstance(response.speakers, list)


def test_get_speakers_structured_invalid_userid(otterai_instance):
    """Test get_speakers_structured raises exception with invalid userid."""
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speakers_structured()


def test_groups_response_model():
    """Test GroupsResponse model validation with generic test data."""
    data = {
        "status": "OK",
        "groups": [
            {
                "id": 123456789,
                "created_at": 1700000000,
                "last_modified_at": 1700000000,
                "name": "Test Group",
                "is_deleted": False,
                "is_public": False,
                "has_left": False,
                "public_name": None,
                "description": None,
                "new_unread_msg_count": 0,
                "bolding": False,
                "latest_message_time": "2024-01-01 12:00:00",
                "last_group_visit_time": "2024-01-01 12:00:00",
                "owner": {
                    "id": 111111111,
                    "name": "Test Owner",
                    "email": "owner@example.com",
                    "first_name": "Test",
                    "last_name": "Owner",
                    "avatar_url": None,
                },
                "cover_photo_url": None,
                "avatar_url": None,
                "open_post": True,
                "open_invite": True,
                "can_post": True,
                "member_count": 5,
                "dm_name": None,
                "is_dm_visible": False,
                "first_member": {
                    "id": 222222222,
                    "name": "Test Member",
                    "email": "member@example.com",
                    "first_name": "Test",
                    "last_name": "Member",
                    "avatar_url": None,
                },
                "has_live_speech": False,
                "is_autoshare_group": False,
                "discoverability": "private",
                "workspace_id": None,
            }
        ],
        "last_load_ts": 1700000000,
    }
    response = GroupsResponse(**data)
    assert response.status == "OK"
    assert len(response.groups) == 1
    assert isinstance(response.groups[0].name, str)
    assert isinstance(response.groups[0].owner.name, str)
    assert isinstance(response.groups[0].first_member.name, str)
    assert isinstance(response.groups[0].member_count, int)
    assert response.groups[0].member_count > 0
    assert isinstance(response.groups[0].discoverability, str)


def test_speakers_response_model():
    """Test SpeakersResponse model validation with generic test data."""
    data = {
        "status": "OK",
        "speakers": [
            {
                "id": 123456789,
                "created_at": "2024-01-01 12:00:00",
                "speaker_name": "Test Speaker 1",
                "url": None,
                "user_id": 111111111,
                "self_speaker": True,
                "speaker_email": None,
                "owner": {
                    "id": 111111111,
                    "name": "Test User 1",
                    "email": "user1@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
            },
            {
                "id": 987654321,
                "created_at": "2024-01-01 12:00:00",
                "speaker_name": "Test Speaker 2",
                "url": "https://s3.us-west-2.amazonaws.com/example-bucket/example-key",
                "user_id": 222222222,
                "self_speaker": True,
                "speaker_email": "user2@example.com",
                "owner": {
                    "id": 222222222,
                    "name": "Test User 2",
                    "email": "user2@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
            },
        ],
    }
    response = SpeakersResponse(**data)
    assert response.status == "OK"
    assert len(response.speakers) == 2
    assert isinstance(response.speakers[0].speaker_name, str)
    assert isinstance(response.speakers[0].owner.name, str)
    assert isinstance(response.speakers[1].speaker_name, str)
    assert isinstance(response.speakers[1].speaker_email, str)
    assert response.speakers[1].url is not None


def test_groups_response_model_optional_fields():
    """Test Group model handles optional fields correctly."""
    data = {
        "status": "OK",
        "groups": [
            {
                "id": 123456789,
                "created_at": 1700000000,
                "last_modified_at": 1700000000,
                "name": "Test Group",
                "is_deleted": False,
                "is_public": False,
                "has_left": False,
                "public_name": None,
                "description": None,
                "new_unread_msg_count": 0,
                "bolding": False,
                "latest_message_time": "2024-01-01 12:00:00",
                "last_group_visit_time": "2024-01-01 12:00:00",
                "owner": {
                    "id": 111111111,
                    "name": "Test User",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
                "cover_photo_url": None,
                "avatar_url": None,
                "open_post": True,
                "open_invite": True,
                "can_post": True,
                "member_count": 1,
                "dm_name": None,
                "is_dm_visible": False,
                "first_member": {
                    "id": 111111111,
                    "name": "Test User",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
                "has_live_speech": False,
                "is_autoshare_group": False,
                "discoverability": "workspace",
                "workspace_id": 999999999,
            }
        ],
        "last_load_ts": 1700000000,
    }
    response = GroupsResponse(**data)
    assert response.status == "OK"
    assert isinstance(response.groups[0].workspace_id, int)
    assert response.groups[0].public_name is None
    assert response.groups[0].description is None
    assert isinstance(response.groups[0].discoverability, str)


def test_speakers_response_model_optional_fields():
    """Test Speaker model handles optional fields correctly."""
    data = {
        "status": "OK",
        "speakers": [
            {
                "id": 123456789,
                "created_at": "2024-01-01 12:00:00",
                "speaker_name": "Test Speaker",
                "url": None,
                "user_id": 111111111,
                "self_speaker": True,
                "speaker_email": None,
                "owner": {
                    "id": 111111111,
                    "name": "Test User",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
            }
        ],
    }
    response = SpeakersResponse(**data)
    assert response.status == "OK"
    assert response.speakers[0].url is None
    assert response.speakers[0].speaker_email is None
    assert response.speakers[0].owner.avatar_url is None


# Phase 4: Speech Templates and Action Items Tests
def test_get_speech_templates_structured_success(authenticated_otterai_instance):
    """Test get_speech_templates_structured returns structured SpeechTemplatesResponse."""
    response = authenticated_otterai_instance.get_speech_templates_structured()
    assert isinstance(response, SpeechTemplatesResponse)
    assert response.status == "OK"
    assert hasattr(response, "data")
    assert hasattr(response.data, "permissions")
    assert hasattr(response.data, "templates")
    assert isinstance(response.data.templates, list)


def test_get_speech_action_items_structured_success(authenticated_otterai_instance):
    """Test get_speech_action_items_structured returns structured ActionItemsResponse."""
    otid = TEST_SPEECH_OTID
    response = authenticated_otterai_instance.get_speech_action_items_structured(otid)
    assert isinstance(response, ActionItemsResponse)
    assert response.status == "OK"
    assert hasattr(response, "process_status")
    assert hasattr(response, "speech_action_items")
    assert isinstance(response.speech_action_items, list)


def test_get_abstract_summary_structured_success(authenticated_otterai_instance):
    """Test get_abstract_summary_structured returns structured AbstractSummaryResponse."""
    otid = TEST_SPEECH_OTID
    response = authenticated_otterai_instance.get_abstract_summary_structured(otid)
    assert isinstance(response, AbstractSummaryResponse)
    assert response.status == "OK"
    assert hasattr(response, "process_status")
    assert hasattr(response, "abstract_summary")
    assert isinstance(response.abstract_summary.short_summary, str)


# Unit tests for Phase 4 models
def test_speech_templates_response_model():
    """Test SpeechTemplatesResponse model validation with generic test data."""
    data = {
        "status": "OK",
        "code": 200,
        "data": {
            "permissions": {
                "can_create_personal_templates": True,
                "can_create_workspace_templates": True,
            },
            "templates": [
                {
                    "id": 123456789,
                    "name": "Test Template",
                    "is_personal_template": False,
                    "is_customized": False,
                    "created_by": {"id": None, "name": "Test System"},
                    "base_template_type": "general",
                    "permissions": {
                        "can_edit": True,
                        "can_delete": False,
                        "can_clone": True,
                        "can_view": True,
                        "can_apply": True,
                    },
                }
            ],
        },
    }
    response = SpeechTemplatesResponse(**data)
    assert response.status == "OK"
    assert response.data.permissions.can_create_personal_templates is True
    assert len(response.data.templates) == 1
    assert isinstance(response.data.templates[0].name, str)
    assert isinstance(response.data.templates[0].permissions.can_edit, bool)
    assert response.data.templates[0].created_by.id is None


def test_action_items_response_model():
    """Test ActionItemsResponse model validation with generic test data."""
    data = {
        "status": "OK",
        "process_status": "finished",
        "speech_action_items": [
            {
                "id": 123456789,
                "created_at": 1700000000,
                "last_modified_at": 1700000000,
                "start_msec": 1000,
                "end_msec": None,
                "speech_otid": "test_otid_123",
                "creator": None,
                "text": "Test action item",
                "assignee": {
                    "id": 111111111,
                    "name": "Test User",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "avatar_url": None,
                },
                "assigner": None,
                "completed": False,
                "uuid": "test-uuid-123",
                "order": "test123",
                "deleted_at": None,
                "process_id": 987654321,
            }
        ],
    }
    response = ActionItemsResponse(**data)
    assert response.status == "OK"
    assert response.process_status == "finished"
    assert len(response.speech_action_items) == 1
    assert isinstance(response.speech_action_items[0].text, str)
    assert response.speech_action_items[0].assignee.name == "Test User"
    assert response.speech_action_items[0].end_msec is None
    assert response.speech_action_items[0].completed is False


def test_abstract_summary_response_model():
    """Test AbstractSummaryResponse model validation with generic test data."""
    data = {
        "status": "OK",
        "process_status": "finished",
        "abstract_summary": {
            "id": 123456789,
            "status": "completed",
            "speech_otid": "test_otid_123",
            "items": [],
            "short_summary": "This is a test summary of the speech content.",
        },
    }
    response = AbstractSummaryResponse(**data)
    assert response.status == "OK"
    assert response.process_status == "finished"
    assert isinstance(response.abstract_summary.short_summary, str)
    assert response.abstract_summary.status == "completed"
    assert isinstance(response.abstract_summary.items, list)
    assert len(response.abstract_summary.items) == 0


def test_speech_templates_response_model_optional_fields():
    """Test SpeechTemplate model handles optional fields correctly."""
    data = {
        "status": "OK",
        "code": 200,
        "data": {
            "permissions": {
                "can_create_personal_templates": False,
                "can_create_workspace_templates": False,
            },
            "templates": [
                {
                    "id": 123456789,
                    "name": "Test Template",
                    "is_personal_template": True,
                    "is_customized": True,
                    "created_by": {"id": 111111111, "name": "Test Creator"},
                    "base_template_type": "custom",
                    "permissions": {
                        "can_edit": False,
                        "can_delete": True,
                        "can_clone": False,
                        "can_view": True,
                        "can_apply": False,
                    },
                }
            ],
        },
    }
    response = SpeechTemplatesResponse(**data)
    assert response.status == "OK"
    assert response.data.permissions.can_create_personal_templates is False
    assert response.data.templates[0].is_personal_template is True
    assert response.data.templates[0].created_by.id == 111111111
