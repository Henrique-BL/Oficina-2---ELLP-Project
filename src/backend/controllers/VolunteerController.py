from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from models.Volunteer import Volunteer
from schemas.VolunteerSchema import VolunteerIn, VolunteerOut
from models.Sector import Sector
from configs.dependencies import DataBaseDependency

router = APIRouter()

@router.post("/volunteers", response_model=VolunteerOut)
async def create_volunteer(db_session: DataBaseDependency, volunteer_in: VolunteerIn = Body(...)) -> VolunteerOut:
    sector = (
        (
            await db_session.execute(
                select(Sector).filter_by(name=volunteer_in.sector_name)
            )
        )
        .scalars()
        .first()
    )

    if not sector:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The sector {volunteer_in.sector_name} was not found",
        )
    
    return await Volunteer.create(db_session, volunteer_in)

@router.get("/volunteers", response_model=list[VolunteerOut])
async def query(db_session: DataBaseDependency) -> list[VolunteerOut]:
    volunteers: list[VolunteerOut] = await db_session.execute(select(Volunteer)).scalars().all()
    return [VolunteerOut.model_validate(volunteer) for volunteer in volunteers]

@router.get("/volunteers/{id}", response_model=VolunteerOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> VolunteerOut:
    volunteer: VolunteerOut = await db_session.execute(select(Volunteer).filter_by(id=id)).scalar_one_or_none()
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The volunteer with id {id} was not found",
        )
    return volunteer

@router.delete("/volunteers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DataBaseDependency):
    volunteer: VolunteerOut = await db_session.execute(select(Volunteer).filter_by(id=id)).scalar_one_or_none()
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The volunteer with id {id} was not found",
        )
    await db_session.delete(volunteer)
    await db_session.commit()


