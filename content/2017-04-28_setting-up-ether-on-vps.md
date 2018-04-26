Title: Setting up Ether on my VPS
Date: 2017-04-28 18:34
Modified: 2017-04-28 18:34
Category: posts
Tags: vps, ether, ethereum, Linux, geth, blockchain
Slug: setting-up-ether-on-vps
Authors: Jitse-Jan
Summary: My first step in getting to know the Ether platform is installing it on one of my Linux machines.

Installation steps:
``` shell
jitsejan@jjschi2:~$ sudo apt-get install software-properties-common
jitsejan@jjschi2:~$ sudo add-apt-repository -y ppa:ethereum/ethereum
jitsejan@jjschi2:~$ sudo apt-get update
jitsejan@jjschi2:~$ sudo apt-get install ethereum
```
Get a new account with:
``` shell
jitsejan@jjschi2:~$ geth account new
jitsejan@jjschi2:~$ geth account list
```

Start a screen and start mining:
``` shell
jitsejan@jjschi2:~$ geth --mine
```

To connect to this session and check your balance:
``` shell
jitsejan@jjschi2:~$ geth attach
jitsejan@jjschi2:~$ > eth.getBalance(eth.accounts[0])
```

I am not sure if my slow VPS will ever successfully mine any Ether, but since I want to know the basics of Ether, this is a good starting point.