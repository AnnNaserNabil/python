from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.models.base import Base

class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"

class AgentType(str, enum.Enum):
    CONTENT_GENERATOR = "content_generator"
    ANALYTICS = "analytics"
    ENGAGEMENT = "engagement"
    SCHEDULER = "scheduler"
    CUSTOM = "custom"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    agent_type = Column(Enum(AgentType), nullable=False, default=AgentType.CUSTOM)
    status = Column(Enum(AgentStatus), default=AgentStatus.INACTIVE)
    
    # Configuration for the agent
    config = Column(JSON, default={})
    
    # Owner of the agent
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="agents")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    social_accounts = relationship("AgentSocialAccount", back_populates="agent")
    executions = relationship("AgentExecution", back_populates="agent")
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.agent_type})>"

class AgentSocialAccount(Base):
    __tablename__ = "agent_social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False)
    
    # Additional configuration specific to this agent's use of the social account
    config = Column(JSON, default={})
    
    # Relationships
    agent = relationship("Agent", back_populates="social_accounts")
    social_account = relationship("SocialAccount", back_populates="agent_connections")
    
    def __repr__(self):
        return f"<AgentSocialAccount agent_id={self.agent_id}, social_account_id={self.social_account_id}>"
