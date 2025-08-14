
from sqlalchemy import Table, Column, Text, Integer, TIMESTAMP, MetaData, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

resource_metadata_table = Table(
    "resource_metadata",
    metadata,
    Column("project_id", Text, primary_key=True),
    Column("title", Text, nullable=False),
    Column("description", Text),
    Column("start_time", TIMESTAMP(timezone=True), nullable=False),
    Column("end_time", TIMESTAMP(timezone=True), nullable=False),
    Column("updated_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
    Column("updated_by", Text, nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
    Column("created_by", Text, nullable=False),
)

user_working_state_table = Table(
    "user_working_state",
    metadata,
    Column("woven_id", Text, nullable=False),
    Column("project_id", Text, nullable=False),
    Column("viewer_settings", JSONB),
    Column("last_tick", Integer),
    Column("agent_id", Text),
    Column("updated_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
    UniqueConstraint("woven_id", "project_id", name="uq_user_working_state_woven_project")
)
