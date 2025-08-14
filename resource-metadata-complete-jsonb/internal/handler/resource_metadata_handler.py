
from fastapi import APIRouter, Depends, Header, Request
from typing import Annotated

try:
    from internal.util.log_utils.logger import get_logger  # type: ignore
except Exception:
    def get_logger(name):
        class _L:
            def info(self, *a, **k): print(*a)
        return _L()

from internal.service.resource_metadata_service import ResourceMetadataService
from internal.schema.resource_metadata_schema import (
    GenerateResourceMetadataRequest,
    GenerateResourceMetadataResponse,
    GetResourceMetadataResponse,
)

router = APIRouter()
logger = get_logger(__name__)

def get_service(request: Request) -> ResourceMetadataService:
    return request.app.state.resource_metadata_service  # type: ignore[attr-defined]

@router.post(
    "/dtc-viewer/projects/{project_id}/resource_metadata",
    response_model=GenerateResourceMetadataResponse,
)
async def create_or_update_resource_metadata(
    project_id: str,
    request_body: GenerateResourceMetadataRequest,
    x_woven_id: Annotated[str, Header(alias="X-Woven-Id")],
    service: Annotated[ResourceMetadataService, Depends(get_service)],
):
    service.upsert(project_id, x_woven_id, request_body)
    return GenerateResourceMetadataResponse(message="ok")

@router.get(
    "/dtc-viewer/projects/{project_id}/resource_metadata",
    response_model=GetResourceMetadataResponse,
)
async def get_resource_metadata(
    project_id: str,
    service: Annotated[ResourceMetadataService, Depends(get_service)],
):
    data = service.get(project_id)
    return GetResourceMetadataResponse(project_id=project_id, data=data)

@router.delete(
    "/dtc-viewer/projects/{project_id}/resource_metadata",
    response_model=GenerateResourceMetadataResponse,
)
async def delete_resource_metadata(
    project_id: str,
    service: Annotated[ResourceMetadataService, Depends(get_service)],
):
    service.delete(project_id)
    return GenerateResourceMetadataResponse(message="deleted")
