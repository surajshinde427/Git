
# Resource Metadata + User Working State API (JSONB viewer_settings)

## Endpoints
- POST `/dtc-viewer/projects/{project_id}/resource_metadata`
- GET `/dtc-viewer/projects/{project_id}/resource_metadata`
- DELETE `/dtc-viewer/projects/{project_id}/resource_metadata`

`viewer_settings` is stored as JSONB in Postgres.

## Migration
```sql
ALTER TABLE public.user_working_state
  ALTER COLUMN viewer_settings TYPE jsonb
  USING CASE
    WHEN viewer_settings IS NULL OR btrim(viewer_settings) = '' THEN NULL
    WHEN viewer_settings ~ '^[\[{].*[\]}]$' THEN viewer_settings::jsonb
    ELSE to_jsonb(viewer_settings)
  END;

CREATE INDEX IF NOT EXISTS user_working_state_viewer_settings_gin
  ON public.user_working_state USING GIN (viewer_settings);
```
