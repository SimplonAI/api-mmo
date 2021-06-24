from __future__ import annotations
from flask_login import current_user
from app.models import User

def has_permissions(perms: str | list[str]) -> bool:
    if isinstance(perms, str):
        perms = [perms]
    if current_user.is_authenticated:
        return all([perm in current_user.role.permissions for perm in perms])
    return False