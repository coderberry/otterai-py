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
