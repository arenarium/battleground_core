sudo apt-get update
sudo apt-get install -y zsh curl python3 python3-venv language-pack-en
sudo apt-get install -y ruby ruby-dev gcc make libffi-dev

sudo gem install travis -v 1.8.8 --no-rdoc --no-ri

curl -L https://github.com/docker/machine/releases/download/v0.12.2/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine
chmod +x /tmp/docker-machine
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
