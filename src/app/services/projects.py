from datetime import UTC, datetime
from functools import cache, lru_cache
from msilib import UuidCreate
from uuid import UUID, uuid4

from app.schemas.projects import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
    ProjectStatus,
)

class ProjectNotFoundError(Exception):
    def __init__(self, project_id: UUID) -> None:
        super().__init__(f"Project {project_id} was not found.")
        self.project_id = project_id



class ProjectService:
    def __init__(self) -> None:
        self._projects: dict[UUID, ProjectRead] = {}
        self._owners: dict[UUID, str] = {}


    def create_project(
        self,
        payload: ProjectCreate,
        created_by: str,
    ) -> ProjectRead:
        project_id = uuid4()
        project = ProjectRead(
            id=project_id,
            name=payload.name,
            description=payload.description,
            status=payload.status,
            created_at=datetime.now(UTC),
        )
        self._projects[project_id] = project
        self._owners[project_id] = created_by
        return project
    

    def list_projects(
        self,
        status: ProjectStatus | None = None,
    ) -> ProjectListResponse:
        items = list(self._projects.values())
        if status is not None:
            items = [project for project in items if project.status == status]
        return ProjectListResponse(items=items, count=len(items))


    def get_project(self, project_id: UUID) -> ProjectRead:
        project = self._projects.get(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        return project
        

    def update_project(
        self,
        project_id: UUID,
        payload: ProjectUpdate,
    ) -> ProjectRead:
        current_project = self.get_project(project_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated_project = current_project.model_copy(update=update_data)
        self._projects[project_id] = updated_project
        return updated_project
    

@lru_cache
def get_project_service() -> ProjectService:
    return ProjectService()
