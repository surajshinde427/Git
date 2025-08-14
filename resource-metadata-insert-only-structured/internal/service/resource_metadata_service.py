
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from internal.schema.resource_metadata_schema import (
    GenerateResourceMetadataRequest,
    ResourceMetadataRow,
    UserWorkingStateRow,
)
from internal.repository.postgres.resource_metadata_repository import ResourceMetadataRepository

class ResourceMetadataService:
    def __init__(self, repo: ResourceMetadataRepository):
        self.repo = repo

    def create(self, project_id: str, woven_id: str, req: GenerateResourceMetadataRequest) -> None:
        now = datetime.now(timezone.utc).astimezone(timezone.utc).replace(tzinfo=None)  # naive UTC for DB timestamps
        resource_row = ResourceMetadataRow.from_request(project_id, req.data, now)
        user_row = UserWorkingStateRow.from_request(project_id, woven_id, req.data, now)

        try:
            self.repo.insert_resource_metadata(resource_row)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="resource_metadata already exists for this project_id")

        try:
            self.repo.insert_user_working_state(user_row)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="user_working_state already exists for this user+project")
