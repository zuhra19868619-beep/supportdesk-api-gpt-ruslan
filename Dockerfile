FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ /app/
RUN python manage.py collectstatic --noinput
CMD ["sh","-c","python manage.py migrate --noinput && python manage.py seed_categories && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
