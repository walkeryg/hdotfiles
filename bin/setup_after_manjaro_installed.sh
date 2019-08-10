#!/bin/bash

# change source
sudo pacman-mirrors -i -c China -m rank

# sudo pacman -Syy --force
sudo pacman -Syy 

# add archlinuxcn source
sudo cp /etc/pacman.conf /etc/pacman.conf.bak
cp /etc/pacman.conf /tmp/pacman.conf
echo "[archlinuxcn]" >> /tmp/pacman.conf
echo "SigLevel = Optional TrustedOnly" >> /tmp/pacman.conf
echo "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch" >> /tmp/pacman.conf
sudo cp /tmp/pacman.conf /etc/pacman.conf

# install archlinuxcn-keyring
sudo pacman -Syy
sudo pacman -S archlinuxcn-keyring
sudo pacman -Syyu

sudo pacman -S google-chrome

sudo pacman -S autojump


curl -sLf https://spacevim.org/install.sh | bash

sudo pacman -S fcitx-im
sudo pacman -S fcitx-configtool
sudo pacman -S fcitx-sogoupinyin

echo "export GTK_IM_MODULE=fcitx" >> ~/.xprofile
echo "export QT_IM_MODULE=fcitx" >> ~/.xprofile
echo "export XMODIFIERS="@im=fcitx"" >> ~/.xprofile
sudo pacman -S fcitx-qt4
sudo pacman -S wqy-microhei
sudo pacman -S bat
sudo pacman -S fzf
sudo pacman -S prettyping
sudo pacman -S ncdu
sudo pacman -S tldr
# sudo pacman -S electronic-webchat

sudo pacman -S yay base-devel
yay -S yaourt
yay -S netease-cloud-music
