Title: Using Supervisor to start Gunicorn
Date: 2016-10-04 14:06
Modified: 2017-03-27 17:25
Category: posts
Tags: Ubuntu, Supervisor, gunicorn
Slug: using-supervisor-start-gunicorn
Authors: Jitse-Jan
Summary: To avoid running the Gunicorn in a separate screen, you can use Supervisor to automatically start the Gunicorn server on system start or on user demand.

Install Supervisor.
``` shell
jitsejan@jjsvps:~$ sudo pip install supervisor
```

Create the default configuration file for Supervisor.
``` shell
jitsejan@jjsvps:~$ sudo echo_supervisord_conf > /etc/supervisord.conf
```

Create the configuration file for the website.
``` shell
jitsejan@jjsvps:~$ sudo nano /etc/supervisor/conf.d/website.conf
```
Enter the following.
```
; /etc/supervisor/conf.d/website.conf
[program:website]
command=gunicorn -c /opt/env/gunicorn_config.py django_project.wsgi:application
directory=/opt/env/django_project/
user=jitsejan
autostart=True
autorestart=True
redirect_stderr=True
```

Make the file executable.
``` shell
jitsejan@jjsvps:~$ sudo chmod a+x /etc/supervisor/conf.d/website.conf 
```

Reload Supervisor to find the new file and update the configuration.
``` shell
jitsejan@jjsvps:~$ sudo supervisorctl reread
jitsejan@jjsvps:~$ sudo supervisorctl update
```

Now you can start the website with the following command.
``` shell
jitsejan@jjsvps:~$ sudo supervisorctl start website
```