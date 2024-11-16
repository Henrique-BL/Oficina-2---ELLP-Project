from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from models.Sector import Sector
from schemas.SectorSchema import SectorIn, SectorOut
from configs.dependencies import DataBaseDependency
from datetime import datetime
from pydantic import ValidationError

router = APIRouter()    
@router.post("/", response_model=SectorOut, status_code=status.HTTP_201_CREATED)
async def post(db_session: DataBaseDependency, sector_in: SectorIn = Body(...)) -> SectorOut:
    
    sector = (await db_session.execute(select(Sector).filter_by(name=sector_in.name))).scalar_one_or_none()
    if sector:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The sector {sector_in.name} already exists")
    try:
        sector_out = SectorOut(id=uuid4(), created_at=datetime.utcnow(), **sector_in.model_dump())
        sector_model = Sector(**sector_out.model_dump())
        db_session.add(sector_model)
        await db_session.commit()
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return sector_out

@router.get("/sectors", response_model=list[SectorOut])
async def query(db_session: DataBaseDependency) -> list[SectorOut]:
    sectors: list[SectorOut] = (await db_session.execute(select(Sector))).scalars().all()
    print('Sectors', sectors)
    return [SectorOut.model_validate(sector) for sector in sectors]

@router.get("/sectors/{sector_id}", response_model=SectorOut)
async def get(db_session: DataBaseDependency, sector_id: UUID4) -> SectorOut:

    sector: SectorOut = (await db_session.execute(select(Sector).filter_by(id=sector_id))).scalar_one_or_none()
    
    if not sector:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The sector {sector_id} was not found")
    
    return sector


@router.delete("/sectors/{sector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db_session: DataBaseDependency, sector_id: UUID4) -> None:
    sector: SectorOut = (await db_session.execute(select(Sector).filter_by(id=sector_id))).scalar_one_or_none()
    
    if not sector:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The sector {sector_id} was not found")
    
    await db_session.delete(sector)
    await db_session.commit()
