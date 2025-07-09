"""
Performance and memory usage tests for OtterAI Python client.

These tests ensure that the structured data models perform well
with large datasets and don't consume excessive memory.
"""

import time
from unittest.mock import Mock, patch

import pytest

from otterai.models import (
    AvailableSpeechesResponse,
    ContactsResponse,
    GroupsResponse,
    SpeechResponse,
)
from otterai.otterai import OtterAI


class TestPerformance:
    """Test performance with large datasets."""

    def test_large_contacts_list_performance(self):
        """Test performance with large contacts list."""
        # Create mock data with 1000 contacts
        contacts_data = []
        for i in range(1000):
            contacts_data.append(
                {
                    "id": 1000 + i,
                    "type": "contact",
                    "first_name": f"User{i}",
                    "last_name": f"Contact{i}",
                    "email": f"user{i}@example.com",
                    "phone_number": None,
                    "avatar_url": None,
                }
            )

        mock_response_data = {
            "status": "OK",
            "contacts": contacts_data,
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

            # Measure execution time
            start_time = time.time()
            result = client.get_contacts_structured()
            end_time = time.time()

            execution_time = end_time - start_time

            # Performance assertions
            assert isinstance(result, ContactsResponse)
            assert len(result.contacts) == 1000
            assert execution_time < 1.0  # Should complete within 1 second

            # Verify data integrity
            assert result.contacts[0].first_name == "User0"
            assert result.contacts[999].first_name == "User999"

    def test_large_groups_list_performance(self):
        """Test performance with large groups list."""
        # Create mock data with 500 groups
        groups_data = []
        for i in range(500):
            groups_data.append(
                {
                    "id": 3000 + i,
                    "created_at": 1640995200,
                    "last_modified_at": 1640995300,
                    "name": f"Group {i}",
                    "is_deleted": False,
                    "is_public": False,
                    "has_left": False,
                    "public_name": None,
                    "description": f"Description for group {i}",
                    "new_unread_msg_count": 0,
                    "bolding": False,
                    "latest_message_time": "2024-01-01 10:00:00",
                    "last_group_visit_time": "2024-01-01 10:30:00",
                    "owner": {
                        "id": 12345 + i,
                        "name": f"Owner {i}",
                        "email": f"owner{i}@example.com",
                        "first_name": f"Owner{i}",
                        "last_name": f"User{i}",
                        "avatar_url": f"https://example.com/avatar{i}.png",
                    },
                    "cover_photo_url": None,
                    "avatar_url": None,
                    "open_post": True,
                    "open_invite": True,
                    "can_post": True,
                    "member_count": 5 + i,
                    "dm_name": None,
                    "is_dm_visible": False,
                    "first_member": {
                        "id": 12346 + i,
                        "name": f"Member {i}",
                        "email": f"member{i}@example.com",
                        "first_name": f"Member{i}",
                        "last_name": f"User{i}",
                        "avatar_url": f"https://example.com/member{i}.png",
                    },
                    "has_live_speech": False,
                    "is_autoshare_group": False,
                    "discoverability": "private",
                    "workspace_id": None,
                }
            )

        mock_response_data = {
            "status": "OK",
            "groups": groups_data,
            "last_load_ts": 1640995400,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            # Measure execution time
            start_time = time.time()
            result = client.list_groups_structured()
            end_time = time.time()

            execution_time = end_time - start_time

            # Performance assertions
            assert isinstance(result, GroupsResponse)
            assert len(result.groups) == 500
            assert execution_time < 2.0  # Should complete within 2 seconds

            # Verify nested object performance
            assert result.groups[0].owner.name == "Owner 0"
            assert result.groups[499].first_member.name == "Member 499"

    def test_complex_speech_object_performance(self):
        """Test performance with complex speech object."""
        # Create a complex speech with many nested structures
        speech_outline = []
        for i in range(100):
            speech_outline.append(
                {
                    "id": i + 1,
                    "text": f"Section {i + 1}",
                    "start_offset": i * 30000,
                    "end_offset": (i + 1) * 30000,
                    "start_word_offset": i * 50,
                    "end_word_offset": (i + 1) * 50,
                    "segments": [
                        {
                            "id": j + 1,
                            "text": f"Segment {i + 1}.{j + 1}",
                            "start_offset": i * 30000 + j * 5000,
                            "end_offset": i * 30000 + (j + 1) * 5000,
                            "start_word_offset": i * 50 + j * 10,
                            "end_word_offset": i * 50 + (j + 1) * 10,
                            "segments": None,
                        }
                        for j in range(5)
                    ],
                }
            )

        word_clouds = []
        for i in range(50):
            word_clouds.append(
                {
                    "word": f"word{i}",
                    "score": f"0.{90 - i}",
                    "variants": [f"word{i}s", f"word{i}ing"],
                }
            )

        mock_response_data = {
            "status": "OK",
            "speech": {
                "access_request": None,
                "access_seconds": 3600,
                "access_status": 1,
                "action_item_count": 50,
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
                "duration": 18000,  # 5 hours
                "end_time": 1641013200,
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
                "short_abstract_summary": "Complex meeting with many topics",
                "speakers": [],
                "speech_id": "speech123",
                "speech_metadata": {"version": "1.0", "source": "upload"},
                "speech_outline": speech_outline,
                "speech_outline_status": "completed",
                "speech_settings": {
                    "allow_topics": True,
                    "language": True,
                    "allow_collaborators_to_share": True,
                    "allow_viewers_to_export": False,
                },
                "start_time": 1640995200,
                "summary": "Complex meeting summary with extensive content",
                "timecode_offset": None,
                "timezone": "America/New_York",
                "title": "Complex Long Meeting",
                "transcript_updated_at": 1640995400,
                "unshared": False,
                "upload_finished": True,
                "word_clouds": word_clouds,
                "session_info": [
                    {
                        "live_status": "finished",
                        "live_status_message": "Recording completed",
                        "id": "session123",
                        "title": "Complex Long Meeting",
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

            # Measure execution time
            start_time = time.time()
            result = client.get_speech_structured("speech_otid_123")
            end_time = time.time()

            execution_time = end_time - start_time

            # Performance assertions
            assert isinstance(result, SpeechResponse)
            assert result.speech.title == "Complex Long Meeting"
            assert len(result.speech.speech_outline) == 100
            assert len(result.speech.word_clouds) == 50
            assert execution_time < 1.0  # Should complete within 1 second

            # Verify nested structure performance
            assert result.speech.speech_outline[0].text == "Section 1"
            assert len(result.speech.speech_outline[0].segments) == 5
            assert result.speech.speech_outline[99].text == "Section 100"

    def test_available_speeches_large_list_performance(self):
        """Test performance with large available speeches list."""
        # Create mock data with 200 speeches
        speeches_data = []
        for i in range(200):
            speeches_data.append(
                {
                    "access_request": None,
                    "access_seconds": 3600,
                    "access_status": 1,
                    "action_item_count": None,
                    "agent_session": None,
                    "allow_transcript_copy": None,
                    "appid": f"app{i}",
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
                    "created_at": 1640995200 + i,
                    "deleted": False,
                    "displayed_start_time": 1640995200 + i,
                    "download_url": None,
                    "duration": 1800 + i * 10,
                    "end_time": 1640997000 + i,
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
                    "modified_time": 1640995300 + i,
                    "non_member_shared_groups": None,
                    "otid": f"speech_otid_{i}",
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
                    "speech_id": f"speech{i}",
                    "speech_metadata": None,
                    "speech_outline": None,
                    "speech_outline_status": None,
                    "speech_settings": None,
                    "start_time": 1640995200 + i,
                    "summary": None,
                    "timecode_offset": None,
                    "timezone": None,
                    "title": f"Speech {i}",
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
                }
            )

        mock_response_data = {
            "status": "OK",
            "end_of_list": False,
            "speeches": speeches_data,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()

            # Measure execution time
            start_time = time.time()
            result = client.get_available_speeches_structured()
            end_time = time.time()

            execution_time = end_time - start_time

            # Performance assertions
            assert isinstance(result, AvailableSpeechesResponse)
            assert len(result.speeches) == 200
            assert execution_time < 2.0  # Should complete within 2 seconds

            # Verify data integrity
            assert result.speeches[0].title == "Speech 0"
            assert result.speeches[199].title == "Speech 199"


class TestMemoryUsage:
    """Test memory usage with large datasets."""

    def test_memory_efficiency_large_dataset(self):
        """Test memory efficiency with large dataset."""
        # This test ensures that large datasets don't cause memory issues
        # In a real scenario, you would use memory profiling tools

        # Create a large dataset
        large_contacts = []
        for i in range(5000):
            large_contacts.append(
                {
                    "id": 10000 + i,
                    "type": "contact",
                    "first_name": f"FirstName{i}",
                    "last_name": f"LastName{i}",
                    "email": f"user{i}@example.com",
                    "phone_number": f"+123456{i:04d}",
                    "avatar_url": f"https://example.com/avatar{i}.png",
                }
            )

        mock_response_data = {
            "status": "OK",
            "contacts": large_contacts,
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

            # Process the large dataset
            result = client.get_contacts_structured()

            # Verify the result
            assert isinstance(result, ContactsResponse)
            assert len(result.contacts) == 5000

            # Basic memory test - ensure we can access all items
            for i, contact in enumerate(result.contacts):
                if i % 1000 == 0:  # Sample every 1000th contact
                    assert contact.first_name == f"FirstName{i}"
                    assert contact.email == f"user{i}@example.com"

            # Test cleanup - ensure objects can be garbage collected
            del result
            del large_contacts
            del mock_response_data

    def test_nested_object_memory_efficiency(self):
        """Test memory efficiency with deeply nested objects."""
        # Create a speech with many nested levels
        complex_outline = []
        for i in range(50):
            segments = []
            for j in range(20):
                segments.append(
                    {
                        "id": j + 1,
                        "text": f"Nested segment {i}.{j}",
                        "start_offset": j * 1000,
                        "end_offset": (j + 1) * 1000,
                        "start_word_offset": j * 10,
                        "end_word_offset": (j + 1) * 10,
                        "segments": None,
                    }
                )

            complex_outline.append(
                {
                    "id": i + 1,
                    "text": f"Complex section {i}",
                    "start_offset": i * 20000,
                    "end_offset": (i + 1) * 20000,
                    "start_word_offset": i * 200,
                    "end_word_offset": (i + 1) * 200,
                    "segments": segments,
                }
            )

        mock_response_data = {
            "status": "OK",
            "speech": {
                "access_request": None,
                "access_seconds": 3600,
                "access_status": 1,
                "action_item_count": None,
                "agent_session": None,
                "allow_transcript_copy": None,
                "appid": "memory_test",
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
                "duration": 36000,
                "end_time": 1641031200,
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
                "otid": "memory_test_speech",
                "owner": {
                    "id": 12345,
                    "name": "Memory Test User",
                    "email": "memory@example.com",
                    "first_name": "Memory",
                    "last_name": "Test",
                    "avatar_url": None,
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
                "speech_id": "memory_test_speech",
                "speech_metadata": None,
                "speech_outline": complex_outline,
                "speech_outline_status": None,
                "speech_settings": None,
                "start_time": 1640995200,
                "summary": None,
                "timecode_offset": None,
                "timezone": None,
                "title": "Memory Test Speech",
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
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            # Process the complex nested structure
            result = client.get_speech_structured("memory_test_speech")

            # Verify the result
            assert isinstance(result, SpeechResponse)
            assert result.speech.title == "Memory Test Speech"
            assert len(result.speech.speech_outline) == 50

            # Verify nested structure
            for i, item in enumerate(result.speech.speech_outline):
                assert len(item.segments) == 20
                assert item.text == f"Complex section {i}"

                # Sample check of nested segments
                if i == 0:
                    assert item.segments[0].text == "Nested segment 0.0"
                    assert item.segments[19].text == "Nested segment 0.19"

            # Test cleanup
            del result
            del complex_outline
            del mock_response_data


class TestBenchmarks:
    """Benchmark tests for performance comparison."""

    def test_serialization_benchmark(self):
        """Benchmark serialization performance."""
        # Create a moderately sized dataset
        test_data = {
            "status": "OK",
            "contacts": [
                {
                    "id": 1000 + i,
                    "type": "contact",
                    "first_name": f"User{i}",
                    "last_name": f"Contact{i}",
                    "email": f"user{i}@example.com",
                    "phone_number": f"+123456{i:04d}",
                    "avatar_url": f"https://example.com/avatar{i}.png",
                }
                for i in range(100)
            ],
            "user_id": 12345,
            "last_modified_at": 1640995200,
        }

        with patch.object(OtterAI, "_make_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = test_data
            mock_request.return_value = mock_response

            client = OtterAI()
            client._userid = "12345"

            # Benchmark multiple runs
            execution_times = []
            for _ in range(10):
                start_time = time.time()
                result = client.get_contacts_structured()
                end_time = time.time()
                execution_times.append(end_time - start_time)

            # Calculate statistics
            avg_time = sum(execution_times) / len(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)

            # Performance assertions
            assert avg_time < 0.1  # Average should be under 100ms
            assert max_time < 0.2  # Max should be under 200ms
            assert min_time > 0.0  # Min should be positive

            # Verify result consistency
            assert isinstance(result, ContactsResponse)
            assert len(result.contacts) == 100
