from fastapi import APIRouter

from controllers.VolunteerController import router as volunteer
from controllers.AdminController import router as admin

api_router = APIRouter()
api_router.include_router(volunteer, prefix="/volunteers", tags=['volunteers'])
api_router.include_router(admin, prefix="/admin", tags=['admin'])