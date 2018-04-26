Title: Add CSS to Splunk dashboard
Date: 2016-12-17 14:18
Modified: 2017-03-27 17:59
Category: posts
Tags: Splunk, tutorial, dashboard, CSS
Slug: add-css-splunk-dashboard
Authors: Jitse-Jan
Summary: To add some custom style to your dashboard, you can create a cascade stylesheet in your app folder and overrule the standard dashboard lay-out.

The file should be located in 
```
%SPLUNK_HOME%/etc/apps/<APPNAME>/appserver/static/
```

If the file is called _dashboard.css_, the file will be automatically applied to all dashboards within this application. If you give it a custom name, you need to include it explicitly in the stylesheet attribute in the XML of your dashboard like the following

```
<form stylesheet="mycustomstyle.css">
```

Currently the base of my _dashboard.css_ looks like the stylesheet of this webpage, to make it clear that I am in my own application.

``` css
@import url('https://fonts.googleapis.com/css?family=Raleway');
body, html{
	background-color: white;
	font-family: "Raleway";
	height: 100%;
}
header{
    background-color: rgb(102,153,255);
    border: 0px;
    background-image: url('./images/Bar.GIF');
    background-repeat: repeat-x;
    background-position: bottom;
    padding: 0px 0px 16px 0px;
}
.dashboard-body{
	background-color: white;
	height: 100%;
}
.dashboard{
	background-color: white;
}
footer{
    margin-top: 0px;
    padding-bottom: 50px;
    font-size: small;
    color: rgb(200, 200, 200);
    background-image: url('./images/Bottom.GIF');
    background-repeat: repeat-x;
    background-position: bottom;
}
h1, h2, a{
    color: rgb(102, 153, 255);
}
```

Note that when a new stylesheet is added, Splunkweb needs a restart. If you simply update the stylesheet, run the following command:
``` 
http://SPLUNKHOST/en-US/_bump
```