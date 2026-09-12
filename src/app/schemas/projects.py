from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectStatus(StrEnum):
    active = "active"
    archived = "archived"


class ProjectCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra="forbid")
    name: str = Field(min_length=3, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    status: ProjectStatus = ProjectStatus.active



class ProjectUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra="forbid")
    name: str | None = Field(default=None, min_length=3, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    status: ProjectStatus | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra="forbid")
    id: UUID
    name: str
    description: str | None
    status: ProjectStatus
    create_at: datetime


class ProjectListResponse(BaseModel):
    items: list[ProjectRead]
    count: int





