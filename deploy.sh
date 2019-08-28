#!/bin/bash

# eval "$(ssh-agent -s)" &&
# ssh-add -k ~/.ssh/id_rsa &&
# cd /var/www/helloworld
# git pull

# source ~/.profile
# echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin

sudo docker stop syamsuldocker/image_test
sudo docker rm syamsuldocker/image_test
sudo docker rmi syamsuldocker/image_test
sudo docker pull syamsuldocker/image_test
sudo docker run -d -p 8000:8000 syamsuldocker/image_test:latest