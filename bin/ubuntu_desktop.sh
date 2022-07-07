sudo apt update
sudo apt-get install build-essential cmake
sudo apt-get install curl
sudo apt-get install git
sudo apt-get install zsh
sudo apt-get install net-tools
sudo apt-get install openssh-server
sudo apt-get install vim
sudo apt-get install ibus-pinyin

curl -sLf https://spacevim.org/install.sh | bash
# install communi theme
sudo snap install communitheme --edge
# install vscode
sudo snap install --classic code
# install neovim
sudo apt install neovim
sudo apt install silversearcher-ag
sudo apt install npm

# location=/usr/local/bin/tldr
# sudo wget -qO $location https://raw.githubusercontent.com/pepa65/tldr-bash-client/master/tldr
# sudo chmod +x $location

#sudo add-apt-repository ppa:h-realh/roxterm
#sudo apt-get update
#sudo apt-get install roxterm

cat /etc/shells
chsh -s /usr/bin/zsh

sudo snap install sublime-text --classic

sudo apt-get install GConf2

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
