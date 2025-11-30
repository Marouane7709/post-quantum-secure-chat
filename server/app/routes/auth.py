from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .. import crypto, schemas
from ..dependencies import get_current_user, get_master_key
from ..models import User
from ..database import get_session
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserWithKeys, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    password_hash = hash_password(payload.password)
    kem_public, kem_private = crypto.generate_kem_keypair()
    sign_public, sign_private = crypto.generate_signature_keypair()
    master_key = get_master_key()

    kem_private_enc, kem_nonce = crypto.encrypt_private_key(master_key, kem_private)
    sign_private_enc, sign_nonce = crypto.encrypt_private_key(master_key, sign_private)

    user = User(
        username=payload.username,
        password_hash=password_hash,
        kem_public_key=kem_public,
        kem_private_key_encrypted=kem_private_enc,
        kem_private_key_nonce=kem_nonce,
        sign_public_key=sign_public,
        sign_private_key_encrypted=sign_private_enc,
        sign_private_key_nonce=sign_nonce,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return schemas.UserWithKeys(
        id=user.id,
        username=user.username,
        kem_public_key=user.kem_public_key,
        kem_private_key=kem_private,
        sign_public_key=user.sign_public_key,
        sign_private_key=sign_private,
        created_at=user.created_at,
    )


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return schemas.Token(access_token=token)


@router.get("/me", response_model=schemas.UserPublic)
def read_me(current_user: User = Depends(get_current_user)):
    return schemas.UserPublic(
        id=current_user.id,
        username=current_user.username,
        kem_public_key=current_user.kem_public_key,
        sign_public_key=current_user.sign_public_key,
        created_at=current_user.created_at,
    )


