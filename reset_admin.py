"""Admin password reset (manual, controlled operation).

Requires DATABASE_URL, ADMIN_EMAIL and ADMIN_NEW_PASSWORD environment variables.
Never commit credentials or print their values.
Historical Git credentials must be rotated at the provider separately.
"""
import os
import psycopg2
from werkzeug.security import generate_password_hash


def reset():
    database_url = os.environ["DATABASE_URL"]
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_NEW_PASSWORD"]
    if len(password) < 12:
        raise ValueError("ADMIN_NEW_PASSWORD must contain at least 12 characters")
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET password_hash = %s WHERE email = %s AND nivel = 3",
                (generate_password_hash(password), email),
            )
            if cur.rowcount != 1:
                raise ValueError("Exactly one administrator account must match")
    print("Administrator password updated.")


if __name__ == "__main__":
    reset()
