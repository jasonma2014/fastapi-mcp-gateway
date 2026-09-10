from importlib.metadata import PackageNotFoundError, version
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter()

def package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "not-installed"


@router.get("/health/live")
async def live_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "fastapi-mcp-gateway",
    }

@router.get("/health/ready")
async def readiness_check(settings: Annotated[Settings, Depends(get_settings)], ) -> dict[str, object]:
    return {
        "status": "ready",
        "app_name": settings.app_name,
        "environment": settings.environment,
        "mcp": {
            "endpoing_path": settings.mcp_endpoint_path,
            "sdk_version": package_version("mcp")
        },
        "runtime": {
            "fastapi_version": package_version("fastapi"),
        },
    }
