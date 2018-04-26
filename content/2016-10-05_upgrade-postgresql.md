Title: Upgrade PostgreSQL
Date: 2016-10-05 08:24
Modified: 2017-03-27 17:25
Category: posts
Tags: Postgres
Slug: upgrade-postgresql
Authors: Jitse-Jan
Summary: By default Ubuntu 14.04 is running PostgreSQL version 9.3. In order to use the json datatype PostgreSQL version 9.4 or bigger is needed. The versions can be installed side by side, but for clarity you could remove the 
older/wrong versions.

First check which PostgreSQL is running
``` shell
jitsejan@jjsvps:~$ sudo service postgresql status
```
Probably this will list version 9.3 running on port 5432.

Add the PostgreSQL repository to the sources to be able to update to newer versions.
``` shell
jitsejan@jjsvps:~$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
jitsejan@jjsvps:~$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
Now update the system to retrieve data from the new repository.
``` shell
jitsejan@jjsvps:~$ sudo apt-get update
jitsejan@jjsvps:~$ sudo apt-get upgrade
```

Next we can install version 9.4 of PostgreSQL.
``` shell
jitsejan@jjsvps:~$ sudo apt-get install postgresql-9.4
```

If you check the status again, you will see two instances of PostgreSQL running.
``` shell
jitsejan@jjsvps:~$ sudo service postgresql status
```

Optionally the old version can be removed.
``` shell
jitsejan@jjsvps:~$ sudo apt-get remove --purge postgresql-9.3
```