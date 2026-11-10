"""Generate password hashes for explicitly configured demo accounts."""
import os

from werkzeug.security import generate_password_hash


def seed_password_hash(user_id):
    key = f"SEED_PASSWORD_{user_id}"
    password = os.environ.get(key)
    if not password or len(password) < 12:
        raise RuntimeError(f"Set {key} to a unique password of at least 12 characters")
    return generate_password_hash(password)
