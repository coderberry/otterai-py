"""
Mock API response tests for OtterAI Python client.

These tests use generic, non-PII mock data based on the sample API responses
to ensure comprehensive coverage without exposing any personal information.
"""

import json
from unittest.mock import Mock, patch

import pytest

from otterai.models import (
    AbstractSummaryResponse,
    ActionItemsResponse,
    AvailableSpeechesResponse,
    ContactsResponse,
    FoldersResponse,
    GroupsResponse,
    MentionCandidatesResponse,
    SpeakersResponse,
    SpeechResponse,
    SpeechTemplatesResponse,
)
from otterai.otterai import OtterAI, OtterAIException


class TestMockContactsAPI:
    """Test contacts API with mock data."""

    def test_contacts_structured_success(self):
        """Test successful contacts retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "contacts": [
                {
                    "id": 1001,
                    "type": "contact",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone_number": None,
                    "avatar_url": None,
                },
                {
                    "id": 1002,
                    "type": "contact",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@company.com",
                    "phone_number": "+1234567890",
                    "avatar_url": "https://example.com/avatar2.png",
                },
            ],
            "user_id": 12345,
            "last_modified_at": 1640995200,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_contacts_structured()

            assert isinstance(result, ContactsResponse)
            assert result.status == "OK"
            assert len(result.contacts) == 2
            assert result.user_id == 12345
            assert result.contacts[0].first_name == "John"
            assert result.contacts[0].last_name == "Doe"
            assert result.contacts[1].phone_number == "+1234567890"

    def test_contacts_structured_failure(self):
        """Test contacts API failure handling."""
        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            with pytest.raises(OtterAIException, match="Failed to get contacts: 400"):
                client.get_contacts_structured()

    def test_contacts_structured_invalid_userid(self):
        """Test contacts API with invalid userid."""
        client = OtterAI()
        client._userid = None

        with pytest.raises(OtterAIException, match="userid is invalid"):
            client.get_contacts_structured()


class TestMockFoldersAPI:
    """Test folders API with mock data."""

    def test_folders_structured_success(self):
        """Test successful folders retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "folders": [
                {
                    "id": 2001,
                    "created_at": 1640995200,
                    "last_modified_at": 1640995200,
                    "deleted_at": None,
                    "last_speech_added_at": None,
                    "speech_count": 0,
                    "user_id": 12345,
                    "folder_name": "Meeting Notes",
                },
                {
                    "id": 2002,
                    "created_at": 1640995300,
                    "last_modified_at": 1640995400,
                    "deleted_at": None,
                    "last_speech_added_at": 1640995500,
                    "speech_count": 5,
                    "user_id": 12345,
                    "folder_name": "Interviews",
                },
            ],
            "last_modified_at": 1640995600,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_folders_structured()

            assert isinstance(result, FoldersResponse)
            assert result.status == "OK"
            assert len(result.folders) == 2
            assert result.folders[0].folder_name == "Meeting Notes"
            assert result.folders[1].speech_count == 5


class TestMockGroupsAPI:
    """Test groups API with mock data."""

    def test_groups_structured_success(self):
        """Test successful groups retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "groups": [
                {
                    "id": 3001,
                    "created_at": 1640995200,
                    "last_modified_at": 1640995300,
                    "name": "Weekly Standup",
                    "is_deleted": False,
                    "is_public": False,
                    "has_left": False,
                    "public_name": None,
                    "description": None,
                    "new_unread_msg_count": 0,
                    "bolding": False,
                    "latest_message_time": "2024-01-01 10:00:00",
                    "last_group_visit_time": "2024-01-01 10:30:00",
                    "owner": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "avatar_url": "https://example.com/avatar.png",
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
                        "id": 12346,
                        "name": "Jane Smith",
                        "email": "jane.smith@company.com",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "avatar_url": "https://example.com/avatar2.png",
                    },
                    "has_live_speech": False,
                    "is_autoshare_group": False,
                    "discoverability": "private",
                    "workspace_id": None,
                },
            ],
            "last_load_ts": 1640995400,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.list_groups_structured()

            assert isinstance(result, GroupsResponse)
            assert result.status == "OK"
            assert len(result.groups) == 1
            assert result.groups[0].name == "Weekly Standup"
            assert result.groups[0].owner.name == "John Doe"
            assert result.groups[0].first_member.name == "Jane Smith"


class TestMockSpeakersAPI:
    """Test speakers API with mock data."""

    def test_speakers_structured_success(self):
        """Test successful speakers retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "speakers": [
                {
                    "id": 4001,
                    "created_at": "2024-01-01T10:00:00Z",
                    "speaker_name": "John Doe Speaker",
                    "url": "https://example.com/speaker1.wav",
                    "user_id": 12345,
                    "self_speaker": True,
                    "speaker_email": "john.doe@example.com",
                    "owner": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "avatar_url": "https://example.com/avatar.png",
                    },
                },
                {
                    "id": 4002,
                    "created_at": "2024-01-01T11:00:00Z",
                    "speaker_name": "Jane Smith Speaker",
                    "url": None,
                    "user_id": 12346,
                    "self_speaker": False,
                    "speaker_email": None,
                    "owner": {
                        "id": 12346,
                        "name": "Jane Smith",
                        "email": "jane.smith@company.com",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "avatar_url": None,
                    },
                },
            ],
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_speakers_structured()

            assert isinstance(result, SpeakersResponse)
            assert result.status == "OK"
            assert len(result.speakers) == 2
            assert result.speakers[0].speaker_name == "John Doe Speaker"
            assert result.speakers[0].self_speaker is True
            assert result.speakers[1].self_speaker is False


class TestMockMentionCandidatesAPI:
    """Test mention candidates API with mock data."""

    def test_mention_candidates_structured_success(self):
        """Test successful mention candidates retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "mention_candidates": [
                {
                    "id": 5001,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "avatar_url": "https://example.com/avatar.png",
                    "permission": "owner",
                },
                {
                    "id": 5002,
                    "name": "Jane Smith",
                    "email": "jane.smith@company.com",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "avatar_url": None,
                    "permission": "collaborator",
                },
            ],
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            result = client.get_speech_mention_candidates_structured("test_otid")

            assert isinstance(result, MentionCandidatesResponse)
            assert result.status == "OK"
            assert len(result.mention_candidates) == 2
            assert result.mention_candidates[0].permission == "owner"
            assert result.mention_candidates[1].permission == "collaborator"


class TestMockSpeechTemplatesAPI:
    """Test speech templates API with mock data."""

    def test_speech_templates_structured_success(self):
        """Test successful speech templates retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "data": {
                "permissions": {
                    "can_create_personal_templates": True,
                    "can_create_workspace_templates": False,
                },
                "templates": [
                    {
                        "id": 6001,
                        "name": "Meeting Notes Template",
                        "is_personal_template": True,
                        "is_customized": False,
                        "created_by": {
                            "id": 12345,
                            "name": "John Doe",
                        },
                        "base_template_type": "meeting_notes",
                        "permissions": {
                            "can_edit": True,
                            "can_delete": True,
                            "can_clone": True,
                            "can_view": True,
                            "can_apply": True,
                        },
                    },
                    {
                        "id": 6002,
                        "name": "System Interview Template",
                        "is_personal_template": False,
                        "is_customized": True,
                        "created_by": {
                            "id": None,
                            "name": "System",
                        },
                        "base_template_type": "interview",
                        "permissions": {
                            "can_edit": False,
                            "can_delete": False,
                            "can_clone": True,
                            "can_view": True,
                            "can_apply": True,
                        },
                    },
                ],
            },
            "code": 200,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            result = client.get_speech_templates_structured()

            assert isinstance(result, SpeechTemplatesResponse)
            assert result.status == "OK"
            assert result.code == 200
            assert result.data.permissions.can_create_personal_templates is True
            assert len(result.data.templates) == 2
            assert result.data.templates[0].name == "Meeting Notes Template"
            assert result.data.templates[1].created_by.id is None


class TestMockActionItemsAPI:
    """Test action items API with mock data."""

    def test_action_items_structured_success(self):
        """Test successful action items retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "process_status": "completed",
            "speech_action_items": [
                {
                    "id": 7001,
                    "created_at": 1640995200,
                    "last_modified_at": 1640995300,
                    "start_msec": 120000,
                    "end_msec": 125000,
                    "speech_otid": "test_otid_123",
                    "creator": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "avatar_url": "https://example.com/avatar.png",
                    },
                    "text": "Follow up on quarterly review",
                    "assignee": {
                        "id": 12346,
                        "name": "Jane Smith",
                        "email": "jane.smith@company.com",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "avatar_url": None,
                    },
                    "assigner": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "avatar_url": "https://example.com/avatar.png",
                    },
                    "completed": False,
                    "uuid": "action-item-uuid-123",
                    "order": "1",
                    "deleted_at": None,
                    "process_id": 8001,
                },
            ],
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            result = client.get_speech_action_items_structured("test_otid_123")

            assert isinstance(result, ActionItemsResponse)
            assert result.status == "OK"
            assert result.process_status == "completed"
            assert len(result.speech_action_items) == 1
            assert result.speech_action_items[0].text == "Follow up on quarterly review"
            assert result.speech_action_items[0].completed is False
            assert result.speech_action_items[0].assignee.name == "Jane Smith"


class TestMockAbstractSummaryAPI:
    """Test abstract summary API with mock data."""

    def test_abstract_summary_structured_success(self):
        """Test successful abstract summary retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "process_status": "completed",
            "abstract_summary": {
                "id": 9001,
                "status": "ready",
                "speech_otid": "test_otid_123",
                "items": ["Summary point 1", "Summary point 2"],
                "short_summary": "This is a brief summary of the meeting discussion.",
            },
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            result = client.get_abstract_summary_structured("test_otid_123")

            assert isinstance(result, AbstractSummaryResponse)
            assert result.status == "OK"
            assert result.process_status == "completed"
            assert result.abstract_summary.status == "ready"
            assert len(result.abstract_summary.items) == 2
            assert "brief summary" in result.abstract_summary.short_summary


class TestMockSpeechAPI:
    """Test speech API with mock data."""

    def test_speech_structured_success(self):
        """Test successful speech retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "speech": {
                "access_request": None,
                "access_seconds": 3600,
                "access_status": 1,
                "action_item_count": 2,
                "agent_session": None,
                "allow_transcript_copy": True,
                "appid": "app123",
                "audio_enabled": True,
                "auto_record": False,
                "auto_snapshot_enabled": False,
                "calendar_guests": None,
                "calendar_meeting_id": None,
                "can_comment": True,
                "can_edit": True,
                "can_export": True,
                "can_highlight": True,
                "chat_status": {
                    "show_chat": True,
                    "owner_chat_enabled": True,
                    "viewer_opt_out": False,
                    "can_edit_chat": True,
                },
                "conf_image_url": None,
                "conf_join_url": None,
                "create_method": "upload",
                "created_at": 1640995200,
                "deleted": False,
                "displayed_start_time": 1640995200,
                "download_url": "https://example.com/download/speech123",
                "duration": 3600,
                "end_time": 1640998800,
                "first_shared_group_name": None,
                "folder": None,
                "from_shared": False,
                "hasPhotos": 0,
                "has_meeting_series_access": False,
                "has_started": True,
                "image_urls": None,
                "images": [],
                "is_low_confidence": False,
                "is_meeting_series": False,
                "is_read": True,
                "language": "en-US",
                "link_share": {
                    "scope": "workspace",
                    "permission": "view",
                    "workspace_id": 12345,
                },
                "live_status": "finished",
                "live_status_message": "Processing completed",
                "meeting_otid": None,
                "modified_time": 1640995300,
                "non_member_shared_groups": [],
                "otid": "speech_otid_123",
                "owner": {
                    "id": 12345,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "avatar_url": "https://example.com/avatar.png",
                    "workspace": {
                        "id": 12345,
                        "name": "Example Workspace",
                    },
                },
                "permissions": {
                    "highlight": {"can_create": True, "can_edit": True},
                    "comment": {"can_create": True, "can_edit": True},
                    "text_note": {"can_create": True, "can_edit": True},
                    "chat": {"can_participate": True, "can_moderate": True},
                    "speech_share": {"can_share": True, "can_unshare": True},
                    "assign": True,
                    "reorder": True,
                    "share": True,
                    "export": True,
                    "emoji_react": True,
                },
                "process_failed": False,
                "process_finished": True,
                "process_status": {
                    "abstract_summary": "completed",
                    "action_item": "completed",
                    "speech_outline": "completed",
                },
                "public_share_url": None,
                "public_view": False,
                "pubsub_jwt": None,
                "pubsub_jwt_persistent": None,
                "sales_call_qualified": False,
                "shared_by": None,
                "shared_emails": [],
                "shared_groups": [],
                "shared_with": [],
                "short_abstract_summary": "Brief meeting summary",
                "speakers": [],
                "speech_id": "speech123",
                "speech_metadata": {"version": "1.0", "source": "upload"},
                "speech_outline": [
                    {
                        "id": 1,
                        "text": "Introduction",
                        "start_offset": 0,
                        "end_offset": 30000,
                        "start_word_offset": 0,
                        "end_word_offset": 50,
                        "segments": [
                            {
                                "id": 1,
                                "text": "Welcome everyone",
                                "start_offset": 0,
                                "end_offset": 15000,
                                "start_word_offset": 0,
                                "end_word_offset": 25,
                                "segments": None,
                            }
                        ],
                    }
                ],
                "speech_outline_status": "completed",
                "speech_settings": {
                    "allow_topics": True,
                    "language": True,
                    "allow_collaborators_to_share": True,
                    "allow_viewers_to_export": False,
                },
                "start_time": 1640995200,
                "summary": "Meeting summary content",
                "timecode_offset": None,
                "timezone": "America/New_York",
                "title": "Weekly Team Meeting",
                "transcript_updated_at": 1640995400,
                "unshared": False,
                "upload_finished": True,
                "word_clouds": [
                    {
                        "word": "meeting",
                        "score": "0.95",
                        "variants": ["meetings", "meet"],
                    }
                ],
                "session_info": [
                    {
                        "live_status": "finished",
                        "live_status_message": "Recording completed",
                        "id": "session123",
                        "title": "Weekly Team Meeting",
                        "offset": 0,
                    }
                ],
                "has_hidden_transcript": False,
                "language_config": {
                    "version": "1.0",
                    "default": {
                        "word_separator": " ",
                        "multiplier": 1,
                        "segment_punctuations": [".", "!", "?"],
                    },
                    "language_families": {},
                    "languages": {},
                    "metadata": {},
                },
                "transcripts": [],
                "realign_finished": True,
                "rematch_finished": True,
                "diarization_finished": True,
                "rematch_cutoff_time": None,
                "annotations": [],
                "topic_matches": [],
                "allow_topics": True,
                "topics": [],
                "topic_status": "completed",
                "audio_url": "https://example.com/audio/speech123.mp3",
                "show_live_summary": False,
                "crm_export_urls": {},
                "feedback_permission_checkbox_value": False,
                "feedback_permission_show_checkbox": False,
                "feedback_permission_type": "opt_in",
                "block_summary_display": False,
                "block_transcript_display": False,
            },
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_speech_structured("speech_otid_123")

            assert isinstance(result, SpeechResponse)
            assert result.status == "OK"
            assert result.speech.title == "Weekly Team Meeting"
            assert result.speech.duration == 3600
            assert result.speech.owner.name == "John Doe"
            assert result.speech.chat_status.show_chat is True
            assert result.speech.speech_outline[0].text == "Introduction"

    def test_available_speeches_structured_success(self):
        """Test successful available speeches retrieval with mock data."""
        mock_response_data = {
            "status": "OK",
            "end_of_list": False,
            "speeches": [
                {
                    "access_request": None,
                    "access_seconds": 3600,
                    "access_status": 1,
                    "action_item_count": None,
                    "agent_session": None,
                    "allow_transcript_copy": None,
                    "appid": "app123",
                    "audio_enabled": None,
                    "auto_record": None,
                    "auto_snapshot_enabled": None,
                    "calendar_guests": None,
                    "calendar_meeting_id": None,
                    "can_comment": None,
                    "can_edit": None,
                    "can_export": None,
                    "can_highlight": None,
                    "chat_status": None,
                    "conf_image_url": None,
                    "conf_join_url": None,
                    "create_method": None,
                    "created_at": 1640995200,
                    "deleted": False,
                    "displayed_start_time": 1640995200,
                    "download_url": None,
                    "duration": 1800,
                    "end_time": 1640997000,
                    "first_shared_group_name": None,
                    "folder": None,
                    "from_shared": None,
                    "hasPhotos": None,
                    "has_meeting_series_access": None,
                    "has_started": True,
                    "image_urls": None,
                    "images": [],
                    "is_low_confidence": None,
                    "is_meeting_series": None,
                    "is_read": None,
                    "language": "en-US",
                    "link_share": None,
                    "live_status": "finished",
                    "live_status_message": "Processing completed",
                    "meeting_otid": None,
                    "modified_time": 1640995300,
                    "non_member_shared_groups": None,
                    "otid": "speech_otid_456",
                    "owner": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "avatar_url": "https://example.com/avatar.png",
                        "workspace": None,
                    },
                    "permissions": None,
                    "process_failed": None,
                    "process_finished": None,
                    "process_status": None,
                    "public_share_url": None,
                    "public_view": None,
                    "pubsub_jwt": None,
                    "pubsub_jwt_persistent": None,
                    "sales_call_qualified": None,
                    "shared_by": None,
                    "shared_emails": [],
                    "shared_groups": [],
                    "shared_with": [],
                    "short_abstract_summary": None,
                    "speakers": [],
                    "speech_id": "speech456",
                    "speech_metadata": None,
                    "speech_outline": None,
                    "speech_outline_status": None,
                    "speech_settings": None,
                    "start_time": 1640995200,
                    "summary": None,
                    "timecode_offset": None,
                    "timezone": None,
                    "title": "Quick Standup",
                    "transcript_updated_at": None,
                    "unshared": None,
                    "upload_finished": None,
                    "word_clouds": None,
                    "session_info": None,
                    "has_hidden_transcript": None,
                    "language_config": None,
                    "transcripts": None,
                    "realign_finished": None,
                    "rematch_finished": None,
                    "diarization_finished": None,
                    "rematch_cutoff_time": None,
                    "annotations": [],
                    "topic_matches": [],
                    "allow_topics": None,
                    "topics": [],
                    "topic_status": None,
                    "audio_url": None,
                    "show_live_summary": None,
                    "crm_export_urls": None,
                    "feedback_permission_checkbox_value": None,
                    "feedback_permission_show_checkbox": None,
                    "feedback_permission_type": None,
                    "block_summary_display": None,
                    "block_transcript_display": None,
                },
            ],
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            result = client.get_available_speeches_structured()

            assert isinstance(result, AvailableSpeechesResponse)
            assert result.status == "OK"
            assert result.end_of_list is False
            assert len(result.speeches) == 1
            assert result.speeches[0].title == "Quick Standup"
            assert result.speeches[0].duration == 1800


class TestMockErrorHandling:
    """Test comprehensive error handling scenarios."""

    def test_network_error_handling(self):
        """Test network error handling."""
        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_request.side_effect = Exception("Network error")

            client = OtterAI()
            client._userid = "12345"

            with pytest.raises(Exception, match="Network error"):
                client.get_contacts_structured()

    def test_json_parsing_error(self):
        """Test JSON parsing error handling."""
        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            with pytest.raises(ValueError, match="Invalid JSON"):
                client.get_contacts_structured()

    def test_validation_error_handling(self):
        """Test Pydantic validation error handling."""
        invalid_response_data = {
            "status": "OK",
            "contacts": [
                {
                    "id": "invalid_id",  # Should be int
                    "type": "contact",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone_number": None,
                    "avatar_url": None,
                }
            ],
            "user_id": 12345,
            "last_modified_at": 1640995200,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            with pytest.raises(Exception):  # Pydantic validation error
                client.get_contacts_structured()


class TestMockEdgeCases:
    """Test edge cases and optional field handling."""

    def test_empty_lists_handling(self):
        """Test handling of empty lists."""
        mock_response_data = {
            "status": "OK",
            "contacts": [],
            "user_id": 12345,
            "last_modified_at": 1640995200,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_contacts_structured()

            assert isinstance(result, ContactsResponse)
            assert result.status == "OK"
            assert len(result.contacts) == 0

    def test_null_optional_fields(self):
        """Test handling of null optional fields."""
        mock_response_data = {
            "status": "OK",
            "folders": [
                {
                    "id": 2001,
                    "created_at": 1640995200,
                    "last_modified_at": 1640995200,
                    "deleted_at": None,
                    "last_speech_added_at": None,
                    "speech_count": 0,
                    "user_id": 12345,
                    "folder_name": "Test Folder",
                }
            ],
            "last_modified_at": 1640995600,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            result = client.get_folders_structured()

            assert isinstance(result, FoldersResponse)
            assert result.folders[0].deleted_at is None
            assert result.folders[0].last_speech_added_at is None
