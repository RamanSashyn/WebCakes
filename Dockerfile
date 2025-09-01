FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

# Gunicorn как WSGI/ASGI сервер
CMD gunicorn WebCakes.wsgi:application --bind 0.0.0.0:${PORT:-8000}
