"""Local manager PIN hashing and verification; no plaintext PIN is persisted."""
import base64
import hashlib
import hmac
import os
from sqlalchemy.orm import Session
from .models import SecuritySettings

_ITERATIONS = 310_000


def hash_pin(pin: str) -> str:
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac('sha256', pin.encode(), salt, _ITERATIONS)
    return f'{_ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(derived).decode()}'


def verify_pin(pin: str, encoded: str) -> bool:
    iterations, salt, expected = encoded.split('$')
    candidate = hashlib.pbkdf2_hmac('sha256', pin.encode(), base64.b64decode(salt), int(iterations))
    return hmac.compare_digest(candidate, base64.b64decode(expected))


def security_settings(db: Session) -> SecuritySettings | None:
    return db.get(SecuritySettings, 1)
