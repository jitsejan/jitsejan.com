Title: Install Jira on Ubuntu 14.04
Date: 2016-10-04 07:09
Modified: 2017-03-27 16:57
Category: posts
Tags: Ubuntu, Jira
Slug: install-jira-ubuntu-1404
Authors: Jitse-Jan
Summary: These are the steps needed to get Jira working on Ubuntu 14.04.

Retrieve the last Jira binary from the website. Note that you should pick the right version, either x32 or x64.
``` shell
jitsejan@jjsvps:~/Downloads$ wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-7.2.1-x64.bin 
```
Make the binary executable.
``` shell
jitsejan@jjsvps:~/Downloads$ chmod a+x atlassian-jira-software-7.2.1-x64.bin 
```
Install the dependencies for Jira.
``` shell
jitsejan@jjsvps:~/Downloads$ sudo ​​apt-get install lsb-core​ default-jdk​ default-jre
```
Execute the binary as sudo.
``` shell
​jitsejan@jjsvps:~/Downloads$ ​$ sudo ./atlassian-jira-software-7.2.1-x64.bin
```
Start the Jira server.
``` shell
jitsejan@jjsvps:~/Downloads$ sudo sh /opt/atlassian/jira/bin/start-jira.sh
```
Create a Jira user and database.
``` shell
jitsejan@jjsvps:~$ sudo -u postgres psql
postgres=# CREATE DATABASE jira;
postgres=# CREATE USER jira_user WITH PASSWORD 'bla';
postgres=# GRANT ALL PRIVILEGES ON DATABASE jira TO jira_user;
```
Now go to port 8080 on your IP address and perform the set-up. After some configuration you will be able to use Jira for your projects.

### Update
It could be that the server does not start. Check if the permissions are right.
``` shell
jitsejan@jjsvps:~$ sudo chown -R jira:jira /var/atlassian/application-data/jira

```

