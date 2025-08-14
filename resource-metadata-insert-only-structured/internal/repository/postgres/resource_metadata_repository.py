
from __future__ import annotations
from sqlalchemy import insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from internal.db.tables import resource_metadata_table, user_working_state_table
from internal.schema.resource_metadata_schema import ResourceMetadataRow, UserWorkingStateRow

class ResourceMetadataRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_resource_metadata(self, row: ResourceMetadataRow) -> None:
        try:
            with self.engine.begin() as conn:
                conn.execute(insert(resource_metadata_table).values(**row.model_dump()))
        except IntegrityError:
            # duplicate project_id (PK)
            raise
        except SQLAlchemyError:
            raise

    def insert_user_working_state(self, row: UserWorkingStateRow) -> None:
        try:
            with self.engine.begin() as conn:
                conn.execute(insert(user_working_state_table).values(**row.model_dump()))
        except IntegrityError:
            # duplicate (woven_id, project_id)
            raise
        except SQLAlchemyError:
            raise
