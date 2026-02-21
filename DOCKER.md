# Running the Travel Planner with Docker

## Quick start

```bash
# Build and run (first time runs migrations automatically)
docker compose up --build

# API: http://localhost:8000
```

Run in the background:

```bash
docker compose up --build -d
```

## Settings for Docker

1. **SQLite path (so data survives restarts)**  
   In your Django `settings.py`, set the database path from the environment:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.environ.get('SQLITE_PATH', BASE_DIR / 'db.sqlite3'),
       }
   }
   ```
   Docker Compose sets `SQLITE_PATH=/app/db/db.sqlite3` and mounts a volume at `/app/db`.

## Useful commands

| Command | Description |
|--------|-------------|
| `docker compose up --build` | Build image and start the service |
| `docker compose up -d` | Start in background |
| `docker compose down` | Stop and remove containers |
| `docker compose exec web python manage.py migrate` | Run migrations |
| `docker compose exec web python manage.py createsuperuser` | Create admin user |
