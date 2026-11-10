import ast
from pathlib import Path
import re

import pytest
from werkzeug.security import check_password_hash

from app.utils.seed_credentials import seed_password_hash


def test_seed_accounts_require_explicit_passwords(monkeypatch):
    monkeypatch.delenv("SEED_PASSWORD_123", raising=False)
    with pytest.raises(RuntimeError):
        seed_password_hash(123)
    monkeypatch.setenv("SEED_PASSWORD_123", "example-only-password-123")
    assert check_password_hash(seed_password_hash(123), "example-only-password-123")


def test_python_sources_have_no_embedded_database_passwords_or_hashes():
    root = Path(__file__).resolve().parents[1]
    paths = list(root.glob("*.py")) + list((root / "app").rglob("*.py")) + list((root / "tests").glob("*.py"))
    db_uri = re.compile(r"postgres(?:ql)?(?:\+[a-z0-9_]+)?://[^/\s:@]+:[^/\s@]+@", re.I)
    password_hash = re.compile(r"^(?:scrypt|pbkdf2):[^\s]+\$[^\s]+\$", re.I)
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert not db_uri.search(node.value), f"Embedded database password: {path.relative_to(root)}"
                assert not password_hash.search(node.value), f"Embedded password hash: {path.relative_to(root)}"
