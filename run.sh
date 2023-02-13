#!/usr/bin/bash

now=$(date)
line="========================= $now ========================="

echo $line
echo "Runing git pull to git branch develop"
git pull origin develop

now=$(date)
echo $line
echo "Runing Docker Build"
sudo docker-compose build

now=$(date)
echo $line
echo "Runing Docker Up"
sudo docker-compose up
