
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class ResourceMetadataBody(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    updated_by: str
    created_by: str

class UserWorkingStateBody(BaseModel):
    viewer_settings: Optional[dict[str, Any]] = None
    last_tick: Optional[int] = None
    agent_id: Optional[str] = None

class GenerateResourceMetadataRequest(BaseModel):
    data: ResourceMetadataBody
    user_state: Optional[UserWorkingStateBody] = None

class GenerateResourceMetadataResponse(BaseModel):
    message: str = "ok"

class GetResourceMetadataResponse(BaseModel):
    project_id: str
    data: ResourceMetadataBody
