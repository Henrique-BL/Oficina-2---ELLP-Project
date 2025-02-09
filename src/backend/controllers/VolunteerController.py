from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from models.Volunteer import Volunteer
from schemas.VolunteerSchema import VolunteerIn, VolunteerOut
from configs.dependencies import DataBaseDependency
from pydantic import ValidationError
from datetime import datetime


router = APIRouter()

@router.post("/", response_model=VolunteerOut, status_code=status.HTTP_201_CREATED)
async def create_volunteer(db_session: DataBaseDependency, volunteer_in: VolunteerIn = Body(...)) -> VolunteerOut:
    volunteer = (await db_session.execute(select(Volunteer).filter_by(student_code=volunteer_in.student_code))).scalar_one_or_none()
    if volunteer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The volunteer with student code {volunteer_in.student_code} already exists",
        )
    try:    
        volunteer_out = VolunteerOut(id=uuid4(), created_at=datetime.utcnow(), **volunteer_in.model_dump())
        volunteer_model = Volunteer(**volunteer_out.model_dump())
        db_session.add(volunteer_model)
        await db_session.commit()
        return volunteer_out
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        await db_session.close()

@router.post("/workshops/{workshop_id}", response_model=list[VolunteerOut], status_code=status.HTTP_201_CREATED)
async def add_volunteers_to_workshop(
    workshop_id: str,
    db_session: DataBaseDependency,
    volunteers: list[str] = Body(..., embed=True)
) -> list[VolunteerOut]:
    volunteers_out = []
    for volunteer_id in volunteers:
        volunteer = (await db_session.execute(
            select(Volunteer).filter_by(id=volunteer_id)
        )).scalar_one_or_none()
        
        if not volunteer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The volunteer with id {volunteer_id} does not exist",
            )
            
        volunteer.workshop_id = workshop_id
        volunteers_out.append(VolunteerOut.model_validate(volunteer))
    
    await db_session.commit()
    return volunteers_out

@router.get("/", response_model=list[VolunteerOut], status_code=status.HTTP_200_OK)
async def query(db_session: DataBaseDependency) -> list[VolunteerOut]:
    volunteers: list[VolunteerOut] = (await db_session.execute(select(Volunteer))).scalars().all()
    return [VolunteerOut.model_validate(volunteer) for volunteer in volunteers]


@router.get("/{id}", response_model=VolunteerOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> VolunteerOut:
    volunteer: VolunteerOut = (await db_session.execute(select(Volunteer).filter_by(id=id))).scalar_one_or_none()
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The volunteer with id {id} was not found",
        )
    return volunteer

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DataBaseDependency):
    volunteer: VolunteerOut = (await db_session.execute(select(Volunteer).filter_by(id=id))).scalar_one_or_none()
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The volunteer with id {id} was not found",
        )
    await db_session.delete(volunteer)
    await db_session.commit()


