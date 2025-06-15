from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.Agent)
def create_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_in: schemas.AgentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new agent.
    """
    # Check if agent with this name already exists for the user
    agent = crud.agent.get_by_name_and_owner(
        db, name=agent_in.name, owner_id=current_user.id
    )
    if agent:
        raise HTTPException(
            status_code=400,
            detail="An agent with this name already exists for this user.",
        )
    
    # Create the agent
    agent = crud.agent.create_with_owner(
        db=db, obj_in=agent_in, owner_id=current_user.id
    )
    return agent

@router.get("/", response_model=List[schemas.Agent])
def read_agents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve agents for the current user.
    """
    agents = crud.agent.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return agents

@router.get("/{agent_id}", response_model=schemas.Agent)
def read_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get agent by ID.
    """
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if the current user is the owner of the agent
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return agent

@router.put("/{agent_id}", response_model=schemas.Agent)
def update_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    agent_in: schemas.AgentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an agent.
    """
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if the current user is the owner of the agent
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if the new name is already taken
    if agent_in.name and agent_in.name != agent.name:
        existing_agent = crud.agent.get_by_name_and_owner(
            db, name=agent_in.name, owner_id=current_user.id
        )
        if existing_agent and existing_agent.id != agent_id:
            raise HTTPException(
                status_code=400,
                detail="An agent with this name already exists for this user.",
            )
    
    agent = crud.agent.update(db, db_obj=agent, obj_in=agent_in)
    return agent

@router.delete("/{agent_id}", response_model=schemas.Agent)
def delete_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an agent.
    """
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if the current user is the owner of the agent
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    agent = crud.agent.remove(db, id=agent_id)
    return agent

@router.post("/{agent_id}/execute", response_model=schemas.AgentExecution)
def execute_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    input_parameters: dict,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Execute an agent with the given input parameters.
    """
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if the current user is the owner of the agent
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Create a new execution record
    execution_data = {
        "status": "pending",
        "input_parameters": input_parameters,
    }
    
    # In a real implementation, you would queue the execution
    # For now, we'll just create the execution record
    execution = crud.agent.log_execution(
        db, agent_id=agent_id, execution_data=execution_data
    )
    
    # TODO: Queue the execution in a background task
    
    return execution

@router.get("/{agent_id}/executions", response_model=List[schemas.AgentExecution])
def get_agent_executions(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get execution history for an agent.
    """
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if the current user is the owner of the agent
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # In a real implementation, you would fetch executions from the database
    # For now, we'll return an empty list
    return []
