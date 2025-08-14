
from __future__ import annotations
from typing import Any, Optional
from datetime import datetime
from sqlalchemy import Table, MetaData, select, insert, update, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

try:
    from internal.util.log_utils.logger import get_logger  # type: ignore
    _logger = get_logger(__name__)
except Exception:
    class _L:
        def info(self, *a, **k): print(*a)
        def error(self, *a, **k): print(*a)
        def exception(self, *a, **k): print(*a)
    _logger = _L()

class ResourceMetadataRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        md = MetaData()
        self.table: Table = Table("resource_metadata", md, autoload_with=self.engine)

    def upsert(self, project_id: str, data: dict[str, Any]) -> None:
        now = datetime.utcnow()
        payload = {
            "project_id": project_id,
            "title": data["title"],
            "description": data.get("description"),
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "updated_by": data["updated_by"],
            "created_by": data["created_by"],
            "updated_at": now,
        }
        try:
            with self.engine.begin() as conn:
                exists = conn.execute(
                    select(self.table.c.project_id).where(self.table.c.project_id == project_id)
                ).fetchone()
                if exists:
                    conn.execute(update(self.table).where(self.table.c.project_id == project_id).values(**payload))
                    _logger.info(f"[resource_metadata] updated project_id={project_id}")
                else:
                    payload["created_at"] = now
                    conn.execute(insert(self.table).values(**payload))
                    _logger.info(f"[resource_metadata] inserted project_id={project_id}")
        except SQLAlchemyError as e:
            _logger.error(f"[resource_metadata] upsert failed: {e}")
            raise

    def get(self, project_id: str) -> Optional[dict[str, Any]]:
        try:
            with self.engine.connect() as conn:
                row = conn.execute(
                    select(self.table).where(self.table.c.project_id == project_id)
                ).fetchone()
                return dict(row._mapping) if row else None
        except SQLAlchemyError as e:
            _logger.error(f"[resource_metadata] get failed: {e}")
            raise

    def delete(self, project_id: str) -> bool:
        try:
            with self.engine.begin() as conn:
                res = conn.execute(delete(self.table).where(self.table.c.project_id == project_id))
                _logger.info(f"[resource_metadata] deleted count={res.rowcount} project_id={project_id}")
                return res.rowcount > 0
        except SQLAlchemyError as e:
            _logger.error(f"[resource_metadata] delete failed: {e}")
            raise

class UserWorkingStateRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        md = MetaData()
        self.table: Table = Table("user_working_state", md, autoload_with=self.engine)

    def upsert(self, project_id: str, woven_id: str, state: dict[str, Any] | None) -> None:
        now = datetime.utcnow()
        state = state or {}
        payload = {
            "project_id": project_id,
            "woven_id": woven_id,
            "viewer_settings": state.get("viewer_settings"),
            "last_tick": state.get("last_tick"),
            "agent_id": state.get("agent_id"),
            "updated_at": now,
        }
        try:
            with self.engine.begin() as conn:
                exists = conn.execute(
                    select(self.table.c.woven_id).where(
                        (self.table.c.woven_id == woven_id) & (self.table.c.project_id == project_id)
                    )
                ).fetchone()
                if exists:
                    conn.execute(
                        update(self.table)
                        .where((self.table.c.woven_id == woven_id) & (self.table.c.project_id == project_id))
                        .values(**payload)
                    )
                    _logger.info(f"[user_working_state] updated woven_id={woven_id}, project_id={project_id}")
                else:
                    payload["created_at"] = now
                    conn.execute(insert(self.table).values(**payload))
                    _logger.info(f"[user_working_state] inserted woven_id={woven_id}, project_id={project_id}")
        except SQLAlchemyError as e:
            _logger.error(f"[user_working_state] upsert failed: {e}")
            raise
