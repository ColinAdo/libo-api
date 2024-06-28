# Requirement to dockerize a project
1. Setting Config:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER')
    variable in env file CELERY_BROKER='redis://redis:6379/0'
2. Base project directory:
    from .celery import app as app_celery

    __all__ = ("app_celery",)
3. Install redis:
    pip install redis
4. Dockerfile:
    FROM python:3

    ENV PYTHONUNBUFFERED=1

    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install -r requirements.txt
5. Docker Compose.yml:
    version: "3.9"

    services:
    django:
        build: .
        container_name: django
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
        - .:/usr/src/app/
        ports:
        - "8000:8000"

        depends_on:
        - pgdb
        - redis
    celery:
        build: .
        command: celery -A core worker -l INFO
        volumes:
        - .:/usr/src/app/
        depends_on:
        - django
        - redis
    pgdb:
        image: postgres
        container_name: pgbd
        environment:
        - POSTGRES_DB=postgres
        - POSTGRES_USER=postgres
        - POSTGRES_PASSWORD=postgres
        volumes:
        - pgdata:/var/lib/postgresql/data/

    redis:
        image: "redis:alpine"
    volumes:
    pgdata:

6. Commands:
    docker-compose run build To build the app
    docker-compose up to run the server
    docker-compose down -v To stop the server and remove other images
    docker-compose rm to remove images completely
    docker-compose up --build --forece-recreate to force build
    docker-compose up to run the server

