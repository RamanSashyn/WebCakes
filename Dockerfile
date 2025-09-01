FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD bash -lc "python manage.py migrate --noinput && \
              gunicorn WebCakes.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
