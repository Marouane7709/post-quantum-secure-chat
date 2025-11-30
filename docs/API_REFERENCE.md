# API Reference

## Auth

### `POST /auth/register`
- **Body**: `{ "username": "alice", "password": "Secret#1" }`
- **Response**: `UserWithKeys` including one-time private key bundle.

### `POST /auth/login`
- **Body**: `{ "username": "alice", "password": "Secret#1" }`
- **Response**: `{ "access_token": "...", "token_type": "bearer" }`

### `GET /auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: user public metadata.

## Users

### `GET /users`
- List all user public keys.

### `GET /users/{username}`
- Retrieve public keys for a specific identity.

## Messages

### `POST /messages`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "recipient_username": "bob", "plaintext": "hi" }`
- **Flow**: server encapsulates w/ Kyber, encrypts w/ AES-GCM, signs via Dilithium.
- **Response**: persisted message record.

### `GET /messages/inbox`
- Returns encrypted envelopes for the authenticated user.

### `GET /messages/sent`
- Returns envelopes sent by the authenticated user.

### `POST /messages/{id}/decrypt`
- **Headers**: bearer token of recipient.
- **Response**: `{ "message_id": 1, "plaintext": "hi", "created_at": "..." }`
- **Validation**: rejects if Dilithium signature fails.

## Health

### `GET /health`
- Returns `{ "status": "ok" }` for monitoring.

