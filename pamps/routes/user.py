from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from pamps.db import ActiveSession
from pamps.models.user import User, UserRequest, UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def list_users(*, session = ActiveSession):
    """List All users"""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_name(*, session: Session=ActiveSession, username: str):
    """Get user from name"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Create new user"""
    db_user = User.from_orm(user) # Transform userrequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user