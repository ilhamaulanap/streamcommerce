#!/bin/bash

# Change directory to where your docker-compose.yml is located
echo "Running Kafka using docker-compose"
cd streamcommerce/airflow
docker-compose build

echo "Running airflow-init"
docker-compose up airflow-init

# Start airflow containers
echo "Starting Kafka using docker-compose"
docker-compose up -d



echo "Airflow running in detached mode"
