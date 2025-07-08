"""
Pydantic models for structured data handling in OtterAI Python client.

This module provides base models and common data structures used across
the OtterAI API endpoints.
"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class User(BaseModel):
    """Basic user information model."""

    id: int = Field(..., description="Unique user identifier")
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")


class Workspace(BaseModel):
    """Workspace information model."""

    id: int = Field(..., description="Unique workspace identifier")
    name: str = Field(..., description="Workspace name")


class Permission(BaseModel):
    """Generic permission structure."""

    can_read: bool = Field(default=True, description="Read permission")
    can_write: bool = Field(default=False, description="Write permission")
    can_delete: bool = Field(default=False, description="Delete permission")
    can_share: bool = Field(default=False, description="Share permission")


class BaseResponse(BaseModel):
    """Common response wrapper for API responses."""

    status: str = Field(..., description="Response status")
    last_load_ts: Optional[int] = Field(None, description="Last load timestamp")


class Contact(BaseModel):
    """Contact information model."""

    id: int = Field(..., description="Unique contact identifier")
    type: str = Field(..., description="Contact type (typically 'contact')")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    phone_number: Optional[str] = Field(None, description="Phone number")
    avatar_url: Optional[str] = Field(None, description="URL to contact's avatar image")


class ContactsResponse(BaseResponse):
    """Response wrapper for contacts endpoint."""

    contacts: List[Contact] = Field(..., description="List of contacts")
    user_id: int = Field(..., description="User ID")
    last_modified_at: int = Field(..., description="Last modified timestamp")


class Folder(BaseModel):
    """Folder structure model."""

    id: int = Field(..., description="Unique folder identifier")
    created_at: int = Field(..., description="Creation timestamp")
    last_modified_at: int = Field(..., description="Last modified timestamp")
    deleted_at: Optional[int] = Field(None, description="Deletion timestamp")
    last_speech_added_at: Optional[int] = Field(
        None, description="Last speech added timestamp"
    )
    speech_count: int = Field(..., description="Number of speeches in folder")
    user_id: int = Field(..., description="User ID")
    folder_name: str = Field(..., description="Folder name")


class FoldersResponse(BaseResponse):
    """Response wrapper for folders endpoint."""

    folders: List[Folder] = Field(..., description="List of folders")
    last_modified_at: int = Field(..., description="Last modified timestamp")


class MentionCandidate(BaseModel):
    """Simple user reference model for mention candidates."""

    id: int = Field(..., description="Unique user identifier")
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")
    permission: str = Field(..., description="Permission level (e.g., 'owner')")


class MentionCandidatesResponse(BaseResponse):
    """Response wrapper for mention candidates endpoint."""

    mention_candidates: List[MentionCandidate] = Field(
        ..., description="List of mention candidates"
    )


class Group(BaseModel):
    """Group information model with nested user objects."""

    id: int = Field(..., description="Unique group identifier")
    created_at: int = Field(..., description="Creation timestamp")
    last_modified_at: int = Field(..., description="Last modified timestamp")
    name: str = Field(..., description="Group name")
    is_deleted: bool = Field(..., description="Whether the group is deleted")
    is_public: bool = Field(..., description="Whether the group is public")
    has_left: bool = Field(..., description="Whether the user has left the group")
    public_name: Optional[str] = Field(None, description="Public name of the group")
    description: Optional[str] = Field(None, description="Group description")
    new_unread_msg_count: int = Field(..., description="Number of unread messages")
    bolding: bool = Field(..., description="Whether messages are bolded")
    latest_message_time: str = Field(..., description="Latest message timestamp")
    last_group_visit_time: str = Field(..., description="Last group visit timestamp")
    owner: User = Field(..., description="Group owner information")
    cover_photo_url: Optional[str] = Field(None, description="Cover photo URL")
    avatar_url: Optional[str] = Field(None, description="Group avatar URL")
    open_post: bool = Field(..., description="Whether posting is open")
    open_invite: bool = Field(..., description="Whether invites are open")
    can_post: bool = Field(..., description="Whether user can post")
    member_count: int = Field(..., description="Number of members")
    dm_name: Optional[str] = Field(None, description="Direct message name")
    is_dm_visible: bool = Field(..., description="Whether DM is visible")
    first_member: User = Field(..., description="First member information")
    has_live_speech: bool = Field(..., description="Whether group has live speech")
    is_autoshare_group: bool = Field(..., description="Whether group is autoshare")
    discoverability: str = Field(..., description="Group discoverability setting")
    workspace_id: Optional[int] = Field(None, description="Workspace ID")


class GroupsResponse(BaseResponse):
    """Response wrapper for groups endpoint."""

    groups: List[Group] = Field(..., description="List of groups")
    last_load_ts: int = Field(..., description="Last load timestamp")


class Speaker(BaseModel):
    """Speaker information model with owner details."""

    id: int = Field(..., description="Unique speaker identifier")
    created_at: str = Field(..., description="Creation timestamp")
    speaker_name: str = Field(..., description="Speaker name")
    url: Optional[str] = Field(None, description="Speaker audio profile URL")
    user_id: int = Field(..., description="Associated user ID")
    self_speaker: bool = Field(..., description="Whether this is user's own speaker")
    speaker_email: Optional[str] = Field(None, description="Speaker email address")
    owner: User = Field(..., description="Speaker owner information")


class SpeakersResponse(BaseResponse):
    """Response wrapper for speakers endpoint."""

    speakers: List[Speaker] = Field(..., description="List of speakers")


# Phase 4: Speech Templates and Action Items Models


class TemplatePermissions(BaseModel):
    """Template-specific permissions model."""

    can_edit: bool = Field(..., description="Can edit template")
    can_delete: bool = Field(..., description="Can delete template")
    can_clone: bool = Field(..., description="Can clone template")
    can_view: bool = Field(..., description="Can view template")
    can_apply: bool = Field(..., description="Can apply template")


class TemplateCreator(BaseModel):
    """Template creator information model."""

    id: Optional[int] = Field(
        None, description="Creator ID (null for system templates)"
    )
    name: str = Field(..., description="Creator name")


class SpeechTemplate(BaseModel):
    """Speech template model."""

    id: int = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    is_personal_template: bool = Field(..., description="Whether template is personal")
    is_customized: bool = Field(..., description="Whether template is customized")
    created_by: TemplateCreator = Field(..., description="Template creator")
    base_template_type: str = Field(..., description="Base template type")
    permissions: TemplatePermissions = Field(..., description="Template permissions")


class SpeechTemplatePermissions(BaseModel):
    """Global speech template permissions model."""

    can_create_personal_templates: bool = Field(
        ..., description="Can create personal templates"
    )
    can_create_workspace_templates: bool = Field(
        ..., description="Can create workspace templates"
    )


class SpeechTemplatesData(BaseModel):
    """Data structure for speech templates response."""

    permissions: SpeechTemplatePermissions = Field(
        ..., description="Global template permissions"
    )
    templates: List[SpeechTemplate] = Field(..., description="List of speech templates")


class SpeechTemplatesResponse(BaseResponse):
    """Response wrapper for speech_templates endpoint."""

    data: SpeechTemplatesData = Field(..., description="Speech templates data")
    code: int = Field(..., description="HTTP status code")


class ActionItem(BaseModel):
    """Action item model."""

    id: int = Field(..., description="Unique action item identifier")
    created_at: int = Field(..., description="Creation timestamp")
    last_modified_at: int = Field(..., description="Last modified timestamp")
    start_msec: int = Field(..., description="Start time in milliseconds")
    end_msec: Optional[int] = Field(None, description="End time in milliseconds")
    speech_otid: str = Field(..., description="Speech OTID")
    creator: Optional[User] = Field(None, description="Action item creator")
    text: str = Field(..., description="Action item text")
    assignee: Optional[User] = Field(None, description="Action item assignee")
    assigner: Optional[User] = Field(None, description="Action item assigner")
    completed: bool = Field(..., description="Whether action item is completed")
    uuid: str = Field(..., description="Action item UUID")
    order: str = Field(..., description="Action item order")
    deleted_at: Optional[int] = Field(None, description="Deletion timestamp")
    process_id: int = Field(..., description="Process ID")


class ActionItemsResponse(BaseResponse):
    """Response wrapper for speech_action_items endpoint."""

    process_status: str = Field(..., description="Processing status")
    speech_action_items: List[ActionItem] = Field(
        ..., description="List of action items"
    )


class AbstractSummaryData(BaseModel):
    """Abstract summary data model."""

    id: int = Field(..., description="Summary ID")
    status: str = Field(..., description="Summary status")
    speech_otid: str = Field(..., description="Speech OTID")
    items: List = Field(..., description="Summary items")
    short_summary: str = Field(..., description="Short summary text")


class AbstractSummaryResponse(BaseResponse):
    """Response wrapper for abstract_summary endpoint."""

    process_status: str = Field(..., description="Processing status")
    abstract_summary: AbstractSummaryData = Field(
        ..., description="Abstract summary data"
    )


# Phase 5: Speech Model - Most Complex


class ChatStatus(BaseModel):
    """Chat status configuration model."""

    show_chat: bool = Field(..., description="Whether to show chat")
    owner_chat_enabled: bool = Field(..., description="Whether owner chat is enabled")
    viewer_opt_out: bool = Field(..., description="Whether viewer opted out")
    can_edit_chat: bool = Field(..., description="Whether chat can be edited")


class LinkShare(BaseModel):
    """Link sharing configuration model."""

    scope: Optional[str] = Field(None, description="Sharing scope")
    permission: Optional[str] = Field(None, description="Sharing permission")
    workspace_id: Optional[int] = Field(None, description="Workspace ID for sharing")


class SpeechOutlineSegment(BaseModel):
    """Speech outline segment model."""

    id: int = Field(..., description="Segment ID")
    text: str = Field(..., description="Segment text")
    start_offset: int = Field(..., description="Start offset in milliseconds")
    end_offset: int = Field(..., description="End offset in milliseconds")
    start_word_offset: int = Field(..., description="Start word offset")
    end_word_offset: int = Field(..., description="End word offset")
    segments: Optional[List["SpeechOutlineSegment"]] = Field(
        None, description="Nested segments"
    )


class SpeechOutlineItem(BaseModel):
    """Speech outline item model."""

    id: int = Field(..., description="Outline item ID")
    text: str = Field(..., description="Outline item text")
    start_offset: int = Field(..., description="Start offset in milliseconds")
    end_offset: int = Field(..., description="End offset in milliseconds")
    start_word_offset: int = Field(..., description="Start word offset")
    end_word_offset: int = Field(..., description="End word offset")
    segments: List[SpeechOutlineSegment] = Field(
        ..., description="List of outline segments"
    )


class SpeechPermissions(BaseModel):
    """Speech permissions model."""

    highlight: dict = Field(..., description="Highlight permissions")
    comment: dict = Field(..., description="Comment permissions")
    text_note: dict = Field(..., description="Text note permissions")
    chat: dict = Field(..., description="Chat permissions")
    speech_share: dict = Field(..., description="Speech share permissions")
    assign: bool = Field(..., description="Assign permission")
    reorder: bool = Field(..., description="Reorder permission")
    share: bool = Field(..., description="Share permission")
    export: bool = Field(..., description="Export permission")
    emoji_react: bool = Field(..., description="Emoji react permission")


class ProcessStatus(BaseModel):
    """Processing status model."""

    abstract_summary: str = Field(..., description="Abstract summary status")
    action_item: str = Field(..., description="Action item status")
    speech_outline: str = Field(..., description="Speech outline status")


class SpeechSettings(BaseModel):
    """Speech settings model."""

    allow_topics: bool = Field(..., description="Allow topics")
    language: bool = Field(..., description="Language setting")
    allow_collaborators_to_share: bool = Field(
        ..., description="Allow collaborators to share"
    )
    allow_viewers_to_export: bool = Field(..., description="Allow viewers to export")


class WordCloudItem(BaseModel):
    """Word cloud item model."""

    word: str = Field(..., description="Word")
    score: str = Field(..., description="Score")
    variants: List[str] = Field(..., description="Word variants")


class SessionInfo(BaseModel):
    """Session information model."""

    live_status: str = Field(..., description="Live status")
    live_status_message: str = Field(..., description="Live status message")
    id: Optional[str] = Field(None, description="Session ID")
    title: str = Field(..., description="Session title")
    offset: int = Field(..., description="Session offset")


class LanguageFamily(BaseModel):
    """Language family configuration model."""

    word_separator: str = Field(..., description="Word separator")
    multiplier: int = Field(..., description="Multiplier")
    segment_punctuations: Optional[List[str]] = Field(
        None, description="Segment punctuations"
    )


class LanguageConfig(BaseModel):
    """Language configuration model."""

    version: str = Field(..., description="Configuration version")
    default: LanguageFamily = Field(..., description="Default language family")
    language_families: dict = Field(..., description="Language families")
    languages: dict = Field(..., description="Languages")
    metadata: dict = Field(..., description="Configuration metadata")


class TranscriptAlignment(BaseModel):
    """Transcript alignment model."""

    word: str = Field(..., description="Word")
    start: float = Field(..., description="Start time")
    end: float = Field(..., description="End time")
    startOffset: int = Field(..., description="Start offset")
    endOffset: int = Field(..., description="End offset")


class Transcript(BaseModel):
    """Transcript model."""

    uuid: str = Field(..., description="Transcript UUID")
    id: int = Field(..., description="Transcript ID")
    start_offset: int = Field(..., description="Start offset")
    end_offset: int = Field(..., description="End offset")
    transcript: str = Field(..., description="Transcript text")
    label: str = Field(..., description="Speaker label")
    speaker_id: Optional[str] = Field(None, description="Speaker ID")
    created_at: str = Field(..., description="Created timestamp")
    speaker_model_label: Optional[str] = Field(None, description="Speaker model label")
    speech_id: str = Field(..., description="Speech ID")
    speaker_edited_at: Optional[str] = Field(
        None, description="Speaker edited timestamp"
    )
    alignment: List[TranscriptAlignment] = Field(..., description="Word alignment")
    sig: str = Field(..., description="Signature")


class UserWithWorkspace(BaseModel):
    """User model with workspace information."""

    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User name")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    workspace: Optional[Workspace] = Field(None, description="Workspace information")


class Speech(BaseModel):
    """Complete speech model with all nested structures."""

    access_request: Optional[str] = Field(None, description="Access request")
    access_seconds: int = Field(..., description="Access seconds")
    access_status: int = Field(..., description="Access status")
    action_item_count: Optional[int] = Field(None, description="Action item count")
    agent_session: Optional[str] = Field(None, description="Agent session")
    allow_transcript_copy: Optional[bool] = Field(
        None, description="Allow transcript copy"
    )
    appid: str = Field(..., description="Application ID")
    audio_enabled: Optional[bool] = Field(None, description="Audio enabled")
    auto_record: Optional[bool] = Field(None, description="Auto record")
    auto_snapshot_enabled: Optional[bool] = Field(
        None, description="Auto snapshot enabled"
    )
    calendar_guests: Optional[str] = Field(None, description="Calendar guests")
    calendar_meeting_id: Optional[Union[str, int]] = Field(
        None, description="Calendar meeting ID"
    )
    can_comment: Optional[bool] = Field(None, description="Can comment")
    can_edit: Optional[bool] = Field(None, description="Can edit")
    can_export: Optional[bool] = Field(None, description="Can export")
    can_highlight: Optional[bool] = Field(None, description="Can highlight")
    chat_status: Optional[ChatStatus] = Field(None, description="Chat status")
    conf_image_url: Optional[str] = Field(None, description="Conference image URL")
    conf_join_url: Optional[str] = Field(None, description="Conference join URL")
    create_method: Optional[str] = Field(None, description="Create method")
    created_at: int = Field(..., description="Created timestamp")
    deleted: bool = Field(..., description="Deleted status")
    displayed_start_time: int = Field(..., description="Displayed start time")
    download_url: Optional[str] = Field(None, description="Download URL")
    duration: int = Field(..., description="Duration in seconds")
    end_time: int = Field(..., description="End time")
    first_shared_group_name: Optional[str] = Field(
        None, description="First shared group name"
    )
    folder: Optional[str] = Field(None, description="Folder")
    from_shared: Optional[bool] = Field(None, description="From shared")
    hasPhotos: Optional[int] = Field(None, description="Has photos")
    has_meeting_series_access: Optional[bool] = Field(
        None, description="Has meeting series access"
    )
    has_started: bool = Field(..., description="Has started")
    image_urls: Optional[str] = Field(None, description="Image URLs")
    images: List = Field(..., description="Images")
    is_low_confidence: Optional[bool] = Field(None, description="Is low confidence")
    is_meeting_series: Optional[bool] = Field(None, description="Is meeting series")
    is_read: Optional[bool] = Field(None, description="Is read")
    language: str = Field(..., description="Language")
    link_share: Optional[LinkShare] = Field(None, description="Link share")
    live_status: str = Field(..., description="Live status")
    live_status_message: str = Field(..., description="Live status message")
    meeting_otid: Optional[str] = Field(None, description="Meeting OTID")
    modified_time: int = Field(..., description="Modified time")
    non_member_shared_groups: Optional[List] = Field(
        None, description="Non-member shared groups"
    )
    otid: str = Field(..., description="OTID")
    owner: UserWithWorkspace = Field(..., description="Owner")
    permissions: Optional[SpeechPermissions] = Field(None, description="Permissions")
    process_failed: Optional[bool] = Field(None, description="Process failed")
    process_finished: Optional[bool] = Field(None, description="Process finished")
    process_status: Optional[ProcessStatus] = Field(None, description="Process status")
    public_share_url: Optional[str] = Field(None, description="Public share URL")
    public_view: Optional[bool] = Field(None, description="Public view")
    pubsub_jwt: Optional[str] = Field(None, description="Pubsub JWT")
    pubsub_jwt_persistent: Optional[str] = Field(
        None, description="Pubsub JWT persistent"
    )
    sales_call_qualified: Optional[bool] = Field(
        None, description="Sales call qualified"
    )
    shared_by: Optional[str] = Field(None, description="Shared by")
    shared_emails: Optional[List] = Field(default=[], description="Shared emails")
    shared_groups: Optional[List] = Field(default=[], description="Shared groups")
    shared_with: Optional[List] = Field(default=[], description="Shared with")
    short_abstract_summary: Optional[str] = Field(
        None, description="Short abstract summary"
    )
    speakers: List = Field(..., description="Speakers")
    speech_id: str = Field(..., description="Speech ID")
    speech_metadata: Optional[dict] = Field(None, description="Speech metadata")
    speech_outline: Optional[List[SpeechOutlineItem]] = Field(
        None, description="Speech outline"
    )
    speech_outline_status: Optional[str] = Field(
        None, description="Speech outline status"
    )
    speech_settings: Optional[SpeechSettings] = Field(
        None, description="Speech settings"
    )
    start_time: int = Field(..., description="Start time")
    summary: Optional[str] = Field(None, description="Summary")
    timecode_offset: Optional[str] = Field(None, description="Timecode offset")
    timezone: Optional[str] = Field(None, description="Timezone")
    title: Optional[str] = Field(None, description="Title")
    transcript_updated_at: Optional[int] = Field(
        None, description="Transcript updated at"
    )
    unshared: Optional[bool] = Field(None, description="Unshared")
    upload_finished: Optional[bool] = Field(None, description="Upload finished")
    word_clouds: Optional[List[WordCloudItem]] = Field(None, description="Word clouds")
    session_info: Optional[List[SessionInfo]] = Field(None, description="Session info")
    has_hidden_transcript: Optional[bool] = Field(
        None, description="Has hidden transcript"
    )
    language_config: Optional[LanguageConfig] = Field(
        None, description="Language config"
    )
    transcripts: Optional[List[Transcript]] = Field(None, description="Transcripts")
    realign_finished: Optional[bool] = Field(None, description="Realign finished")
    rematch_finished: Optional[bool] = Field(None, description="Rematch finished")
    diarization_finished: Optional[bool] = Field(
        None, description="Diarization finished"
    )
    rematch_cutoff_time: Optional[str] = Field(None, description="Rematch cutoff time")
    annotations: Optional[List] = Field(default=[], description="Annotations")
    topic_matches: Optional[List] = Field(default=[], description="Topic matches")
    allow_topics: Optional[bool] = Field(None, description="Allow topics")
    topics: Optional[List] = Field(default=[], description="Topics")
    topic_status: Optional[str] = Field(None, description="Topic status")
    audio_url: Optional[str] = Field(None, description="Audio URL")
    show_live_summary: Optional[bool] = Field(None, description="Show live summary")
    crm_export_urls: Optional[dict] = Field(None, description="CRM export URLs")
    feedback_permission_checkbox_value: Optional[bool] = Field(
        None, description="Feedback permission checkbox value"
    )
    feedback_permission_show_checkbox: Optional[bool] = Field(
        None, description="Feedback permission show checkbox"
    )
    feedback_permission_type: Optional[str] = Field(
        None, description="Feedback permission type"
    )
    block_summary_display: Optional[bool] = Field(
        None, description="Block summary display"
    )
    block_transcript_display: Optional[bool] = Field(
        None, description="Block transcript display"
    )


class SpeechResponse(BaseResponse):
    """Response wrapper for speech endpoint."""

    speech: Speech = Field(..., description="Speech data")


class AvailableSpeeches(BaseModel):
    """Available speeches data model."""

    end_of_list: bool = Field(..., description="End of list indicator")
    speeches: List[Speech] = Field(..., description="List of speeches")


class AvailableSpeechesResponse(BaseResponse):
    """Response wrapper for available_speeches endpoint."""

    end_of_list: bool = Field(..., description="End of list indicator")
    speeches: List[Speech] = Field(..., description="List of speeches")


# Forward reference resolution
SpeechOutlineSegment.model_rebuild()
