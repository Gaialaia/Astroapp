FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/astro_app

WORKDIR /astro_app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    python3-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise requests ydb django-ydb-backend

COPY . .

RUN SECRET_KEY=build-time-only-key python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate --noinput; gunicorn --bind 0.0.0.0:$PORT astroknow.wsgi:application"]


# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "astroknow.wsgi:application"]


# CMD ["sh", "-c", "python manage.py migrate --noinput; gunicorn --bind 0.0.0.0:$PORT --timeout 90 --workers 2 astroknow.wsgi:application"]







# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install gunicorn whitenoise requests psycopg2-binary dj-database-url

# CMD ["sh", "-c", "python manage.py migrate --noinput; \
#     python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='Gaia').exists() or User.objects.create_superuser('Gaia', 'volodeya@gmail.com', 'giant')\"; \
#     gunicorn --bind 0.0.0.0:$PORT astroknow.wsgi:application"]


