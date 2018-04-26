Title: Send attachment from command line
Date: 2016-07-29 19:09
Modified: 2017-03-27 14:31
Category: posts
Tags: shell
Slug: send-attachment-from-command-line
Authors: Jitse-Jan
Summary:

``` shell
$ echo 'Mail with attachment' | mutt -a "/file/to/add/" -s "FYI: See attachment" -- name@email.com
```