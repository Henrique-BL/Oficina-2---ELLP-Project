from fastapi import APIRouter

from controllers.VolunteerController import router as volunteer
from controllers.WorkshopController import router as workshop
from controllers.AdminController import router as admin


api_router = APIRouter()
api_router.include_router(volunteer, prefix="/volunteers", tags=['volunteers'])
api_router.include_router(admin, prefix="/admins", tags=['admins'])
api_router.include_router(workshop, prefix="/workshops", tags=['workshops'])