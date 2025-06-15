from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field

# Vector collection schemas
class VectorCollectionBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    dimensions: int
    distance_metric: str = "cosine"
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class VectorCollectionCreate(VectorCollectionBase):
    pass

class VectorCollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class VectorCollectionInDBBase(VectorCollectionBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class VectorCollection(VectorCollectionInDBBase):
    vector_count: int = 0

# Vector schemas
class VectorBase(BaseModel):
    vector_data: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")
    document_id: Optional[str] = None

class VectorCreate(VectorBase):
    collection_id: int

class VectorUpdate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    document_id: Optional[str] = None

class VectorInDBBase(VectorBase):
    id: int
    collection_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Vector(VectorInDBBase):
    pass

# Document chunk schemas
class DocumentChunkBase(BaseModel):
    document_id: str
    chunk_index: int
    chunk_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class DocumentChunkCreate(DocumentChunkBase):
    vector_data: Optional[List[float]] = None
    collection_id: Optional[int] = None

class DocumentChunkUpdate(BaseModel):
    chunk_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentChunkInDBBase(DocumentChunkBase):
    id: int
    vector_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DocumentChunk(DocumentChunkInDBBase):
    vector: Optional[Vector] = None

# Query schemas
class VectorQuery(BaseModel):
    query_vector: List[float]
    top_k: int = 5
    filter_conditions: Optional[Dict[str, Any]] = None

class TextQuery(BaseModel):
    query_text: str
    top_k: int = 5
    filter_conditions: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    vector: Vector
    distance: float
    chunk: Optional[DocumentChunk] = None

class SearchResults(BaseModel):
    results: List[SearchResult]
    total: int

# Document schemas
class DocumentBase(BaseModel):
    document_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_")

class DocumentCreate(DocumentBase):
    chunks: Optional[List[DocumentChunkCreate]] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentInDBBase(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Document(DocumentInDBBase):
    chunks: List[DocumentChunk] = []
