# CS50w Commerce
Revisiting my first [django](https://docs.djangoproject.com/en/3.2/) app. This project does not aim to reproduce all of ebay's functionality but does intend to generally allow any user to view content and for authenticated users to create or interact with auctions.



### Prerequisites

This project uses docker for local development, to ensure that docker and docker-compose are properly installed on your local system please review [Docker's installation guide] (https://docs.docker.com/get-docker/) and[Docker-Compose](https://docs.docker.com/compose/install/)

### Build stage
This project utilizes the [python3.9-slim-bullseye](https://hub.docker.com/_/python) image - depending on how exicted you are about the new python 3.11 features you may update the local and production Django Dockerfiles to your desired python version (currently 3.7-3.11.0).

**Note** this project is tested/run on Debian flavored linux containers. You will need to embark on your own Dockerfile journey should you want to use Alpine linux for an itty bitty image size.

```bash
$ docker-compose -f local.yml build
```

### Pre-commit
Check out pre-commit to catch any nitpicky issues before they are pushed to the remote repository. Before committing any code please follow [pre-commit's installation instructions](https://pre-commit.com/#install)

Here we are creating a local virtual environment to contain this locally installed version of pre-commit.
```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install pre-commit
$ pre-commit install
```

## Local development

Now we're ready to roll, simply run the following to launch the dev server
```bash
$ docker-compose -f local.yml up
```

### Management commands and directly accessing your django container

To run migrations and create your first superuser
```bash
$ docker-compose -f local.yml run --rm django python manage.py migrate
$ docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

To directly access a local container you can view all running containers by running:
```bash
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED       STATUS       PORTS                                       NAMES
934c0f431cc4   wagtail_web            "./manage.py runserv…"   5 weeks ago   Up 5 weeks   0.0.0.0:8085->8085/tcp, :::8085->8085/tcp   web
a7d06cdda977   wagtail_frontend       "docker-entrypoint.s…"   5 weeks ago   Up 5 weeks                                               frontend
aa183c54dc68   postgres:12.3-alpine   "docker-entrypoint.s…"   5 weeks ago   Up 5 weeks   5432/tcp                                    db
```

You can then directly log into the target container by running the following with either the IMAGE_NAME or IMAGE_ID of the container:
```bash
$ docker exec -it bash IMAGE_NAME
```
or
```bash
$ docker exec -it bash IMAGE_ID
```

**Note** I've found that you will need to update two environment variables inside of the django container in order to successfully interact with postgres.
```bash
$ export CELERY_BROKER_URL="${REDIS_URL}"
$ export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
```

both of these env variable export commands can be found in the compose/production/django/entrypoin.sh file.
