from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth_router,
    users_router,
    agents_router,
    social_router,
    vector_store_router,
)

# Create the main API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(agents_router, prefix="/agents", tags=["Agents"])
api_router.include_router(social_router, prefix="/social", tags=["Social Media"])
api_router.include_router(vector_store_router, prefix="/vector-store", tags=["Vector Store"])
