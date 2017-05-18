sudo apt-get install silversearcher-ag
sudo apt-get install rxvt-unicode
sudo apt-get install tmux
sudo apt-get install jq

location=/usr/local/bin/tldr
sudo wget -qO $location https://raw.githubusercontent.com/pepa65/tldr-bash-client/master/tldr
sudo chmod +x $location
