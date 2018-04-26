Title: Mount Amazon EC as local folder
Date: 2016-07-29 19:07
Modified: 2017-03-27 14:27
Category: posts
Tags: shell
Slug: mount-amazon-ec-local-folder
Authors: Jitse-Jan
Summary:

``` shell
jitsejan@MBP $ sshfs ubuntu@ec2-34-56-7-89.eu-central-1.compute.amazonaws.com:/home/ubuntu/ ~/AmazonEC2/ -oauto_cache,reconnect,defer_permissions,noappledouble,negative_vncache
```