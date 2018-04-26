Title: Change PostgreSQL database encoding
Date: 2016-10-05 08:24
Modified: 2017-03-27 17:32
Category: posts
Tags: Postgres, Ubuntu
Slug: change-postgresql-database-encoding
Authors: Jitse-Jan
Summary: I ran into an issue where I couldn't save some JSON-data to the database because of a weird UTF8 character. Apparently my databases have the SQL ASCII encoding and not the necessary UTF8 encoding.

First login to the PostgreSQL shell.
``` shell
(env)jitsejan@jjsvps:/opt/canadalando_env/canadalando_django$ sudo -u postgres psql
```

Check the list of databases.
``` shell
postgres=# \l
```
Here I could see my database had the wrong encoding, instead of SQL_ASCII I want UTF8. 
I dropped the database so I can re-create it with the right encoding. Note that I did NOT make a back-up, since my database was still empty.

``` shell
postgres=# DROP DATABASE website_db;
```

In order to use UTF8 the template for the databases needs to be updated first.

Disable the template1.
``` shell
postgres=# UPDATE pg_database SET datistemplate = FALSE WHERE datname ='template1';                                                                                                                                                                                                                                 
```

Drop the database.
``` shell
postgres=# DROP DATABASE template1;
```

Now re-create it with the right encoding.
``` shell
postgres=# CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UNICODE';
```

Activate the template.
``` shell
postgres=# UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
```

Now we can re-create the database that we dropped earlier.
``` shell
postgres=# CREATE DATABASE website_db WITH ENCODING 'UNICODE';
```