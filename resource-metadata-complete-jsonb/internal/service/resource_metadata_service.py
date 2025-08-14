
from fastapi import HTTPException

try:
    from internal.util.log_utils.logger import get_logger  # type: ignore
except Exception:
    def get_logger(name):
        class _L:
            def info(self, *a, **k): print(*a)
            def exception(self, *a, **k): print(*a)
        return _L()

from internal.schema.resource_metadata_schema import (
    GenerateResourceMetadataRequest,
    ResourceMetadataBody,
)
from internal.repository.postgres.resource_metadata_repository import (
    ResourceMetadataRepository,
    UserWorkingStateRepository,
)

class ResourceMetadataService:
    def __init__(self, resource_repo: ResourceMetadataRepository, user_state_repo: UserWorkingStateRepository):
        self.resource_repo = resource_repo
        self.user_state_repo = user_state_repo
        self.logger = get_logger(__name__)

    def upsert(self, project_id: str, woven_id: str, req: GenerateResourceMetadataRequest) -> None:
        try:
            self.resource_repo.upsert(project_id, req.data.model_dump())
            self.user_state_repo.upsert(project_id, woven_id, req.user_state.model_dump() if req.user_state else None)
            self.logger.info(f"Saved resource_metadata + user_working_state (jsonb): project_id={project_id}, woven_id={woven_id}")
        except Exception:
            self.logger.exception("ResourceMetadataService.upsert failed")
            raise HTTPException(status_code=500, detail="Failed to save metadata")

    def get(self, project_id: str) -> ResourceMetadataBody:
        row = self.resource_repo.get(project_id)
        if not row:
            raise HTTPException(status_code=404, detail="resource metadata not found")
        return ResourceMetadataBody(
            title=row["title"],
            description=row.get("description"),
            start_time=row["start_time"],
            end_time=row["end_time"],
            updated_by=row.get("updated_by"),
            created_by=row.get("created_by"),
        )

    def delete(self, project_id: str) -> None:
        existed = self.resource_repo.delete(project_id)
        if not existed:
            raise HTTPException(status_code=404, detail="resource metadata not found")
