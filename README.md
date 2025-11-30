# PQ Secure Messenger

Web-based messaging prototype demonstrating post-quantum cryptography with Kyber512 key encapsulation and Dilithium2 signatures. Built for the cryptography class project (due Nov 26, 2025).

## Features
- FastAPI backend with SQLModel + SQLite persistence.
- PQ key lifecycle (Kyber + Dilithium) with AES-GCM key wrapping.
- React + Vite SPA for registration, login, message composition, and inbox decryption.
- CLI demo script for automated end-to-end run.
- Documentation bundles for report + presentation.

## Tech Stack
- **Backend**: Python 3.11, FastAPI, SQLModel, pqcrypto, cryptography, Argon2.
- **Frontend**: React 18, Vite, Axios.
- **Security**: Kyber512, Dilithium2, AES-256-GCM, Argon2id, JWT (HS256).

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend
```powershell
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment overrides (optional) via `.env`:
```
DATABASE_URL=sqlite:///./pqchat.db
SECRET_KEY=...
CRYPTO_MASTER_KEY=...
```

### Frontend
```powershell
cd client
npm install
npm run dev
```
Set `VITE_API_URL` to backend origin if not using the local proxy.

### Demo Script
Run after backend is up:
```powershell
cd server
.venv\Scripts\activate
python scripts/demo_flow.py
```

## Testing
```powershell
cd server
.venv\Scripts\activate
pytest
```

## Documentation
- Architecture: `docs/ARCHITECTURE.md`
- API reference: `docs/API_REFERENCE.md`

## Roadmap
- Client-side WASM crypto (avoid decrypting on server).
- Key transparency service + audit logs.
- WebSocket push notifications for real-time chat.

