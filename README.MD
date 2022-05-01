# CS50w Commerce
Revisiting my first [django](https://docs.djangoproject.com/en/3.2/) app. This project does not aim to reproduce all of ebay's functionality but does intend to generally allow any user to view content and for authenticated users to create or interact with auctions.



## Prerequisites

This project uses docker for local development, to ensure that docker and docker-compose are properly installed on your local system please review [Docker's installation guide] (https://docs.docker.com/get-docker/) and[Docker-Compose](https://docs.docker.com/compose/install/)

### Build stage
This project utilizes the [python3.9-slim-bullseye](https://hub.docker.com/_/python) image - depending on how exicted you are about the new python 3.11 features you may update the local and production Django Dockerfiles to your desired python version (currently 3.7-3.11.0).

**Note** this project is tested/run on Debian flavored linux containers. You will need to embark on your own Dockerfile journey should you want to use Alpine linux for an itty bitty image size.

```bash
$ docker-compose -f local.yml build
```
