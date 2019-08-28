#!/bin/bash

# eval "$(ssh-agent -s)" &&
# ssh-add -k ~/.ssh/id_rsa &&
# cd /var/www/helloworld
# git pull

# source ~/.profile
# echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin

sudo docker stop syamsuldocker/backend_automate
sudo docker rm syamsuldocker/backend_automate
sudo docker rmi syamsuldocker/backend_automate
sudo docker pull syamsuldocker/backend_automate
sudo docker stop 9e57ccefccf3
sudo docker run -d -p 5001:5001 syamsuldocker/backend_automate:latest