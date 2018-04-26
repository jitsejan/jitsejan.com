Title: Adding aliases to Windows
Date: 2016-12-05 10:27
Modified: 2017-03-27 17:56
Category: posts
Tags: Windows, alias
Slug: adding-aliases-windows
Authors: Jitse-Jan
Summary: Since I have been using Linux for a while, switching back to the Windows CLI has some challenges. Luckily you can add aliases to the command prompt with the following procedure.

Open the __Registry Editor__ and go to the following key

``` 
Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor
```

and add the key __AutoRun__ with the value of the file containing the aliases. In my case this is 
```
"%USERPROFILE%\alias.cmd"
```

Save the change to the registry and restart the command prompt. Currently my __alias.cmd__ contains the following:

```
:: Registry path:	Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor
:: Key: 			AutoRun
:: Value: 			"%USERPROFILE%\alias.cmd"
@echo off
DOSKEY alias="C:\Program Files (x86)\Notepad++\notepad++.exe" "%USERPROFILE%\alias.cmd"
DOSKEY ls=dir /B
DOSKEY proj1=cd "%USERPROFILE%\Documents\Projects\proj1"
```