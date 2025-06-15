from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from app.schemas.user import UserResponse

class AgentType(str, Enum):
    CONTENT_GENERATOR = "content_generator"
    ANALYTICS = "analytics"
    ENGAGEMENT = "engagement"
    SCHEDULER = "scheduler"
    CUSTOM = "custom"

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"

# Base schema
class AgentBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    agent_type: AgentType = AgentType.CUSTOM
    status: AgentStatus = AgentStatus.INACTIVE
    config: Dict[str, Any] = Field(default_factory=dict)

# Schema for creating a new agent
class AgentCreate(AgentBase):
    pass

# Schema for updating an agent
class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    config: Optional[Dict[str, Any]] = None

# Schema for agent in database
class AgentInDBBase(AgentBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for returning agent data via API
class Agent(AgentInDBBase):
    pass

# Schema for agent with relationships
class AgentWithRelations(AgentInDBBase):
    owner: UserResponse
    
    class Config:
        from_attributes = True

# Schema for agent execution
class AgentExecutionBase(BaseModel):
    agent_id: int
    status: str
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class AgentExecutionCreate(AgentExecutionBase):
    pass

class AgentExecutionUpdate(BaseModel):
    status: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AgentExecutionInDBBase(AgentExecutionBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AgentExecution(AgentExecutionInDBBase):
    pass

# Schema for agent execution task
class AgentExecutionTaskBase(BaseModel):
    execution_id: int
    task_type: str
    status: str
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class AgentExecutionTaskCreate(AgentExecutionTaskBase):
    pass

class AgentExecutionTaskUpdate(BaseModel):
    status: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None

class AgentExecutionTaskInDBBase(AgentExecutionTaskBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AgentExecutionTask(AgentExecutionTaskInDBBase):
    pass
