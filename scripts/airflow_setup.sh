#!/bin/bash

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing Docker..."
sudo wget -qO- https://get.docker.com/ | sh

echo "Docker without sudo setup..."
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart

echo "Cloning git repository"
git clone https://github.com/ilhamaulanap/streamcommerce.git


# Change directory to where your docker-compose.yml is located
echo "Running Airflow using docker-compose"
cd streamcommerce/airflow
docker compose build

echo "Running airflow-init"
docker compose up airflow-init

# Start airflow containers
echo "Airflow running in detached mode"
docker compose up -d



