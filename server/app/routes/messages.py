from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .. import crypto, schemas
from ..database import get_session
from ..dependencies import get_current_user, get_master_key
from ..models import Message, User

router = APIRouter(prefix="/messages", tags=["messages"])


def _serialize_envelope(kem_ciphertext: str, nonce: str, ciphertext: str) -> bytes:
    return "|".join([kem_ciphertext, nonce, ciphertext]).encode("utf-8")


@router.post("", response_model=schemas.MessageRecord, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: schemas.MessageCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    recipient = session.exec(select(User).where(User.username == payload.recipient_username)).first()
    if not recipient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")

    kem_ciphertext, shared_secret = crypto.encapsulate(recipient.kem_public_key)
    ciphertext, nonce = crypto.encrypt_payload(shared_secret, payload.plaintext)

    master_key = get_master_key()
    sender_private_sign_b64 = crypto.decrypt_private_key(
        master_key, current_user.sign_private_key_encrypted, current_user.sign_private_key_nonce
    )
    envelope = _serialize_envelope(kem_ciphertext, nonce, ciphertext)
    signature = crypto.sign_message(sender_private_sign_b64, envelope)

    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient.id,
        kem_ciphertext=kem_ciphertext,
        ciphertext=ciphertext,
        nonce=nonce,
        signature=signature,
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return schemas.MessageRecord(**message.dict())


@router.get("/inbox", response_model=List[schemas.MessageRecord])
def inbox(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.recipient_id == current_user.id).order_by(Message.created_at.desc()))
    return [schemas.MessageRecord(**msg.dict()) for msg in messages]


@router.get("/sent", response_model=List[schemas.MessageRecord])
def sent(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.sender_id == current_user.id).order_by(Message.created_at.desc()))
    return [schemas.MessageRecord(**msg.dict()) for msg in messages]


@router.post("/{message_id}/decrypt", response_model=schemas.MessageDecryptResponse)
def decrypt_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    message = session.get(Message, message_id)
    if not message or message.recipient_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    sender = session.get(User, message.sender_id)
    if not sender:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender missing")

    envelope = _serialize_envelope(message.kem_ciphertext, message.nonce, message.ciphertext)
    if not crypto.verify_signature(sender.sign_public_key, envelope, message.signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature verification failed")

    master_key = get_master_key()
    recipient_kem_private_b64 = crypto.decrypt_private_key(
        master_key, current_user.kem_private_key_encrypted, current_user.kem_private_key_nonce
    )
    shared_secret = crypto.decapsulate(recipient_kem_private_b64, message.kem_ciphertext)
    plaintext = crypto.decrypt_payload(shared_secret, message.ciphertext, message.nonce)

    return schemas.MessageDecryptResponse(message_id=message.id, plaintext=plaintext, created_at=message.created_at)


