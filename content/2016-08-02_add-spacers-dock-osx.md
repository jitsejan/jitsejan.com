Title: Add spacers in your OSX dock
Date: 2016-08-02 13:54
Modified: 2017-03-27 14:46
Category: posts
Tags: shell, mac, osx, dock
Slug: add-spacers-dock-osx
Authors: Jitse-Jan
Summary:

Run this command in the terminal to add a spacer
``` shell
jitsejan@MBP $ defaults write com.apple.dock persistent-apps -array-add '{tile-data={}; tile-type="spacer-tile";}'
```
and restart the dock by running
``` shell
jitsejan@MBP $ killall Dock
```
