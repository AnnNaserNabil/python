from typing import List, Dict, Any, Optional
import numpy as np
from enum import Enum
import logging

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class VectorStoreType(str, Enum):
    POSTGRES = "postgres"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"

class VectorStore:
    """
    A unified interface for different vector store backends.
    """
    def __init__(self, store_type: str = None):
        self.store_type = store_type or settings.VECTOR_STORE_TYPE
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate vector store client."""
        try:
            if self.store_type == VectorStoreType.POSTGRES:
                return self._init_postgres()
            elif self.store_type == VectorStoreType.PINECONE:
                return self._init_pinecone()
            elif self.store_type == VectorStoreType.WEAVIATE:
                return self._init_weaviate()
            else:
                raise ValueError(f"Unsupported vector store type: {self.store_type}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise
    
    def _init_postgres(self):
        """Initialize PostgreSQL with pgvector."""
        try:
            import psycopg2
            from pgvector.psycopg2 import register_vector
            
            conn = psycopg2.connect(settings.POSTGRES_VECTOR_DB_URL or settings.DATABASE_URL)
            register_vector(conn)
            return conn
        except ImportError:
            raise ImportError("pgvector and psycopg2-binary are required for PostgreSQL vector store")
    
    def _init_pinecone(self):
        """Initialize Pinecone client."""
        try:
            import pinecone
            
            if not settings.PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY is required for Pinecone vector store")
            
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT or "us-west1-gcp"
            )
            return pinecone
        except ImportError:
            raise ImportError("pinecone-client is required for Pinecone vector store")
    
    def _init_weaviate(self):
        """Initialize Weaviate client."""
        try:
            import weaviate
            
            if not settings.WEAVIATE_URL:
                raise ValueError("WEAVIATE_URL is required for Weaviate vector store")
            
            return weaviate.Client(settings.WEAVIATE_URL)
        except ImportError:
            raise ImportError("weaviate-client is required for Weaviate vector store")
    
    async def create_collection(self, name: str, dimensions: int, **kwargs):
        """Create a new vector collection."""
        if self.store_type == VectorStoreType.POSTGRES:
            with self.client.cursor() as cur:
                # Create table if it doesn't exist
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {name} (
                        id SERIAL PRIMARY KEY,
                        vector vector({dimensions}),
                        metadata JSONB,
                        document_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.client.commit()
        elif self.store_type == VectorStoreType.PINECONE:
            # Pinecone creates indexes, not collections
            if not self.client.list_indexes():
                self.client.create_index(
                    name=name,
                    dimension=dimensions,
                    metric="cosine"
                )
        elif self.store_type == VectorStoreType.WEAVIATE:
            schema = {
                "class": name,
                "vectorizer": "none",  # We'll provide our own vectors
                "properties": [
                    {"name": "document_id", "dataType": ["text"]},
                    {"name": "metadata", "dataType": ["object"]},
                ]
            }
            self.client.schema.create_class(schema)
    
    async def add_vectors(self, collection: str, vectors: List[Dict[str, Any]]):
        """Add vectors to a collection."""
        if self.store_type == VectorStoreType.POSTGRES:
            with self.client.cursor() as cur:
                for vec in vectors:
                    cur.execute(
                        f"""
                        INSERT INTO {collection} (vector, metadata, document_id)
                        VALUES (%s, %s, %s)
                        """,
                        (np.array(vec['vector']).tobytes(), vec.get('metadata'), vec.get('document_id'))
                    )
                self.client.commit()
        elif self.store_type == VectorStoreType.PINECONE:
            index = self.client.Index(collection)
            # Pinecone expects a list of (id, vector, metadata) tuples
            items = [
                (
                    vec.get('id', str(i)),
                    vec['vector'],
                    {**vec.get('metadata', {}), 'document_id': vec.get('document_id')}
                )
                for i, vec in enumerate(vectors)
            ]
            index.upsert(vectors=items)
        elif self.store_type == VectorStoreType.WEAVIATE:
            with self.client.batch as batch:
                for vec in vectors:
                    data_object = {
                        'document_id': vec.get('document_id'),
                        'metadata': vec.get('metadata', {})
                    }
                    batch.add_data_object(
                        data_object=data_object,
                        class_name=collection,
                        vector=vec['vector']
                    )
    
    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        top_k: int = 5,
        filter_conditions: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        if self.store_type == VectorStoreType.POSTGRES:
            with self.client.cursor() as cur:
                # Convert query vector to bytes for pgvector
                query_vec = np.array(query_vector).tobytes()
                
                # Build the WHERE clause for filtering
                where_clause = ""
                params = [query_vec, top_k]
                
                if filter_conditions:
                    conditions = []
                    for i, (key, value) in enumerate(filter_conditions.items()):
                        param_idx = len(params) + 1
                        conditions.append(f"metadata->>%s = %s")
                        params.extend([key, str(value)])
                    where_clause = "WHERE " + " AND ".join(conditions)
                
                # Execute the query
                query = f"""
                    SELECT id, vector, metadata, document_id, 
                           1 - (vector <=> %s) as similarity
                    FROM {collection}
                    {where_clause}
                    ORDER BY vector <=> %s
                    LIMIT %s
                """
                
                cur.execute(query, [query_vec, query_vec, top_k])
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'id': row[0],
                        'vector': np.frombuffer(row[1], dtype=np.float32).tolist(),
                        'metadata': row[2],
                        'document_id': row[3],
                        'similarity': float(row[4])
                    })
                
                return results
                
        elif self.store_type == VectorStoreType.PINECONE:
            index = self.client.Index(collection)
            
            # Build filter
            filter_dict = {}
            if filter_conditions:
                filter_dict = {
                    key: {"$eq": value}
                    for key, value in filter_conditions.items()
                }
            
            query_result = index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict or None
            )
            
            return [
                {
                    'id': match.id,
                    'vector': match.vector,
                    'metadata': match.metadata,
                    'document_id': match.metadata.get('document_id'),
                    'similarity': match.score
                }
                for match in query_result.matches
            ]
            
        elif self.store_type == VectorStoreType.WEAVIATE:
            # Build filter
            filter_dict = {"operator": "And", "operands": []}
            if filter_conditions:
                for key, value in filter_conditions.items():
                    filter_dict["operands"].append({
                        "path": ["metadata", key],
                        "operator": "Equal",
                        "valueString": str(value)
                    })
            
            query = (
                self.client.query
                .get(collection, ["document_id", "metadata"])
                .with_near_vector({"vector": query_vector})
                .with_limit(top_k)
            )
            
            if filter_conditions:
                query = query.with_where(filter_dict)
            
            result = query.do()
            
            return [
                {
                    'id': item['_additional']['id'],
                    'vector': item['_additional']['vector'],
                    'metadata': item.get('metadata', {}),
                    'document_id': item.get('document_id'),
                    'similarity': 1.0 - item['_additional']['distance']
                }
                for item in result['data']['Get'][collection]
            ]
    
    async def delete_vectors(self, collection: str, vector_ids: List[str]):
        """Delete vectors by their IDs."""
        if not vector_ids:
            return
            
        if self.store_type == VectorStoreType.POSTGRES:
            with self.client.cursor() as cur:
                placeholders = ",".join("%s" for _ in vector_ids)
                cur.execute(
                    f"DELETE FROM {collection} WHERE id IN ({placeholders})",
                    vector_ids
                )
                self.client.commit()
                
        elif self.store_type == VectorStoreType.PINECONE:
            index = self.client.Index(collection)
            index.delete(ids=vector_ids)
            
        elif self.store_type == VectorStoreType.WEAVIATE:
            for vec_id in vector_ids:
                self.client.data_object.delete(
                    uuid=vec_id,
                    class_name=collection
                )
    
    async def get_collection_stats(self, collection: str) -> Dict[str, Any]:
        """Get statistics about a collection."""
        if self.store_type == VectorStoreType.POSTGRES:
            with self.client.cursor() as cur:
                cur.execute(f"""
                    SELECT 
                        COUNT(*) as count,
                        pg_size_pretty(pg_total_relation_size(%s)) as size
                    FROM {collection}
                """, (collection,))
                result = cur.fetchone()
                return {"count": result[0], "size": result[1]}
                
        elif self.store_type == VectorStoreType.PINECONE:
            index = self.client.Index(collection)
            desc = index.describe_index_stats()
            return {
                "count": desc['total_vector_count'],
                "dimensions": desc['dimension'],
                "index_fullness": desc.get('index_fullness'),
                "namespaces": desc.get('namespaces', {})
            }
            
        elif self.store_type == VectorStoreType.WEAVIATE:
            stats = self.client.query.aggregate(collection).with_meta_count().do()
            return {
                "count": stats['data']['Aggregate'][collection][0]['meta']['count'],
                "class_name": collection
            }

# Global vector store instance
vector_store = VectorStore()
