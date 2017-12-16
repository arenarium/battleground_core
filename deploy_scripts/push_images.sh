#!/bin/bash
docker login -u $DOCKER_USER -p $DOCKER_API_KEY
docker push battleground/battleground:latest
