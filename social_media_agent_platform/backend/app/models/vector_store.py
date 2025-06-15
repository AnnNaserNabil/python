from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
import json

from app.models.base import Base

class VectorCollection(Base):
    __tablename__ = "vector_collections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Configuration
    dimensions = Column(Integer, nullable=False)  # Vector dimensions
    distance_metric = Column(String(50), default="cosine")  # cosine, euclidean, dot
    
    # Metadata
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    
    # Owner (if user-specific)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vectors = relationship("Vector", back_populates="collection", cascade="all, delete-orphan")
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<VectorCollection {self.name} (dim={self.dimensions})>"

class Vector(Base):
    __tablename__ = "vectors"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reference to collection
    collection_id = Column(Integer, ForeignKey("vector_collections.id", ondelete="CASCADE"), nullable=False)
    collection = relationship("VectorCollection", back_populates="vectors")
    
    # The actual vector data (stored as JSON for flexibility)
    vector_data = Column(JSON, nullable=False)
    
    # Metadata
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    
    # Reference to the source document (if any)
    document_id = Column(String(255), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __init__(self, **kwargs):
        # Convert numpy array or list to JSON-serializable format if needed
        if 'vector_data' in kwargs and not isinstance(kwargs['vector_data'], (list, dict, str, int, float, bool, type(None))):
            kwargs['vector_data'] = kwargs['vector_data'].tolist() if hasattr(kwargs['vector_data'], 'tolist') else list(kwargs['vector_data'])
        super().__init__(**kwargs)
    
    @property
    def vector(self):
        """Get the vector as a list of floats."""
        return self.vector_data if isinstance(self.vector_data, list) else json.loads(self.vector_data)
    
    def __repr__(self):
        return f"<Vector {self.id} in {self.collection.name}>"

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reference to the original document
    document_id = Column(String(255), nullable=False, index=True)
    
    # Chunk details
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    
    # Embedding reference
    vector_id = Column(Integer, ForeignKey("vectors.id", ondelete="SET NULL"), nullable=True)
    
    # Metadata
    metadata_ = Column("metadata", JSON, default={}, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vector = relationship("Vector", foreign_keys=[vector_id])
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<DocumentChunk {self.document_id}[{self.chunk_index}]>"
