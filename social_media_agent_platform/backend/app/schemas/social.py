from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from enum import Enum

from app.schemas.user import UserResponse

class SocialPlatform(str, Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    REDDIT = "reddit"
    DISCORD = "discord"
    SLACK = "slack"
    OTHER = "other"

class SocialAccountStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    REFRESHING = "refreshing"

# Base schema for social account
class SocialAccountBase(BaseModel):
    platform: SocialPlatform
    display_name: str = Field(..., max_length=255)
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    external_id: str = Field(..., max_length=255)
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

# Schema for creating a new social account connection
class SocialAccountCreate(SocialAccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expiry: Optional[datetime] = None

# Schema for updating a social account
class SocialAccountUpdate(BaseModel):
    display_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[SocialAccountStatus] = None
    metadata: Optional[Dict[str, Any]] = None

# Schema for social account in database
class SocialAccountInDBBase(SocialAccountBase):
    id: int
    owner_id: int
    status: SocialAccountStatus
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for returning social account data via API (without sensitive data)
class SocialAccount(SocialAccountInDBBase):
    is_connected: bool = Field(..., description="Whether the account is currently connected")
    
    @classmethod
    def from_orm(cls, obj):
        # Convert SQLAlchemy model to Pydantic model
        data = {
            **obj.__dict__,
            "is_connected": obj.is_connected
        }
        return cls(**data)

# Schema for social post
class SocialPostBase(BaseModel):
    content: str
    platform: SocialPlatform
    status: str = "draft"
    scheduled_for: Optional[datetime] = None
    media_urls: List[HttpUrl] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class SocialPostCreate(SocialPostBase):
    social_account_id: int
    agent_id: Optional[int] = None

class SocialPostUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    media_urls: Optional[List[HttpUrl]] = None
    metadata: Optional[Dict[str, Any]] = None

class SocialPostInDBBase(SocialPostBase):
    id: int
    external_post_id: Optional[str] = None
    social_account_id: int
    agent_id: Optional[int] = None
    published_at: Optional[datetime] = None
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    view_count: int = 0
    url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SocialPost(SocialPostInDBBase):
    pass

# Schema for agent social account connection
class AgentSocialAccountBase(BaseModel):
    agent_id: int
    social_account_id: int
    config: Dict[str, Any] = Field(default_factory=dict)

class AgentSocialAccountCreate(AgentSocialAccountBase):
    pass

class AgentSocialAccountUpdate(BaseModel):
    config: Optional[Dict[str, Any]] = None

class AgentSocialAccountInDBBase(AgentSocialAccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AgentSocialAccount(AgentSocialAccountInDBBase):
    pass
