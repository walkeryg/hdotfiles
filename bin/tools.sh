sudo apt update
sudo apt-get install build-essential cmake
sudo apt-get install zsh
sudo apt-get install silversearcher-ag
sudo apt-get install rxvt-unicode
sudo apt-get install tmux
sudo apt-get install jq
sudo apt-get install tree

sudo apt-get install net-tools

location=/usr/local/bin/tldr
sudo wget -qO $location https://raw.githubusercontent.com/pepa65/tldr-bash-client/master/tldr
sudo chmod +x $location

#sudo add-apt-repository ppa:niko2040/e19
#sudo apt-get update
#sudo apt-get install enlightenment
#sudo apt-get install terminology

#sudo add-apt-repository ppa:h-realh/roxterm
#sudo apt-get update
#sudo apt-get install roxterm

cat /etc/shells
chsh -s /usr/bin/zsh

sudo apt-get install curl
sudo apt-get install git
sudo apt-get install vim
sudo apt-get install neovim
sudo apt-get install ibus-pinyin
curl -sLf https://spacevim.org/install.sh | bash

sudo apt-get install ubuntu-make

#sublime
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text

umake ide visual-studio-code 
sudo apt-get install GConf2

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
