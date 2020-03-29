Title: Using Powerlevel10K as Zsh theme
Date: 2020-03-29 04:18
Modified: 2020-03-29 04:18
Category: posts
Tags: zshell, command line, iterm2, styling
Slug: using-powerlevel10k-as-zsh-theme
Authors: Jitse-Jan
Summary: 

Previously I was using [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k) as theme for my [iTerm2](https://iterm2.com) Zsh configuration. Recently I had to install a new MacBook and found an easier way to make the terminal look fancier. [powerlevel10k](https://github.com/romkatv/powerlevel10k) is the better version of `powerlevel9k`, especially since it has a configuration prompt where the installer guides you through all the changes you can make to the style.

For Mac it is as simple as the following few lines, assuming you have [brew](https://brew.sh) installed.

```sh
$ brew install romkatv/powerlevel10k/powerlevel10k
$ echo 'source /usr/local/opt/powerlevel10k/powerlevel10k.zsh-theme' >>! ~/.zshrc
$ p10k configure
```