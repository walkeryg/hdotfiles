
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

