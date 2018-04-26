Title: Find most used history command
Date: 2016-07-27 16:55
Modified: 2017-03-26 16:56
Category: posts
Tags: shell
Slug: most-used-history-command
Authors: Jitse-Jan
Summary:

``` shell
$ awk '{print $1}' ~/.bash_history | sort | uniq -c | sort -n
```