from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies import UserContext, get_current_user, require_editor
from app.schemas.projects import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectStatus,
    ProjectUpdate,
)
from app.services.projects import ProjectService, get_project_service

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _user: Annotated[UserContext, Depends(get_current_user)],
    status: ProjectStatus | None = None,
    ) -> ProjectListResponse:
    return service.list_projects(status)


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    user: Annotated[UserContext, Depends(require_editor)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectRead:
    return service.create_project(payload=payload, created_by=user.user_id)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)],
    _user: Annotated[UserContext, Depends(get_current_user)],
) -> ProjectRead:
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    user: Annotated[UserContext, Depends(require_editor)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectRead:
    return service.update_project(project_id=project_id, payload=payload)


