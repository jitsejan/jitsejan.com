Title: Install KDiff3 on OSX
Date: 2016-11-17 12:27
Modified: 2017-03-27 17:41
Category: posts
Tags: kdiff3, mac, OSX, brew
Slug: install-kdiff3-on-osx
Authors: Jitse-Jan
Summary: 

Installing the diff/merge tool [KDiff3](http://kdiff3.sourceforge.net) is easy using the package manager [Homebrew](http://brew.s) extension [Cask](https://caskroom.github.io). The extension makes is possible to install (GUI) applications on the Mac without the dragging and dropping of the DMG-files.

``` shell
jitsejan@MBP $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
jitsejan@MBP $ brew tap caskroom/cask
jitsejan@MBP $ brew cask install kdiff3
```