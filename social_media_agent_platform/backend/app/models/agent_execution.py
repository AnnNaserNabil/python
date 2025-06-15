from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Boolean, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.models.base import Base

class ExecutionStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reference to the agent
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    agent = relationship("Agent", back_populates="executions")
    
    # Execution details
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Performance metrics
    duration_seconds = Column(Float, nullable=True)
    memory_usage_mb = Column(Float, nullable=True)
    cpu_usage_percent = Column(Float, nullable=True)
    
    # Input and output
    input_parameters = Column(JSON, default={}, nullable=False)
    output_data = Column(JSON, nullable=True)
    
    # Error information
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)
    
    # Metadata
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tasks = relationship("AgentExecutionTask", back_populates="execution", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AgentExecution {self.id} - {self.agent.name} ({self.status})>"
    
    @property
    def is_running(self):
        return self.status == ExecutionStatus.RUNNING
    
    @property
    def is_completed(self):
        return self.status == ExecutionStatus.COMPLETED
    
    @property
    def is_failed(self):
        return self.status == ExecutionStatus.FAILED

class AgentExecutionTask(Base):
    __tablename__ = "agent_execution_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reference to the execution
    execution_id = Column(Integer, ForeignKey("agent_executions.id", ondelete="CASCADE"), nullable=False)
    execution = relationship("AgentExecution", back_populates="tasks")
    
    # Task details
    task_type = Column(String(100), nullable=False)  # e.g., "fetch_data", "process_data", "post_update"
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Input and output
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    
    # Error information
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)
    
    # Metadata
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AgentExecutionTask {self.id} - {self.task_type} ({self.status})>"
