#!/bin/bash

# Fetch external IP address using metadata server
EXTERNAL_IP=$(curl -s -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)

# Export as KAFKA_ADDRESS
export KAFKA_ADDRESS=$EXTERNAL_IP

# Verify the exported IP address
echo "Exported KAFKA_ADDRESS: $KAFKA_ADDRESS"

# Change directory to where your docker-compose.yml is located
echo "Running Kafka using docker-compose"
cd streamcommerce/kafka

# Start Kafka and Zookeeper containers
echo "Running Kafka using docker-compose"
docker-compose up -d
