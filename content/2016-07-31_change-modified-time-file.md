Title: Change the last modified time of a file 
Date: 2016-07-31 14:52
Modified: 2017-03-27 14:41
Category: posts
Tags: shell
Slug: change-modified-time-file
Authors: Jitse-Jan
Summary:

This script will change the last modified time of a file in the current directory to 4 days back.
``` shell
#!/bin/ksh 
numDays=4
diff=86400*$numDays
export diff
newDate=$(perl -e 'use POSIX; print strftime "%Y%m%d%H%M", localtime time-$ENV{diff};')
lastFile=$(ls -lt | egrep -v ^d | tail -1 | awk ' { print $9 } ')
touch -t $newDate $lastFile
```
