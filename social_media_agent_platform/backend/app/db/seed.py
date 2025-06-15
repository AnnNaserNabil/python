import logging
from typing import List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base, SessionLocal, engine
from app.models.user import User
from app.models.agent import Agent
from app.models.social_account import SocialAccount
from app.models.social_post import SocialPost
from app.models.vector_store import VectorCollection, Vector, DocumentChunk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """Initialize the database with test data."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create test user if it doesn't exist
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = {
            "email": settings.FIRST_SUPERUSER,
            "hashed_password": get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            "full_name": "Admin User",
            "is_superuser": True,
            "is_active": True,
        }
        user = User(**user_in)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("Created superuser: %s", user.email)
    
    # Create test agent
    agent = db.query(Agent).filter(Agent.name == "Test Agent").first()
    if not agent:
        agent_in = {
            "name": "Test Agent",
            "description": "A test agent for development",
            "config": {"model": "gpt-4", "temperature": 0.7},
            "user_id": user.id,
            "is_active": True,
        }
        agent = Agent(**agent_in)
        db.add(agent)
        db.commit()
        db.refresh(agent)
        logger.info("Created test agent: %s", agent.name)
    
    # Create test social account
    social_account = db.query(SocialAccount).filter(SocialAccount.platform_username == "test_user").first()
    if not social_account:
        social_account_in = {
            "platform": "twitter",
            "platform_user_id": "1234567890",
            "platform_username": "test_user",
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_expires_at": None,
            "user_id": user.id,
            "is_active": True,
        }
        social_account = SocialAccount(**social_account_in)
        db.add(social_account)
        db.commit()
        db.refresh(social_account)
        logger.info("Created test social account: %s", social_account.platform_username)
    
    # Create test vector collection
    collection = db.query(VectorCollection).filter(VectorCollection.name == "test_collection").first()
    if not collection:
        collection_in = {
            "name": "test_collection",
            "description": "A test vector collection",
            "dimensions": 1536,  # OpenAI embeddings dimension
            "user_id": user.id,
        }
        collection = VectorCollection(**collection_in)
        db.add(collection)
        db.commit()
        db.refresh(collection)
        logger.info("Created test vector collection: %s", collection.name)
        
        # Add some test vectors
        test_vectors = [
            {
                "collection_id": collection.id,
                "vector": [0.1] * 1536,  # Dummy vector
                "metadata": {"source": "test_source_1", "type": "test"},
            },
            {
                "collection_id": collection.id,
                "vector": [0.2] * 1536,  # Dummy vector
                "metadata": {"source": "test_source_2", "type": "test"},
            },
        ]
        
        for vector_data in test_vectors:
            vector = Vector(**vector_data)
            db.add(vector)
        db.commit()
        logger.info("Added test vectors to collection")
        
        # Add some test document chunks
        test_chunks = [
            {
                "collection_id": collection.id,
                "content": "This is a test document chunk 1",
                "metadata": {"source": "test_doc_1.txt", "page": 1},
            },
            {
                "collection_id": collection.id,
                "content": "This is a test document chunk 2",
                "metadata": {"source": "test_doc_1.txt", "page": 2},
            },
        ]
        
        for chunk_data in test_chunks:
            chunk = DocumentChunk(**chunk_data)
            db.add(chunk)
        db.commit()
        logger.info("Added test document chunks to collection")

def main() -> None:
    """Main function to initialize the database."""
    logger.info("Creating initial data")
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        logger.error("Error initializing database: %s", e)
        raise
    finally:
        db.close()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
