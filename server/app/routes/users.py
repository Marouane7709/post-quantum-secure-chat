from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..schemas import UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserPublic])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return [
        UserPublic(
            id=user.id,
            username=user.username,
            kem_public_key=user.kem_public_key,
            sign_public_key=user.sign_public_key,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.get("/{username}", response_model=UserPublic)
def get_user(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserPublic(
        id=user.id,
        username=user.username,
        kem_public_key=user.kem_public_key,
        sign_public_key=user.sign_public_key,
        created_at=user.created_at,
    )


