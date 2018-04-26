Title: Check the listening ports on the server
Date: 2016-10-04 11:24
Modified: 2017-03-27 17:19
Category: posts
Tags: shell, network, netstat
Slug: check-listening-ports-on-server
Authors: Jitse-Jan
Summary: 

Use netstat to check with ports are listening on the machine.
``` shell
jitsejan@jjsvps:~$ netstat -lnt | awk '$6 == "LISTEN"'
```