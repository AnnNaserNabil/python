from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, Type
from uuid import UUID
import json

from sqlalchemy.orm import Session
import numpy as np

from app import models, schemas
from app.crud.base import CRUDBase

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=schemas.BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=schemas.BaseModel)

class CRUDVectorCollection(CRUDBase[
    models.VectorCollection, 
    schemas.VectorCollectionCreate, 
    schemas.VectorCollectionUpdate
]):
    def get_by_name(
        self, db: Session, *, name: str, owner_id: Optional[int] = None
    ) -> Optional[models.VectorCollection]:
        query = db.query(self.model).filter(models.VectorCollection.name == name)
        if owner_id is not None:
            query = query.filter(models.VectorCollection.owner_id == owner_id)
        return query.first()
    
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.VectorCollection]:
        return (
            db.query(self.model)
            .filter(models.VectorCollection.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_with_owner(
        self, db: Session, *, obj_in: schemas.VectorCollectionCreate, owner_id: int
    ) -> models.VectorCollection:
        db_obj = models.VectorCollection(
            **obj_in.dict(exclude_unset=True),
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDVector(CRUDBase[models.Vector, schemas.VectorCreate, schemas.VectorUpdate]):
    def get_multi_by_collection(
        self, db: Session, *, collection_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Vector]:
        return (
            db.query(self.model)
            .filter(models.Vector.collection_id == collection_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_document_id(
        self, db: Session, *, collection_id: int, document_id: str
    ) -> Optional[models.Vector]:
        return (
            db.query(self.model)
            .filter(
                models.Vector.collection_id == collection_id,
                models.Vector.document_id == document_id
            )
            .first()
        )
    
    def search_similar(
        self,
        db: Session,
        *,
        collection_id: int,
        query_vector: List[float],
        top_k: int = 5,
        filter_conditions: Optional[Dict[str, Any]] = None,
    ) -> List[models.Vector]:
        # This is a simplified version. In production, you'd want to use a vector database
        # like Pinecone, Weaviate, or pgvector for efficient similarity search
        
        # Get all vectors in the collection
        vectors = self.get_multi_by_collection(db, collection_id=collection_id, limit=1000)  # Adjust limit as needed
        
        # Simple cosine similarity (for demonstration)
        def cosine_similarity(a, b):
            a_norm = np.linalg.norm(a)
            b_norm = np.linalg.norm(b)
            if a_norm == 0 or b_norm == 0:
                return 0.0
            return np.dot(a, b) / (a_norm * b_norm)
        
        # Calculate similarities
        query_vector_np = np.array(query_vector)
        similarities = []
        for vector in vectors:
            vec = np.array(vector.vector_data)
            if len(vec) != len(query_vector_np):
                continue  # Skip vectors with different dimensions
            
            # Apply filter conditions if any
            if filter_conditions:
                match = True
                for key, value in filter_conditions.items():
                    if key not in vector.metadata_ or vector.metadata_[key] != value:
                        match = False
                        break
                if not match:
                    continue
            
            sim = cosine_similarity(query_vector_np, vec)
            similarities.append((vector, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        return [vec for vec, _ in similarities[:top_k]]

class CRUDDocumentChunk(CRUDBase[
    models.DocumentChunk,
    schemas.DocumentChunkCreate,
    schemas.DocumentChunkUpdate
]):
    def get_by_document(
        self, db: Session, *, document_id: str, skip: int = 0, limit: int = 100
    ) -> List[models.DocumentChunk]:
        return (
            db.query(self.model)
            .filter(models.DocumentChunk.document_id == document_id)
            .order_by(models.DocumentChunk.chunk_index)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_document_and_index(
        self, db: Session, *, document_id: str, chunk_index: int
    ) -> Optional[models.DocumentChunk]:
        return (
            db.query(self.model)
            .filter(
                models.DocumentChunk.document_id == document_id,
                models.DocumentChunk.chunk_index == chunk_index
            )
            .first()
        )
    
    def create_with_embedding(
        self,
        db: Session,
        *,
        obj_in: schemas.DocumentChunkCreate,
        collection_id: int,
        vector_data: List[float],
    ) -> models.DocumentChunk:
        # Create the chunk
        chunk = models.DocumentChunk(**obj_in.dict(exclude={"vector_data"}, exclude_unset=True))
        db.add(chunk)
        db.commit()
        db.refresh(chunk)
        
        # Create the vector
        vector = models.Vector(
            collection_id=collection_id,
            vector_data=vector_data,
            document_id=f"{obj_in.document_id}:{obj_in.chunk_index}",
            metadata_={"chunk_id": chunk.id, "document_id": obj_in.document_id}
        )
        db.add(vector)
        db.commit()
        
        # Update chunk with vector reference
        chunk.vector_id = vector.id
        db.add(chunk)
        db.commit()
        db.refresh(chunk)
        
        return chunk

vector_collection = CRUDVectorCollection(models.VectorCollection)
vector = CRUDVector(models.Vector)
document_chunk = CRUDDocumentChunk(models.DocumentChunk)
