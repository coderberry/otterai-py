"""
Pydantic models for structured data handling in OtterAI Python client.

This module provides base models and common data structures used across
the OtterAI API endpoints.
"""

from typing import Optional, List
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
