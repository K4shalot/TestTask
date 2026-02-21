# Travel Planner

Backend API for planning trips and collecting places (Art Institute of Chicago). Projects, places, notes, visited status.

---

## Where do env variables come from?

- **File `.env`** in the project root. Not committed (in `.gitignore`).
- **Create it** by copying the example:  
  `cp .env.example .env` (or copy the contents by hand).
- **Loading:** Django loads them in `travel_planner/settings.py` via `python-dotenv` (if installed). So after `pip install -r requirements.txt`, variables from `.env` are used automatically.
- **If there is no `.env`:** the app still runs: `SECRET_KEY` and `DEBUG` fall back to defaults from settings (dev-only).

**Example `.env`:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=1
```

For Docker, envs can also be set in `docker-compose.yml` or in the environment; see [Docker](#docker) below.

---

## Run manually (runserver)

1. **Clone and enter the project:**
   ```bash
   cd TestTask
   ```

2. **Create virtualenv and install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Optional: env file**
   ```bash
   copy .env.example .env   # Windows
   # cp .env.example .env   # Linux/macOS
   ```
   Edit `.env` if you want another `SECRET_KEY` or `DEBUG=0`.

4. **Migrations and run server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Optional: create superuser (for `/admin/`):**
   ```bash
   python manage.py createsuperuser
   ```
   Then open http://127.0.0.1:8000/admin/ and log in.

6. **URLs:**
   - API root: http://127.0.0.1:8000/api/
   - **Swagger UI:** http://127.0.0.1:8000/api/docs/
   - OpenAPI schema: http://127.0.0.1:8000/api/schema/
   - Admin: http://127.0.0.1:8000/admin/

---

## Docker

1. **Build and run:**
   ```bash
   docker compose up --build
   ```

2. **Same URLs** (port 8000):
   - API root: http://127.0.0.1:8000/api/
   - Swagger: http://127.0.0.1:8000/api/docs/
   - Admin: http://127.0.0.1:8000/admin/

3. **Create superuser in Docker:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

4. **Env in Docker:** set in `docker-compose.yml` or a `.env` file next to it (e.g. `DJANGO_SECRET_KEY`, `DEBUG`). See `DOCKER.md` for details.

---

## API overview

- **Projects:** `GET/POST /api/projects/`, `GET/PATCH/DELETE /api/projects/<id>/`
- **Places (nested):** `GET/POST /api/projects/<id>/places/`, `GET/PATCH /api/projects/<id>/places/<place_id>/`
- Create project with places in one request: `POST /api/projects/` with body `{"name": "...", "places": ["27992", "28560"]}`

Full docs: **http://127.0.0.1:8000/api/docs/** (Swagger).
