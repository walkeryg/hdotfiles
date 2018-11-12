sudo apt update
sudo apt-get install build-essential cmake
sudo apt-get install curl
sudo apt-get install git
sudo apt-get install zsh
sudo apt-get install net-tools
sudo apt-get install openssh-server
sudo apt-get install vim
sudo apt-get install ibus-pinyin
sudo apt-get install ubuntu-make
curl -sLf https://spacevim.org/install.sh | bash

sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

# change brew mirror source
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

# reset brew source
# cd "$(brew --repo)"
# git remote set-url origin https://github.com/Homebrew/brew.git

# cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
# git remote set-url origin https://github.com/Homebrew/homebrew-core.git
echo "export PATH='$(brew --prefix)/bin:$(brew --prefix)/sbin'":'"$PATH"' >>~/.profile

brew install the_silver_searcher
brew install tmux
# sudo apt-get install rxvt-unicode
brew install jq
brew install tree
brew install tldr
brew install neovim
brew install bat
brew install prettyping
brew install fzf
brew install htop
brew install diff-so-fancy
brew install fd
brew install ncdu
brew install noti
brew install lolcat
brew install neofetch
brew install tig
brew install autojump
brew install exa
brew install colorls

# location=/usr/local/bin/tldr
# sudo wget -qO $location https://raw.githubusercontent.com/pepa65/tldr-bash-client/master/tldr
# sudo chmod +x $location

#sudo add-apt-repository ppa:h-realh/roxterm
#sudo apt-get update
#sudo apt-get install roxterm

cat /etc/shells
chsh -s /usr/bin/zsh

#sublime
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text

umake ide visual-studio-code 
sudo apt-get install GConf2

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
