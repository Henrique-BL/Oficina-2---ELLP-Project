from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from models.Workshop import Workshop
from schemas.Workshop import WorkshopIn, WorkshopOut
from configs.dependencies import DataBaseDependency
from pydantic import ValidationError
from datetime import datetime



router = APIRouter()

@router.post("/", response_model=WorkshopOut, status_code=status.HTTP_201_CREATED)
async def create_workshop(db_session: DataBaseDependency, workshop_in: WorkshopIn = Body(...)) -> WorkshopOut:
    print("workshop_in",workshop_in)
    workshop = (await db_session.execute(select(Workshop).filter_by(name=workshop_in.name))).scalar_one_or_none()
    if workshop:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The workshop with name {workshop_in.name} already exists",
        )
    try:    

        workshop_out = WorkshopOut(id=uuid4(), created_at=datetime.utcnow(), **workshop_in.model_dump())
        workshop_model = Workshop(**workshop_out.model_dump())
        db_session.add(workshop_model)
        await db_session.commit()
        return workshop_out

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        await db_session.close()

@router.get("/", response_model=list[WorkshopOut], status_code=status.HTTP_200_OK)
async def query(db_session: DataBaseDependency) -> list[WorkshopOut]:

    workshops: list[WorkshopOut] = (await db_session.execute(select(Workshop))).scalars().all()
    return [WorkshopOut.model_validate(workshop) for workshop in workshops]



@router.get("/{id}", response_model=WorkshopOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> WorkshopOut:
    workshop: WorkshopOut = (await db_session.execute(select(Workshop).filter_by(id=id))).scalar_one_or_none()

    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The workshop with id {id} was not found",
        )

    return workshop

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DataBaseDependency):

    workshop: WorkshopOut = (await db_session.execute(select(Workshop).filter_by(id=id))).scalar_one_or_none()
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The workshop with id {id} was not found",
        )

    await db_session.delete(workshop)
    await db_session.commit()


