# System Architecture

```
[React SPA] --HTTPS--> [FastAPI Gateway] --SQL--> [SQLite DB]
                               |
                               +--> [PQ Crypto Module (Kyber/Dilithium/AES)]
                               |
                               +--> [Argon2 Password Service]
```

## Components
- **Web Client (`client/`)**  
  Vite + React SPA that handles registration/login, message composition, inbox view, and calls FastAPI APIs.

- **API Layer (`server/app`)**  
  FastAPI app exposing auth, user, and messaging routes. Performs PQ operations via `pqcrypto`. Persists metadata using SQLModel + SQLite.

- **Crypto Utilities (`server/app/crypto.py`)**  
  - Kyber512 for key encapsulation.  
  - Dilithium2 for message signing.  
  - AES-256-GCM for payload encryption + key wrapping.  
  - Base64 helpers and deterministic envelope serialization.

- **Persistence (`sqlite:///./pqchat.db`)**  
  Stores user metadata, encrypted private keys, and encrypted message envelopes. For production, swap with Postgres + KMS-managed master key.

- **CLI Demo (`server/scripts/demo_flow.py`)**  
  Automates registration, login, message send, and inbox decryption for reproducible grading/demo.

## Data Flows
1. **Registration**  
   User submits username/password → server Argon2-hashes password, generates PQ key pairs, wraps private keys with master key, stores public material, returns one-time private key bundle to client.

2. **Authentication**  
   Client posts credentials → JWT access token minted via HS256, used for all subsequent API calls.

3. **Message Dispatch**  
   Authenticated user posts plaintext → server encapsulates shared secret with recipient Kyber public key → encrypts payload with AES-GCM → signs envelope with sender Dilithium private key → stores record.

4. **Inbox Retrieval & Decryption**  
   Recipient lists envelopes → upon decrypt request server verifies Dilithium signature, decapsulates shared secret using wrapped Kyber private key, returns plaintext. (Future work: move step to client-side WASM.)

## Security Guarantees
- **Confidentiality**: AES-GCM payloads + server-side key wrapping; TLS recommended in deployment.
- **Integrity & Authentication**: Dilithium signatures validated before decrypting.
- **Non-repudiation**: Signed envelopes + database audit fields provide tamper-evident trail.
- **Key Management**: Master key derived from env secret; documented rotation procedure in `docs/TECH_REPORT_OUTLINE.md`.

