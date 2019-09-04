#!/bin/bash

# eval "$(ssh-agent -s)" &&
# ssh-add -k ~/.ssh/id_rsa &&
# cd /var/www/helloworld
# git pull

# source ~/.profile
# echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin

# sudo docker stop f75a6172a8a9
# sudo docker rm f75a6172a8a9

# sudo docker rmi syamsuldocker/backend_automate
sudo docker pull syamsuldocker/backend_automate
# sudo docker stop be64e3dc3f39
# sudo docker run -d -p 5001:5001 syamsuldocker/backend_automate:latest