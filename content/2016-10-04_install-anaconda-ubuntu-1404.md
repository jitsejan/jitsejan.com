Title: Install Anaconda on Ubuntu 14.04
Date: 2016-10-04 10:29
Modified: 2017-03-27 17:06
Category: posts
Tags: Anaconda, Python, Ubuntu
Slug: install-anaconda-ubuntu-1404
Authors: Jitse-Jan
Summary: Installation of Anaconda on Ubuntu 14.04.

Retrieve the last Anaconda version for your system (32 or 64 bit).
``` shell
jitsejan@jjsvps:~$ cd Downloads/
jitsejan@jjsvps:~/Downloads$ wget https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh
```

Run the installer.
``` shell
jitsejan@jjsvps:~/Downloads$ bash Anaconda2-4.1.1-Linux-x86_64.sh 
```

Update the terminal to include the Anaconda references.
``` shell
jitsejan@jjsvps:~/Downloads$ source ~/.bashrc
```

Test if iPython is working now.
``` shell
jitsejan@jjsvps:~$ ipython -v
```

All set.
