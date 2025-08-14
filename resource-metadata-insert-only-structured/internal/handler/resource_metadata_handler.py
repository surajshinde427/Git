
from fastapi import APIRouter, Depends, Header, Request
from typing import Annotated

from internal.schema.resource_metadata_schema import (
    GenerateResourceMetadataRequest,
    GenerateResourceMetadataResponse,
)
from internal.service.resource_metadata_service import ResourceMetadataService

router = APIRouter()

def get_service(request: Request) -> ResourceMetadataService:
    return request.app.state.resource_metadata_service  # type: ignore[attr-defined]

@router.post(
    "/dtc-viewer/projects/{project_id}/resource_metadata",
    response_model=GenerateResourceMetadataResponse,
)
async def create_resource_metadata(
    project_id: str,
    request_body: GenerateResourceMetadataRequest,
    x_woven_id: Annotated[str, Header(alias="X-Woven-Id")],
    service: Annotated[ResourceMetadataService, Depends(get_service)],
):
    service.create(project_id, x_woven_id, request_body)
    return GenerateResourceMetadataResponse(message="ok")
