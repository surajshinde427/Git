
# Resource Metadata API — Insert-Only, Structured (Service doesn't build payloads)

Design:
- **Service** orchestrates only.
- **Schema** defines API request DTO + DB row DTOs and factory methods to build rows.
- **Repository** inserts those row DTOs. No updates. Conflicts -> 409 in service.

Endpoint:
- POST `/dtc-viewer/projects/{project_id}/resource_metadata`
  - Header: `X-Woven-Id: <user-id>`
  - Body:
    {
      "data": {
        "title": "Run 01",
        "description": "QA",
        "start_time": "2025-08-24T01:00:00Z",
        "end_time": "2025-08-24T01:20:00Z",
        "updated_by": "suraj",
        "created_by": "suraj",
        "viewer_settings": {"theme":"dark"},
        "last_tick": 0,
        "agent_id": "car-alpha"
      }
    }

Wiring example:
    from sqlalchemy import create_engine
    from fastapi import FastAPI
    from internal.handler.resource_metadata_handler import router as resource_metadata_router
    from internal.service.resource_metadata_service import ResourceMetadataService
    from internal.repository.postgres.resource_metadata_repository import ResourceMetadataRepository

    engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
    app = FastAPI()
    app.state.resource_metadata_service = ResourceMetadataService(ResourceMetadataRepository(engine))
    app.include_router(resource_metadata_router)

Tables:
- See `internal/db/tables.py` for SQLAlchemy `Table` classes (JSONB viewer_settings, unique constraint on (woven_id, project_id)).
