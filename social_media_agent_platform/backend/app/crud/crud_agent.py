from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.base import CRUDBase

class CRUDAgent(CRUDBase[models.Agent, schemas.AgentCreate, schemas.AgentUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Agent]:
        return (
            db.query(self.model)
            .filter(models.Agent.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_name_and_owner(
        self, db: Session, *, name: str, owner_id: int
    ) -> Optional[models.Agent]:
        return (
            db.query(self.model)
            .filter(
                models.Agent.name == name,
                models.Agent.owner_id == owner_id
            )
            .first()
        )
    
    def create_with_owner(
        self, db: Session, *, obj_in: schemas.AgentCreate, owner_id: int
    ) -> models.Agent:
        db_obj = models.Agent(
            **obj_in.dict(exclude_unset=True),
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_status(
        self, db: Session, *, db_obj: models.Agent, status: schemas.AgentStatus
    ) -> models.Agent:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def log_execution(
        self, db: Session, *, agent_id: int, execution_data: Dict[str, Any]
    ) -> models.AgentExecution:
        execution = models.AgentExecution(
            agent_id=agent_id,
            **execution_data
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution

agent = CRUDAgent(models.Agent)
