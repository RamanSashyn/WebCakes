FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PORT=8000
CMD python manage.py migrate --noinput \
 && python manage.py collectstatic --noinput \
 && gunicorn WebCakes.wsgi:application --bind 0.0.0.0:$PORT
