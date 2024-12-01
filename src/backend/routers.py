from fastapi import APIRouter

from controllers.VolunteerController import router as volunteer
from controllers.SectorController import router as sector
from controllers.AdminController import router as admin
api_router = APIRouter()

api_router.include_router(volunteer, prefix="/volunteers", tags=['volunteers'])
api_router.include_router(sector, prefix="/sectors", tags=['sectors'])
api_router.include_router(admin, prefix="/admins", tags=['admins'])
