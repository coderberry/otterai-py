"""
Pydantic models for structured data handling in OtterAI Python client.

This module provides base models and common data structures used across
the OtterAI API endpoints.
"""

from typing import Optional
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