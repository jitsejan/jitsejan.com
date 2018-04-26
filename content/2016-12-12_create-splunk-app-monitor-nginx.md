Title: Create a Splunk app to monitor Nginx
Date: 2016-12-12 15:34
Modified: 2017-03-27 17:58
Category: posts
Tags: Splunk, tutorial, dashboard, Nginx
Slug: create-splunk-app-monitor-nginx
Authors: Jitse-Jan
Summary: In this short tutorial I will create a Splunk app to monitor the webserver. We will create the bare-bone app and we add a few panels to the dashboard.

Using the web interface of Splunk you can easily add a new app. This will create the following structure:
```
nginxwatcher/
|-- bin
|   `-- README
|-- default
|   |-- app.conf
|   |-- data
|   |   `-- ui
|   |       |-- nav
|   |       |   `-- default.xml
|   |       `-- views
|   |           `-- README
|   |-- props.conf
|-- local
|   `-- app.conf
`-- metadata
    |-- default.meta
    `-- local.meta
```
To the _nginxwatcher/default_ folder the files **indexes.conf** and **inputs.conf** should be added. 

The content of **indexes.conf** should be something like the following:
``` 
[nginxwatcher]
coldPath = $SPLUNK_DB\nginxwatcher\colddb
enableDataIntegrityControl = 0
enableTsidxReduction = 0
homePath = $SPLUNK_DB\nginxwatcher\db
maxTotalDataSizeMB = 512000
thawedPath = $SPLUNK_DB\nginxwatcher\thaweddb
```
The content of **inputs.conf** should indicate we are monitoring the Nginx logging folder:
```
[monitor:///var/log/nginx/*.log]
disabled = false
host = nginxwatcher
index = nginxwatcher
sourcetype = nginxwatcher_logs
```
The contens of **props.conf** looks like this:
```
[nginxwatcher_logs]
NO_BINARY_CHECK = true
TZ = UTC
category = Structured
pulldown_type = 1
KV_MODE = none
disabled = false
```
After restarting Splunk we can start using the new index of the Nginx app and query with:
``` 
index="nginxwatcher"
```
To retrieve the values of the log files, we can use regular expressions and follow the description on the [Nginx](http://nginx.org/en/docs/http/ngx_http_log_module.html) website. 
``` 
index="nginxwatcher" | rex field=_raw "^(?&lt;remote_addr&gt;\d+.\d+.\d+.\d+)\s-\s(?P&lt;remote_user&gt;.*?)\s\[(?&lt;localtime&gt;\d+\/\w+\/\d{4}:\d{2}:\d{2}:\d{2}\s\+\d+)\]\s+\"(?&lt;request&gt;.*?)\"\s(?&lt;status&gt;\d+)\s(?&lt;bytes_sent&gt;\d+.*?)\s\"(?&lt;http_refererer&gt;.*?)\"\s\"(?&lt;http_user_agent&gt;.*)\""
```
Obviously we do not want to do this every time and we extract the values using the **props.conf**. The file is changed to:
```
[nginxwatcher_logs]
NO_BINARY_CHECK = true
TZ = UTC
category = Structured
pulldown_type = 1
KV_MODE = none
disabled = false
EXTRACT-e1 = ^(?<remote_addr>\d+.\d+.\d+.\d+)\s-\s(?P<remote_user>.*?)\s\[(?<localtime>\d+\/\w+\/\d{4}:\d{2}:\d{2}:\d{2}\s\+\d+)\]\s+\"(?<request>.*?)\"\s(?<status>\d+)\s(?<bytes_sent>\d+.*?)\s\"(?<http_refererer>.*?)\"\s\"(?<http_user_agent>.*)\"
```
The following query will show a timechart for the status over time, grouped by 30 minutes.
``` 
index="nginxwatcher" 
| timechart count(status) span=30m by status
```
Top visitors:
```
index="nginxwatcher"
| top limit=20 remote_addr
```
Pages which produce the most errors:
```
index="nginxwatcher"
| search status >= 500 
| stats count(status) as cnt by request, status
| sort cnt desc
```
All these graphs can of course be added to a dashboard to keep a close watch on the webserver.