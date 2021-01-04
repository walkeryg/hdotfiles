#!/bin/bash

chsh -s /bin/zsh
if [ -d ~/.oh-my-zsh ]; then
  echo "oh my zsh already exist";
else
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
  git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
  # git clone https://github.com/lukechilds/zsh-nvm ~/.oh-my-zsh/custom/plugins/zsh-nvm
  git clone https://github.com/trapd00r/zsh-syntax-highlighting-filetypes.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting-filetypes
  cp ~/.oh-my-zsh/templates/zshrc.zsh-template zshrc
  dircolors LS_COLORS >> zshrc

  sed -i 's/plugins=.*/plugins=(git colorize zsh-syntax-highlighting-filetypes zsh-syntax-highlighting zsh-autosuggestions)/g'

  cat custom_cmd_alias >> zshrc
  my zshrc ~/.zshrc
  # plugins=( git zsh-syntax-highlighting zsh-autosuggestions autojump zsh-nvm )
  # ZSH_THEME="agnoster"
  # export NVM_LAZY_LOAD=true
fi

