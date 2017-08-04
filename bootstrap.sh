sudo apt-get update
sudo apt-get install -y zsh curl python3 python3-venv
#sudo chsh -s /bin/zsh ubuntu
zsh
git clone git://github.com/robbyrussell/oh-my-zsh.git .oh-my-zsh
cp .oh-my-zsh/templates/zshrc.zsh-template .zshrc
sudo chsh -s /bin/zsh ubuntu

sudo echo "
source ~/python3/bin/activate
cd /vagrant
" >> .zshrc
