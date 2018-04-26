Title: Install Django on Ubuntu 14.04 with virtualenv, Nginx, Gunicorn and postgres
Date: 2016-10-04 09:46
Modified: 2017-03-27 16:59
Category: posts
Tags: Ubuntu, Django, Nginx, Gunicorn, postgres, virtualenv
Slug: install-django-ubuntu-1404-virtualenv-nginx-gunicorn-and-postgres
Authors: Jitse-Jan
Summary: A description of the steps needed to get Django working on Ubuntu 14.04.

Update the system first.
``` shell
jitsejan@jjsvps:~$ sudo apt-get update
jitsejan@jjsvps:~$ sudo apt-get upgrade
```
Install the virtual environment for Python.
``` shell
jitsejan@jjsvps:~$ sudo apt-get install python-virtualenv
```
Create a new environment in a folder of your choice.
``` shell
jitsejan@jjsvps:~$ ls /opt
jitsejan@jjsvps:~$ sudo virtualenv /opt/env
jitsejan@jjsvps:~$ sudo chown jitsejan /opt/env/
```
Activate the environment.
``` shell
jitsejan@jjsvps:~$ source /opt/env/bin/activate
```
Install Django inside the environment.
``` shell
(env)jitsejan@jjsvps:~$ pip install django
(env)jitsejan@jjsvps:~$ deactivate env
```
Install Postgresql on the system.
``` shell
jitsejan@jjsvps:~$ sudo apt-get install libpq-dev python-dev
jitsejan@jjsvps:~$ sudo apt-get install postgresql postgresql-contrib
```
Install the Nginx webserver on the system.
``` shell
jitsejan@jjsvps:~$ sudo apt-get install nginx
```
Install Gunicorn in the environment.
``` shell
jitsejan@jjsvps:~$ source /opt/env/bin/activate
(env)jitsejan@jjsvps:~$ sudo pip install gunicorn
```

Create a database and a user for the project.
``` shell
jitsejan@jjsvps:~$ sudo -u postgres psql
postgres=# CREATE DATABASE django_db;
postgres=# CREATE USER django_user WITH PASSWORD 'django_pass';
postgres=# GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;
```

Create a new project in the environment.
``` shell
(env)jitsejan@jjsvps:/opt/env$ django-admin.py startproject django_project
```

Install the Psycopg2 so PostgreSQL can be used in the application.
``` shell
(env)jitsejan@jjsvps:~$ sudo pip install psycopg2
```

Add the database details to the settings.py
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ nano django_project/settings.py
```

Create the default entries for the application in the database,
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo python manage.py syncdb
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo python manage.py migrate
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo python manage.py makemigrations
```

Start the Django server.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo python manage.py runserver 0.0.0.0:8080
```

Now use Gunicorn to connect to the server.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ gunicorn --bind 0.0.0.0:8080 django_project.wsgi:application
```

Create a configuration file for Gunicorn.
``` shell
(env)jitsejan@jjsvps:/opt/env$ sudo nano gunicorn_config.py
``` 

Add the following to the configuration file.
```
command = '/opt/env/bin/gunicorn'
pythonpath = '/opt/env/django_project'
bind = '127.0.0.1:8088'
workers = 3
user = 'jitsejan'
```

Use the configuration file for starting Gunicorn.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ gunicorn -c /opt/env/gunicorn_config.py django_project/django_project.wsgi:application
```

Create a superuser for Django administration.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo ./manage.py createsuperuser
```

Add the STATIC_URL to the settings.py.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ nano django_project/settings.py
```
``` 
...
STATIC_URL = '/static/'
...
```
Now collect the static data
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ sudo ./manage.py collectstatic
```
Create a new site in Nginx for the Django project
``` shell
jitsejan@jjsvps:~$ sudo nano /etc/nginx/sites-available/django_project
```
Add the following. Change the IP address, the folder for the static files and make sure the port is the same as 
configured for Gunicorn before.
```
server {
    server_name 123.456.123.456, *.domain.com;

    access_log off;

    location /static/ {
        alias /opt/env/django_project/static/;
    }

    location / {
            proxy_pass http://127.0.0.1:8088;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
}
```

Enable the site by adding a link in the enabled sites.
``` shell
jitsejan@jjsvps:~$ sudo ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/
```

Stop Apache and start Nginx.
``` shell
jitsejan@jjsvps:~$ sudo service apache2 stop
jitsejan@jjsvps:~$ sudo service nginx start
```

Now run Gunicorn and visit the page in your browser.
``` shell
(env)jitsejan@jjsvps:/opt/env/django_project$ gunicorn -c /opt/env/gunicorn_config.py django_project/django_project.wsgi:application
```
Hopefully the default Django page is shown now.