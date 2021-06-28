from __future__ import annotations
from flask import redirect, url_for, flash
from flask_login import current_user
from werkzeug.exceptions import abort
from app.models import User

def has_permissions(perms: str | list[str]) -> bool:
    if isinstance(perms, str):
        perms = [perms]
    def has_access():
        if not current_user.has_permissions(perms):
            abort(404)
    return has_access