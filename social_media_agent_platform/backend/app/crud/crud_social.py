from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.base import CRUDBase

class CRUDSocialAccount(CRUDBase[models.SocialAccount, schemas.SocialAccountCreate, schemas.SocialAccountUpdate]):
    def get_by_platform_and_external_id(
        self, db: Session, *, platform: str, external_id: str
    ) -> Optional[models.SocialAccount]:
        return (
            db.query(self.model)
            .filter(
                models.SocialAccount.platform == platform,
                models.SocialAccount.external_id == external_id
            )
            .first()
        )
    
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.SocialAccount]:
        return (
            db.query(self.model)
            .filter(models.SocialAccount.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_platform(
        self, db: Session, *, owner_id: int, platform: str
    ) -> List[models.SocialAccount]:
        return (
            db.query(self.model)
            .filter(
                models.SocialAccount.owner_id == owner_id,
                models.SocialAccount.platform == platform
            )
            .all()
        )
    
    def update_status(
        self, db: Session, *, db_obj: models.SocialAccount, status: str
    ) -> models.SocialAccount:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_tokens(
        self,
        db: Session,
        *,
        db_obj: models.SocialAccount,
        access_token: str,
        refresh_token: Optional[str] = None,
        token_expiry: Optional[int] = None
    ) -> models.SocialAccount:
        db_obj.access_token = access_token
        if refresh_token:
            db_obj.refresh_token = refresh_token
        if token_expiry:
            db_obj.token_expiry = token_expiry
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDSocialPost(CRUDBase[models.SocialPost, schemas.SocialPostCreate, schemas.SocialPostUpdate]):
    def get_multi_by_account(
        self, db: Session, *, account_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.SocialPost]:
        return (
            db.query(self.model)
            .filter(models.SocialPost.social_account_id == account_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_agent(
        self, db: Session, *, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.SocialPost]:
        return (
            db.query(self.model)
            .filter(models.SocialPost.agent_id == agent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_external_id(
        self, db: Session, *, external_id: str, platform: str
    ) -> Optional[models.SocialPost]:
        return (
            db.query(self.model)
            .filter(
                models.SocialPost.external_post_id == external_id,
                models.SocialPost.platform == platform
            )
            .first()
        )

class CRUDAgentSocialAccount(CRUDBase[
    models.AgentSocialAccount,
    schemas.AgentSocialAccountCreate,
    schemas.AgentSocialAccountUpdate
]):
    def get_by_agent_and_social_account(
        self, db: Session, *, agent_id: int, social_account_id: int
    ) -> Optional[models.AgentSocialAccount]:
        return (
            db.query(self.model)
            .filter(
                models.AgentSocialAccount.agent_id == agent_id,
                models.AgentSocialAccount.social_account_id == social_account_id
            )
            .first()
        )
    
    def get_multi_by_agent(
        self, db: Session, *, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.AgentSocialAccount]:
        return (
            db.query(self.model)
            .filter(models.AgentSocialAccount.agent_id == agent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_social_account(
        self, db: Session, *, social_account_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.AgentSocialAccount]:
        return (
            db.query(self.model)
            .filter(models.AgentSocialAccount.social_account_id == social_account_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

social_account = CRUDSocialAccount(models.SocialAccount)
social_post = CRUDSocialPost(models.SocialPost)
agent_social_account = CRUDAgentSocialAccount(models.AgentSocialAccount)
