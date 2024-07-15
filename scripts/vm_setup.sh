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


echo "Install requirements.txt"
pip install --no-cache-dir -r streamcommerce/requirements.txt

