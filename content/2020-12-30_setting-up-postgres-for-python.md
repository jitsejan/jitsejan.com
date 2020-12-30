Title: Setting up PostgreSQL for Python
Date: 2020-12-30 16:55
Modified: 2020-12-30 16:55
Category: posts
Tags: Python, postgres, PostgreSQL, SQLAlchemy, Ubuntu
Slug: setting-up-postgres-for-python
Authors: Jitse-Jan
Summary: This tutorial describes how to set up PostgreSQL on Ubuntu and configure it to make it connect with Python. 

## Objective

- Setup PostgreSQL on Ubuntu
- Setup Python to connect to PostgreSQL

## VPS information

### Setup PostgreSQL

For this tutorial I will be installing PostgreSQL on my VPS running `Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-58-generic x86_64)`.

## Ubuntu Packages

Install the following packages to get PostgreSQL and Python running. I assume Python is already installed on the machine.

- `postgresql`
- `postgresql-client`
- `postgresql-client-common`
- `libpq-dev`

```bash
jitsejan@theviji:~$ sudo apt install postgresql \\
                                     postgresql-client \\
                                     postgresql-client-common \\
                                     libpq-dev
```

## Verify PostgreSQL

The PostgreSQL server version can be verified with the `locate` tool which returns version `12`:

```bash
jitsejan@theviji:~$ locate bin/postgres
/usr/lib/postgresql/12/bin/postgres
```

The PostgreSQL client version can simply be checked using `psql` and in this case is `12.5`:

```bash
jitsejan@theviji:~$ psql -V
psql (PostgreSQL) 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
```

## Create new user

After installing PostgreSQL I add a new user for the project I will be working on. First login with the default `postgres` user and use `createuser --interactive` to add a user. In my case I will do a project around Zelda and therefor create a new user `zelda`.

```bash
jitsejan@theviji:~$ sudo -i -u postgres
[sudo] password for jitsejan:
postgres@theviji:~$ createuser --interactive
Enter name of role to add: zelda
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n
```

Default the user doesn't have a password set which means we have to login to the `psql` shell and add a password for the new user:

```bash
postgres@theviji:~$ psql
psql (12.5 (Ubuntu 12.5-0ubuntu0.20.04.1))
Type "help" for help.

postgres=# \password zelda
Enter new password:
Enter it again:
```

Since we are already here lets also add a database with the same name as the user.

```bash
postgres=# create database zelda;
CREATE DATABASE
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 zelda     | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
(4 rows)
```

Additionally to adding the user to PostgreSQL I also add the user to the system.

```bash
jitsejan@theviji:~$ sudo adduser zelda
Adding user `zelda' ...
Adding new group `zelda' (1001) ...
Adding new user `zelda' (1001) with group `zelda' ...
Creating home directory `/home/zelda' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for zelda
Enter the new value, or press ENTER for the default
        Full Name []: Zelda
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
```

Now I can switch to the newly created user and start the PostgreSQL shell. The connection information shows that we are indeed connected to the new `zelda` database by default.

```bash
jitsejan@theviji:~$ sudo -i -u zelda
zelda@theviji:~$ psql
zelda=> \conninfo
You are connected to database "zelda" as user "zelda" via socket in "/var/run/postgresql" at port "5432".
```

## Configure PostgreSQL for Python

The important part to get PostgreSQL working with Python remotely is to make sure PostgreSQL allows external IPs. Modify the `postgresql.conf` that should be located in `/etc/postgresql/12/main`.

Open the file as `sudo` with a text editor:

```bash
jitsejan@theviji:~$ sudo nano /etc/postgresql/12/main/postgresql.conf
```

And change the `listen_addresses` to `'*'` to make PostgreSQL listen to all IPs.

```bash
listen_addresses = '*'                  # what IP address(es) to listen on;
```

Furthermore, update the `pg_hba.conf` to allow a connection from any IP. The file should be located in the same folder as the `postgresql.conf`.

```bash
jitsejan@theviji:~$ sudo nano /etc/postgresql/12/main/pg_hba.conf
```

Add this to that the bottom of the table at the bottom of the file:

```bash
host    all             all             0.0.0.0/0               md5
host    all             all             ::/0                    md5
```

Restart `postgreqsl` to apply the changes:

```bash
jitsejan@theviji:~$ /etc/init.d/postgresql restart
```

In case of errors we can look at the log files located in `/var/log`. Use `sudo tail <logfile>` to check the last lines in the log file.

```bash
 jitsejan@theviji:~$ sudo tail /var/log/postgresql/postgresql-12-main.log
```

## Connect to PostgreSQL with Python

At this point we have a running PostgreSQL server which allows external traffic. We have a dedicated user with a password that we can use to connect to the server. The Python version I will be using is `3.8.5`.

```python
jitsejan@theviji:~$ python3 --version
Python 3.8.5
```

### Install packages

Install `SQLAlchemy` and the `psycopg2` library. [SQLAlchemy]([]()) is an ORM which abstracts the specific PostgreSQL code for the project. If at some point you were to switch databases you could simply update the connection but leave all the database definitions the same.

```bash
pip3 install psycopg2 sqlalchemy
```

### Create database engine

For safety I have added my secrets as environment variables. Update the `~/.bashrc` or `~/.zshrc` and add the necessary exports.

```python
# ~/.bashrc
export POSTGRES_USER=zelda
export POSTGRES_DB=zelda
export POSTGRES_PASS=SomePass
export POSTGRES_PORT=1234
export POSTGRES_HOST=dev.jitsejan.com
```

Make sure to reload the configuration file with `source ~/.bashrc`. Now that the variables are exported we can use them in the following Python script to setup the database engine.

```python
import os
import sqlalchemy
from sqlalchemy import create_engine

USER = os.environ['POSTGRES_USER']
PASS = os.environ['POSTGRES_PASS']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
DB = os.environ['POSTGRES_DB']
db_string = f"postgres://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

engine = create_engine(db_string)
```

### Add a table

For the first project I will crawl items from a website with only two fields for simplicity. The table `items` contains two columns:

- name (string)
- price (integer)

```python
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

items = Table(
   'items', meta, 
   Column('name', String, primary_key = True), 
   Column('price', Integer), 
)
meta.create_all(engine)
```

Verify the table has been created by calling the `table_names` function on the `engine`.

```python
engine.table_names()
# ['items']
```

And that is it. PostgreSQL is up and running and we are able to interact with it using Python.
