import json
import os
from dataclasses import dataclass

import httpx

API_URL = os.getenv("PQCHAT_API_URL", "http://127.0.0.1:8000")


@dataclass
class UserCredentials:
    username: str
    password: str
    token: str


def register(username: str, password: str, client: httpx.Client) -> dict:
    response = client.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
    response.raise_for_status()
    bundle = response.json()
    print(f"Registered {username}")
    return bundle


def login(username: str, password: str, client: httpx.Client) -> UserCredentials:
    response = client.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
    response.raise_for_status()
    token = response.json()["access_token"]
    print(f"Logged in {username}")
    return UserCredentials(username=username, password=password, token=token)


def send_message(token: str, recipient: str, plaintext: str, client: httpx.Client) -> dict:
    response = client.post(
        f"{API_URL}/messages",
        headers={"Authorization": f"Bearer {token}"},
        json={"recipient_username": recipient, "plaintext": plaintext},
    )
    response.raise_for_status()
    message = response.json()
    print(f"Message {message['id']} queued for {recipient}")
    return message


def decrypt_inbox(token: str, client: httpx.Client):
    inbox = client.get(f"{API_URL}/messages/inbox", headers={"Authorization": f"Bearer {token}"})
    inbox.raise_for_status()
    messages = inbox.json()
    for message in messages:
        decrypted = client.post(
            f"{API_URL}/messages/{message['id']}/decrypt",
            headers={"Authorization": f"Bearer {token}"},
        )
        decrypted.raise_for_status()
        payload = decrypted.json()
        print(f"[{payload['created_at']}] Message {payload['message_id']} -> {payload['plaintext']}")


def main():
    alice_pw = "Wonderland#42"
    bob_pw = "Builder#42"
    with httpx.Client(timeout=30) as client:
        try:
            register("alice", alice_pw, client)
            register("bob", bob_pw, client)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code != 400:
                raise
            print("Users already existed, continuing.")

        alice = login("alice", alice_pw, client)
        bob = login("bob", bob_pw, client)
        send_message(alice.token, "bob", "Hello from the post-quantum side!", client)
        decrypt_inbox(bob.token, client)


if __name__ == "__main__":
    main()

