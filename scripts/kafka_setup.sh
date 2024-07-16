#!/bin/bash

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing Docker..."
sudo apt-get -y install docker.io python3-pip

echo "Docker without sudo setup..."
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart

echo "Cloning git repository"
git clone https://github.com/ilhamaulanap/streamcommerce.git


# Install Kafka requirements.txt
echo "Install Kafka requirements.txt"
pip install --no-cache-dir -r streamcommerce/kafka/requirements.txt

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
echo "Starting Kafka using docker-compose"
docker-compose up -d

# Wait for Kafka containers to be healthy
echo "Waiting for Kafka containers to be healthy..."
docker-compose ps kafka | grep "healthy"
while [ $? -ne 0 ]; do
    sleep 5
    docker-compose ps kafka | grep "healthy"
done

# Run Python script in the background with nohup
echo "Running Python script in the background with nohup"
nohup python3 producer_sales_data.py > output.log 2>&1 &


echo "All processes started"
