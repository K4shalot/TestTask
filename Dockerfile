FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV DJANGO_WSGI=travel_planner.wsgi:application
CMD sh -c "python manage.py migrate --noinput && gunicorn ${DJANGO_WSGI} --bind 0.0.0.0:8000 --access-logfile - --capture-output"
