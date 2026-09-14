# Database migrations

The application schema is versioned with Alembic. `0001_initial_schema` creates the initial SQLite schema; startup runs `alembic upgrade head` before the API process starts.

Future schema changes must add a new revision to `migrations/versions/`. Do not use `Base.metadata.create_all()` or destructive schema operations against an installed database outside a reviewed Alembic revision.
