Title: Move Django database between servers
Date: 2016-10-04 10:05
Modified: 2017-03-27 17:04
Category: posts
Tags: Django, Python
Slug: move-django-between-servers
Authors: Jitse-Jan
Summary: 

Save the database on the old server.
``` shell
(oldenv)jitsejan@oldvps:/opt/oldenv/django_project$ sudo python manage.py dumpdata blog > blog.json
```

Load the data on the new server. Make sure the models for both blogs are identical.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo python manage.py loaddata blog.json
```
