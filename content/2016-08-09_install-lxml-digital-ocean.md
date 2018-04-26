Title: Install lxml for Python on DigitalOcean
Date: 2016-08-09 20:05
Modified: 2017-03-27 16:10
Category: posts
Tags: digitalocean, lxml, Python, swapfile
Slug: install-lxml-digital-ocean
Authors: Jitse-Jan
Summary: Installing LXML on a DigitalOcean droplet is tricky because of the small amount of memory.

Currently I am using a DigitalOcean droplet with 512 MB to run this website. I ran into an issue when I was trying to install lxml. First make sure the correct libraries are installed before lxml is installed. 
``` bash
$ sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
```
Next, be aware that the 512 MB is not enough memory to compile the lxml package with Cython when you use pip to install, which means some additional steps are needed. To virtually increase your work memory, you could use a swapfile. Create a swapfile with these commands:

``` bash
$ sudo dd if=/dev/zero of=/swapfile1 bs=1024 count=524288
$ sudo mkswap /swapfile1
$ sudo chown root:root /swapfile1
$ sudo chmod 0600 /swapfile1
```
Now you can use pip to install the lxml Python module
``` bash
$ sudo pip install lxml
```
And of course you need to clean up after installation is done.
``` bash
$ sudo swapoff -v /swapfile1
$ sudo rm /swapfile1
```