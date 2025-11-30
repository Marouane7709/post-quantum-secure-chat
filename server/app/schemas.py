from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    kem_public_key: str
    sign_public_key: str
    created_at: datetime


class UserWithKeys(UserPublic):
    kem_private_key: str
    sign_private_key: str


class MessageCreate(BaseModel):
    recipient_username: str
    plaintext: str


class MessageRecord(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    kem_ciphertext: str
    ciphertext: str
    nonce: str
    signature: str
    created_at: datetime
    delivered_at: Optional[datetime] = None


class MessageDecryptResponse(BaseModel):
    message_id: int
    plaintext: str
    created_at: datetime


