from typing import Annotated, Literal

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel

from app.core.config import Settings, get_settings


class UserContext(BaseModel):
    user_id: str
    role: Literal["viewer", "editor", "admin"]

def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    gateway_key: Annotated[str | None, Header(alias="X-Gateway-Key")] = None,
    role: Annotated[str, Header(alias="X-User-Role")] = "viewer",
) -> UserContext:
    expected_key = settings.gateway_secret_key.get_secret_value()
    if gateway_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid gateway key",
        )
    if role not in ["viewer", "editor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The supplied user role is not allowed.",
        )
    return UserContext(user_id="local-user", role=role)


def require_editor(
    user: Annotated[UserContext, Depends(get_current_user)],
) -> UserContext:
    if user.role not in {"editor", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires editor or admin access.",
        )
    return user

