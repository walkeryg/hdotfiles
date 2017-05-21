sudo apt-get install silversearcher-ag
sudo apt-get install rxvt-unicode
sudo apt-get install tmux
sudo apt-get install jq

location=/usr/local/bin/tldr
sudo wget -qO $location https://raw.githubusercontent.com/pepa65/tldr-bash-client/master/tldr
sudo chmod +x $location

sudo add-apt-repository ppa:niko2040/e19
sudo apt-get update
sudo apt-get install enlightenment
sudo apt-get install terminology

sudo add-apt-repository ppa:h-realh/roxterm
sudo apt-get update
sudo apt-get install roxterm
