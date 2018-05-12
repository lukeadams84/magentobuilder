#!/bin/bash

# Create overlay networks for projects and swarm
docker swarm init
# Proxy Network
docker network create -d overlay --attachable --subnet=10.10.10.0/24 --gateway=10.10.10.254 proxy

# Internal Network
docker network create -d overlay --attachable --subnet=10.10.20.0/24 --gateway=10.10.20.254 --internal internal

# Run proxy components
docker stack deploy -c ./sharedservices/docker-compose.yml proxy

echo 'To download images from dockerhub you need to authenticate. Ensure you use your username (found at the top right of the dockerhub site once you are logged in)'

docker login

.magento/srcfiles/download.sh
