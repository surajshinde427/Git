
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

# ----- API Request DTO -----
class ResourceMetadataData(BaseModel):
    # project-level
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    updated_by: str
    created_by: str
    # user-state (inline)
    viewer_settings: Optional[dict[str, Any]] = None  # JSONB
    last_tick: Optional[int] = None
    agent_id: Optional[str] = None

class GenerateResourceMetadataRequest(BaseModel):
    data: ResourceMetadataData

class GenerateResourceMetadataResponse(BaseModel):
    message: str = "ok"

# ----- DB Row DTOs (service builds these, repo inserts them) -----
class ResourceMetadataRow(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    updated_at: datetime
    updated_by: str
    created_at: datetime
    created_by: str

    @classmethod
    def from_request(cls, project_id: str, data: ResourceMetadataData, now: datetime) -> "ResourceMetadataRow":
        return cls(
            project_id=project_id,
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            updated_at=now,
            updated_by=data.updated_by,
            created_at=now,
            created_by=data.created_by,
        )

class UserWorkingStateRow(BaseModel):
    woven_id: str
    project_id: str
    viewer_settings: Optional[dict[str, Any]] = None
    last_tick: Optional[int] = None
    agent_id: Optional[str] = None
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_request(cls, project_id: str, woven_id: str, data: ResourceMetadataData, now: datetime) -> "UserWorkingStateRow":
        return cls(
            woven_id=woven_id,
            project_id=project_id,
            viewer_settings=data.viewer_settings,
            last_tick=data.last_tick,
            agent_id=data.agent_id,
            updated_at=now,
            created_at=now,
        )
