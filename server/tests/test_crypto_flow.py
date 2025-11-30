import os

from app import crypto


def test_private_key_roundtrip():
    master_key = os.urandom(32)
    kem_public, kem_private = crypto.generate_kem_keypair()
    encrypted, nonce = crypto.encrypt_private_key(master_key, kem_private)
    recovered = crypto.decrypt_private_key(master_key, encrypted, nonce)
    assert recovered == kem_private


def test_message_encryption_cycle():
    kem_public, kem_private = crypto.generate_kem_keypair()
    kem_ciphertext, shared_secret = crypto.encapsulate(kem_public)
    ciphertext, nonce = crypto.encrypt_payload(shared_secret, "test-message")
    recovered_secret = crypto.decapsulate(kem_private, kem_ciphertext)
    plaintext = crypto.decrypt_payload(recovered_secret, ciphertext, nonce)
    assert plaintext == "test-message"

