from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from models.Admin import Admin
from schemas.AdminSchema import AdminInRegister, AdminInLogin, AdminOut, AdminOutRegister
from configs.dependencies import DataBaseDependency
from pydantic import ValidationError
from datetime import datetime
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
async def register_admin(db_session: DataBaseDependency, admin_in: AdminInRegister = Body(...)) -> AdminOut:
    # Check if admin with email already exists
    admin = (await db_session.execute(select(Admin).filter_by(email=admin_in.email))).scalar_one_or_none()
    print(f"admin: {admin}")
    if admin:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An admin with email {admin_in.email} already exists",
        )
    
    try:    
        # Hash the password before storing
        hashed_password = pwd_context.hash(admin_in.password)
        
        # Create admin with hashed password
        admin_data = admin_in.model_dump()
        admin_data["password"] = hashed_password
        
        admin_register = AdminOutRegister(
            id=uuid4(), 
            created_at=datetime.utcnow(), 
            **admin_data
        )
        admin_model = Admin(**admin_register.model_dump())
        db_session.add(admin_model)
        await db_session.commit()
        admin_out = AdminOut(**admin_register.model_dump(exclude={"password"}))
        return admin_out
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        await db_session.close()

@router.post("/login", response_model=AdminOut, status_code=status.HTTP_200_OK)
async def login_admin(db_session: DataBaseDependency, admin_in: AdminInLogin = Body(...)) -> AdminOut:
    admin = (await db_session.execute(select(Admin).filter_by(email=admin_in.email))).scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")    
    try:
        if not pwd_context.verify(admin_in.password, admin.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        return admin
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[AdminOut], status_code=status.HTTP_200_OK)
async def query(db_session: DataBaseDependency) -> list[AdminOut]:
    admins: list[AdminOutRegister] = (await db_session.execute(select(Admin))).scalars().all()
    return [AdminOut.model_validate(admin) for admin in admins]

@router.get("/{id}", response_model=AdminOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> AdminOut:
    admin: AdminOut = (await db_session.execute(select(Admin).filter_by(id=id))).scalar_one_or_none()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The admin with id {id} was not found",
        )
    print(f"admin: {admin}")
    return admin

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DataBaseDependency):
    admin: AdminOut = (await db_session.execute(select(Admin).filter_by(id=id))).scalar_one_or_none()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The admin with id {id} was not found",
        )
    await db_session.delete(admin)
    await db_session.commit()
