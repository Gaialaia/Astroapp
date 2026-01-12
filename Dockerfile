FROM python:3.13-slim

WORKDIR /astro_app

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .

# WORKDIR /app/astroknow

RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-traditional
RUN pip install --no-cache-dir -r requirements.txt

COPY . /astro_app

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "astroknow.wsgi:application"]

COPY ./start.sh /astro_app/start.sh
RUN chmod +x /astro_app/start.sh
# to run db
CMD ["/astro_app/start.sh"]




