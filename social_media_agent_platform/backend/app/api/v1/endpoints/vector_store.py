from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import numpy as np

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

# Vector Collection Endpoints
@router.post("/collections/", response_model=schemas.VectorCollection)
def create_collection(
    *,
    db: Session = Depends(deps.get_db),
    collection_in: schemas.VectorCollectionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new vector collection.
    """
    # Check if a collection with this name already exists for the user
    collection = crud.vector_collection.get_by_name(
        db, name=collection_in.name, owner_id=current_user.id
    )
    if collection:
        raise HTTPException(
            status_code=400,
            detail="A collection with this name already exists for this user.",
        )
    
    # Create the collection
    collection = crud.vector_collection.create_with_owner(
        db=db, obj_in=collection_in, owner_id=current_user.id
    )
    return collection

@router.get("/collections/", response_model=List[schemas.VectorCollection])
def read_collections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve vector collections for the current user.
    """
    collections = crud.vector_collection.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    
    # Add vector count to each collection
    for collection in collections:
        collection.vector_count = len(collection.vectors)
    
    return collections

@router.get("/collections/{collection_id}", response_model=schemas.VectorCollection)
def read_collection(
    *,
    db: Session = Depends(deps.get_db),
    collection_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific vector collection by ID.
    """
    collection = crud.vector_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Check if the current user is the owner of the collection
    if collection.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Add vector count
    collection.vector_count = len(collection.vectors)
    
    return collection

# Vector Endpoints
@router.post("/collections/{collection_id}/vectors/", response_model=schemas.Vector)
def create_vector(
    *,
    db: Session = Depends(deps.get_db),
    collection_id: int,
    vector_in: schemas.VectorCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a vector to a collection.
    """
    # Check if the collection exists and belongs to the user
    collection = crud.vector_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if the vector dimensions match the collection dimensions
    if len(vector_in.vector_data) != collection.dimensions:
        raise HTTPException(
            status_code=400,
            detail=f"Vector dimensions ({len(vector_in.vector_data)}) do not match collection dimensions ({collection.dimensions})",
        )
    
    # Check if a vector with this document_id already exists in the collection
    if vector_in.document_id:
        existing_vector = crud.vector.get_by_document_id(
            db, collection_id=collection_id, document_id=vector_in.document_id
        )
        if existing_vector:
            raise HTTPException(
                status_code=400,
                detail="A vector with this document_id already exists in this collection",
            )
    
    # Create the vector
    vector = crud.vector.create(
        db=db, obj_in=vector_in
    )
    
    return vector

@router.get("/collections/{collection_id}/vectors/", response_model=List[schemas.Vector])
def read_vectors(
    *,
    db: Session = Depends(deps.get_db),
    collection_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve vectors from a collection.
    """
    # Check if the collection exists and belongs to the user
    collection = crud.vector_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Get vectors from the collection
    vectors = crud.vector.get_multi_by_collection(
        db, collection_id=collection_id, skip=skip, limit=limit
    )
    
    return vectors

@router.post("/collections/{collection_id}/search/", response_model=schemas.SearchResults)
def search_vectors(
    *,
    db: Session = Depends(deps.get_db),
    collection_id: int,
    query: schemas.VectorQuery,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search for similar vectors in a collection.
    """
    # Check if the collection exists and belongs to the user
    collection = crud.vector_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if the query vector dimensions match the collection dimensions
    if len(query.query_vector) != collection.dimensions:
        raise HTTPException(
            status_code=400,
            detail=f"Query vector dimensions ({len(query.query_vector)}) do not match collection dimensions ({collection.dimensions})",
        )
    
    # Search for similar vectors
    similar_vectors = crud.vector.search_similar(
        db,
        collection_id=collection_id,
        query_vector=query.query_vector,
        top_k=query.top_k,
        filter_conditions=query.filter_conditions,
    )
    
    # Format the results
    results = []
    for vector, distance in similar_vectors:
        # In a real implementation, you might want to include more information
        # about each result, such as the associated document chunk
        result = schemas.SearchResult(
            vector=vector,
            distance=float(distance),
        )
        results.append(result)
    
    return schemas.SearchResults(
        results=results,
        total=len(results),
    )

# Document Chunk Endpoints
@router.post("/documents/", response_model=schemas.DocumentChunk)
def create_document_chunk(
    *,
    db: Session = Depends(deps.get_db),
    chunk_in: schemas.DocumentChunkCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new document chunk with an optional vector embedding.
    """
    # If a collection_id is provided, verify it exists and belongs to the user
    if chunk_in.collection_id:
        collection = crud.vector_collection.get(db, id=chunk_in.collection_id)
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        if collection.owner_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        
        # If vector_data is provided, ensure it matches the collection dimensions
        if chunk_in.vector_data and len(chunk_in.vector_data) != collection.dimensions:
            raise HTTPException(
                status_code=400,
                detail=f"Vector dimensions ({len(chunk_in.vector_data)}) do not match collection dimensions ({collection.dimensions})",
            )
    
    # Create the document chunk
    chunk = crud.document_chunk.create_with_embedding(
        db=db,
        obj_in=chunk_in,
        collection_id=chunk_in.collection_id,
        vector_data=chunk_in.vector_data or [],
    )
    
    return chunk

@router.get("/documents/{document_id}/chunks/", response_model=List[schemas.DocumentChunk])
def read_document_chunks(
    *,
    db: Session = Depends(deps.get_db),
    document_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve chunks for a specific document.
    """
    # In a real implementation, you would check if the user has access to this document
    # For now, we'll just return the chunks
    chunks = crud.document_chunk.get_by_document(
        db, document_id=document_id, skip=skip, limit=limit
    )
    
    return chunks
