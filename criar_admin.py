"""Create a first administrator explicitly, using environment-provided credentials."""
import os
from app import create_app
from app.db import db
from app.models.user import User


def main():
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_NEW_PASSWORD"]
    nome = os.environ.get("ADMIN_NAME", "Admin")
    if len(password) < 12:
        raise ValueError("ADMIN_NEW_PASSWORD must contain at least 12 characters")
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email=email).first():
            raise ValueError("Administrator email already exists")
        admin = User(nome=nome, email=email, nivel=3)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
    print("Administrator created.")


if __name__ == "__main__":
    main()
