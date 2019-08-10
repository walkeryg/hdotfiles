#!/bin/bash

# change source
sudo pacman-mirrors -i -c China -m rank

# sudo pacman -Syy --force
sudo pacman -Syy 

# add archlinuxcn source
sudo echo "[archlinuxcn]" >> /etc/pacman.conf
sudo echo "SigLevel = Optional TrustedOnly" >> /etc/pacman.conf
sudo echo "Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch" >> /etc/pacman.conf

# install archlinuxcn-keyring
sudo pacman -Syy
sudo pacman -S archlinuxcn-keyring
sudo pacman -Syyu

sudo pacman -S google-chrome

chsh -s /bin/zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/plugins/zsh-syntax-highlighting
git clone https://github.com/lukechilds/zsh-nvm ~/.oh-my-zsh/custom/plugins/zsh-nvm
sudo pacman -S autojump

# plugins=( git zsh-syntax-highlighting zsh-autosuggestions autojump zsh-nvm )
# ZSH_THEME="agnoster"
# export NVM_LAZY_LOAD=true

curl -sLf https://spacevim.org/install.sh | bash

sudo pacman -S fcitx-im
sudo pacman -S fcitx-configtool
sudo pacman -S fcitx-sogoupinyin

echo "export GTK_IM_MODULE=fcitx" >> ~/.xprofile
echo "export QT_IM_MODULE=fcitx" >> ~/.xprofile
echo "export XMODIFIERS="@im=fcitx"" >> ~/.xprofile
sudo pacman -S fcitx-qt4
# sudo pacman -S electronic-webchat

sudo pacman -S yay base-devel
yay -S yaourt
yay -S netease-cloud-music
