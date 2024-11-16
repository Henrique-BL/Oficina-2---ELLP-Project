from fastapi import APIRouter

from controllers.VolunteerController import router as atleta
from controllers.SectorController import router as sector
api_router = APIRouter()

api_router.include_router(atleta, prefix="/atletas", tags=['atletas'])
api_router.include_router(sector, prefix="/sectors", tags=['sectors'])
