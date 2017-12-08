#!/bin/bash
docker login -u $DOCKER_USER -p $DOCKER_API_KEY
docker push battleground/uwsgi:latest
docker push battleground/nginx:latest
docker push battleground/uwsgi:latest
docker push battleground/battleground:latest
