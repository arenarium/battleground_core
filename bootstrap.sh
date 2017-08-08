sudo apt-get update
sudo apt-get install -y zsh curl python3 python3-venv
#sudo chsh -s /bin/zsh ubuntu
zsh
git clone git://github.com/robbyrussell/oh-my-zsh.git .oh-my-zsh
cp .oh-my-zsh/templates/zshrc.zsh-template .zshrc
sudo chsh -s /bin/zsh ubuntu

curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install nodejs
sudo apt-get install build-essential
sudo npm install npm@latest -g
sudo npm install -g create-react-app

sudo echo "
source ~/python3/bin/activate
cd /vagrant
export PYTHONPATH=$PYTHONPATH:/vagrant
" >> .zshrc
