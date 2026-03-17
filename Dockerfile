FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/astro_app

WORKDIR /astro_app

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise


COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT astroknow.wsgi:application"]




