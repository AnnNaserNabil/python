"""API v1 router configuration."""
from fastapi import APIRouter

from src.api.v1.endpoints import auth, campaigns, ads, reporting

api_router = APIRouter()

# Include API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])
api_router.include_router(ads.router, prefix="/ads", tags=["Ads"])
api_router.include_router(reporting.router, prefix="/reporting", tags=["Reporting"])
