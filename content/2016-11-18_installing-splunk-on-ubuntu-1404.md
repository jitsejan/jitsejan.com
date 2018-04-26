Title: Installing Splunk on Ubuntu 14.04
Date: 2016-11-17 11:47
Modified: 2017-03-27 17:48
Category: posts
Tags: Splunk, Ubuntu
Slug: installing-splunk-on-ubuntu-1404
Authors: Jitse-Jan
Summary: Explanation of the installation of Splunk.

Download the latest version of [Splunk Light](https://www.splunk.com/en_us/products/splunk-light.html) (Currently version 6.5) to your download folder.
``` shell
jitsejan@jjsvps:~/Downloads$ wget -O splunklight-6.5.0-59c8927def0f-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=6.5.0&product=splunk_light&filename=splunklight-6.5.0-59c8927def0f-Linux-x86_64.tgz&wget=true'
```
Extract the archive to the __/opt/__ folder.
``` shell
jitsejan@jjsvps:~/Downloads$ sudo tar zvzf splunklight-6.5.0-59c8927def0f-Linux-x86_64.tgz -C /opt/
```
Export the folder where Splunk is installed to your environment.
``` shell
jitsejan@jjsvps:/opt/splunk$ echo 'export SPLUNK_HOME=/opt/splunk/' >> ~/.bashrc 
jitsejan@jjsvps:/opt/splunk$ source ~/.bashrc
```
Make sure the rights of the __/opt/splunk/__ folder are correctly set. 
``` shell
jitsejan@jjsvps:/opt$ sudo chown -R jitsejan:root splunk/ 
```

Enable access to the Splunk web interface by adding a subdomain that links to the right port.                                                                                   
``` shell
jitsejan@jjsvps:/etc/nginx/sites-available$ sudo nano splunk
```
Add the following to the configuration file. Change the subdomain and port to the right values for you. 
``` 
server {
    listen 80;
    server_name subdomain.jitsejan.com;

    location / {
        proxy_pass http://localhost:8888;
    }
}
```
Enable the subdomain by creating a system link.
``` shell
jitsejan@jjsvps:/etc/nginx/sites-available$ sudo ln -s /etc/nginx/sites-available/splunk /etc/nginx/sites-enabled/
```
And finally restart the server.
``` shell
jitsejan@jjsvps:/etc/nginx/sites-available$ sudo service nginx restart
```

Now you can open up the browser and go the the subdomain that you just introduced.