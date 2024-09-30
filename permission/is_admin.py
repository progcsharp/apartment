from typing import Callable

from fastapi import Depends, HTTPException

from db.engine import get_db
from db.handler.get import get_user
from service.security import manager


async def check_admin(user):
    if user.is_admin:
        return True
    return False
