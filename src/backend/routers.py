from fastapi import APIRouter

from controllers.VolunteerController import router as volunteer
api_router = APIRouter()
api_router.include_router(volunteer, prefix="/volunteers", tags=['volunteers'])
