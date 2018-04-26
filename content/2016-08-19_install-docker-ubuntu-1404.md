Title: Install Docker on Ubuntu 14.04
Date: 2016-08-19 20:05
Modified: 2017-03-27 16:56
Category: posts
Tags: digitalocean, Ubuntu, Docker
Slug: install-docker-ubuntu-1404
Authors: Jitse-Jan
Summary: These are the steps needed to get Docker working on Ubuntu 14.04. I have tested these steps on a Digital Ocean droplet.

First update the system.
``` shell
$ sudo apt-get update
$ sudo apt-get -y upgrade
```
Add the recommended package for the current kernel.
``` shell
$ sudo apt-get install linux-image-extra-$(uname -r)
```
Add the official key for Docker.
``` shell
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```
Add the source to the sources.list.d and refresh the packages.
``` shell
$ echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
$ sudo apt-get update
```
Now you can install Docker.
``` shell
$ sudo apt-get install docker-engine
```
Change the following in /etc/default/ufw:
``` shell
DEFAULT_APPLICATION_POLICY="DROP" 
```
becomes
``` shell
DEFAULT_APPLICATION_POLICY="ACCEPT" 
```
Restart the firewall.
``` shell
$ sudo ufw reload
```
Create a Docker group and your current user to it to be able to connect to the Docker daemon.
``` shell
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```
Login again to start using Docker. Now check if Docker is working.
``` shell
$ sudo service docker start
$ sudo docker run hello-world
```
Hopefully this last step will download the image and run the container. If you are happy with the result, make it start automatically on system start.
``` shell
$ sudo systemctl enable docker
```


