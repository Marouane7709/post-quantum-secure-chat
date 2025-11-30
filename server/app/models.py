from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    kem_public_key: str
    kem_private_key_encrypted: str
    kem_private_key_nonce: str
    sign_public_key: str
    sign_private_key_encrypted: str
    sign_private_key_nonce: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.id")
    recipient_id: int = Field(foreign_key="user.id")
    kem_ciphertext: str
    ciphertext: str
    nonce: str
    signature: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None

