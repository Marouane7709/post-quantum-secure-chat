import base64
import secrets
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pqcrypto.kem.ml_kem_512 import decrypt as kem_decrypt
from pqcrypto.kem.ml_kem_512 import encrypt as kem_encrypt
from pqcrypto.kem.ml_kem_512 import generate_keypair as kem_generate_keypair
from pqcrypto.sign.ml_dsa_44 import generate_keypair as dsa_generate_keypair
from pqcrypto.sign.ml_dsa_44 import sign as dsa_sign
from pqcrypto.sign.ml_dsa_44 import verify as dsa_verify


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def generate_kem_keypair() -> Tuple[str, str]:
    public_key, secret_key = kem_generate_keypair()
    return b64encode(public_key), b64encode(secret_key)


def generate_signature_keypair() -> Tuple[str, str]:
    public_key, secret_key = dsa_generate_keypair()
    return b64encode(public_key), b64encode(secret_key)


def encrypt_private_key(master_key: bytes, private_key_b64: str) -> Tuple[str, str]:
    nonce = secrets.token_bytes(12)
    aes = AESGCM(master_key)
    ciphertext = aes.encrypt(nonce, b64decode(private_key_b64), None)
    return b64encode(ciphertext), b64encode(nonce)


def decrypt_private_key(master_key: bytes, encrypted_b64: str, nonce_b64: str) -> str:
    aes = AESGCM(master_key)
    plaintext = aes.decrypt(b64decode(nonce_b64), b64decode(encrypted_b64), None)
    return b64encode(plaintext)


def encapsulate(public_key_b64: str) -> Tuple[str, bytes]:
    ciphertext, shared_secret = kem_encrypt(b64decode(public_key_b64))
    return b64encode(ciphertext), shared_secret


def decapsulate(private_key_b64: str, ciphertext_b64: str) -> bytes:
    return kem_decrypt(b64decode(private_key_b64), b64decode(ciphertext_b64))


def encrypt_payload(shared_secret: bytes, plaintext: str) -> Tuple[str, str]:
    aes = AESGCM(shared_secret)
    nonce = secrets.token_bytes(12)
    ciphertext = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    return b64encode(ciphertext), b64encode(nonce)


def decrypt_payload(shared_secret: bytes, ciphertext_b64: str, nonce_b64: str) -> str:
    aes = AESGCM(shared_secret)
    plaintext = aes.decrypt(b64decode(nonce_b64), b64decode(ciphertext_b64), None)
    return plaintext.decode("utf-8")


def sign_message(private_key_b64: str, data: bytes) -> str:
    signature = dsa_sign(b64decode(private_key_b64), data)
    return b64encode(signature)


def verify_signature(public_key_b64: str, data: bytes, signature_b64: str) -> bool:
    try:
        dsa_verify(b64decode(public_key_b64), data, b64decode(signature_b64))
        return True
    except ValueError:
        return False


