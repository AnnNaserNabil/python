from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.models.base import Base

class SocialPlatform(str, enum.Enum):
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

class SocialAccountStatus(str, enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    REFRESHING = "refreshing"

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(Enum(SocialPlatform), nullable=False)
    display_name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Authentication and connection details
    access_token = Column(String(500), nullable=True)
    refresh_token = Column(String(500), nullable=True)
    token_expiry = Column(DateTime(timezone=True), nullable=True)
    external_id = Column(String(255), nullable=False)
    
    # Account status
    status = Column(Enum(SocialAccountStatus), default=SocialAccountStatus.CONNECTED)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    
    # Additional metadata
    metadata_ = Column("metadata", JSON, default={})
    
    # Owner of this social account connection
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="social_accounts")
    
    # Token refresh information
    token_refresh_attempts = Column(Integer, default=0)
    last_token_refresh_attempt = Column(DateTime(timezone=True), nullable=True)
    token_refresh_error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agent_connections = relationship("AgentSocialAccount", back_populates="social_account")
    posts = relationship("SocialPost", back_populates="social_account")
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<SocialAccount {self.platform}:{self.username or self.email}>"
    
    @property
    def is_connected(self):
        return self.status == SocialAccountStatus.CONNECTED
    
    @property
    def needs_token_refresh(self):
        if not self.token_expiry or not self.refresh_token:
            return False
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) >= self.token_expiry

class SocialPost(Base):
    __tablename__ = "social_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    external_post_id = Column(String(255), nullable=True, index=True)
    content = Column(Text, nullable=False)
    platform = Column(Enum(SocialPlatform), nullable=False)
    
    # Status tracking
    status = Column(String(50), default="draft")  draft, scheduled, published, failed, deleted
    
    # Scheduling
    scheduled_for = Column(DateTime(timezone=True), nullable=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Engagement metrics
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # Links and media
    url = Column(String(500), nullable=True)
    media_urls = Column(JSON, default=list)
    
    # Relationships
    social_account_id = Column(Integer, ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False)
    social_account = relationship("SocialAccount", back_populates="posts")
    
    # Agent that created this post (if any)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    agent = relationship("Agent")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<SocialPost {self.id} ({self.platform}): {self.content[:50]}...>"
