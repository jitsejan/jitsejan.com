Title: Moving my blog to Github Pages
Date: 2018-04-26 12:00
Modified: 2018-04-27 16:56
Category: posts
Tags: infra, static, hosting
Slug: moving-blog-to-github-pages
Authors: Jitse-Jan
Summary: A short description how I managed to move my blog from my VPS to Github pages with SSL served via CloudFlare.

Since I am evaluating the use of the different servers that I own, I am trying to move things away from the servers to _free_ tools or platforms. For example, you can host notebooks on [Azure](http://notebooks.azure.com) for free and Github supports the hosting of static websites on [Github pages](https://pages.github.com/). Ideally I would like to remove two of the three servers that I own to both reduce costs and improve my knowledge of the different available platforms. Below I describe the steps I took to move my website to the new location. 

## Creating the Github page

### Create two repositories
[https://github.com/new](https://github.com/new)

* [jitsejan/pelican-source](https://github.com/jitsejan/jitsejan.github.io-source) (This repository contains source for the Pelican blog for my homepage)
* [jitsejan/jitsejan.github.io](https://github.com/jitsejan/jitsejan.github.io) (This repository contains the Pelican blog for my homepage)

### Set up the Pelican blog
Copy the source repository to the machine:

```bash
jitsejan@dev16:~/code$ git clone https://github.com/jitsejan/jitsejan.github.io-source.git
Cloning into 'jitsejan.github.io-source'...
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
Checking connectivity... done.
```

Verify the repository is correct:

```bash
jitsejan@dev16:~/code$ cd jitsejan.github.io-source/
jitsejan@dev16:~/code/jitsejan.github.io-source$ git remote -v
origin  https://github.com/jitsejan/jitsejan.github.io-source.git (fetch)
origin  https://github.com/jitsejan/jitsejan.github.io-source.git (push)
```

Add the output repository as a submodule to the source repo:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ git submodule add  https://github.com/jitsejan/jitsejan.github.io.git output
Cloning into 'output'...
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
Checking connectivity... done.
```

Create the Pelican application using the quickstart tool:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ pelican-quickstart 
Welcome to pelican-quickstart v3.6.3.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.

    
> Where do you want to create your new web site? [.] 
> What will be the title of this web site? JJs World
> Who will be the author of this web site? Jitse-Jan
> What will be the default language of this web site? [en] 
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) 
> What is your URL prefix? (see above example; no trailing slash) https://jitsejan.github.io
> Do you want to enable article pagination? (Y/n) 
> How many articles per page do you want? [10] 
> What is your time zone? [Europe/Paris] Europe/London
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) 
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) 
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) Y
> Is this your personal page (username.github.io)? (y/N) Y
Error: [Errno 17] File exists: '/home/jitsejan/code/jitsejan.github.io-source/output'
Done. Your new project is available at /home/jitsejan/code/jitsejan.github.io-source
```

Change the `publishconf.py` to not delete the output directory:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://jitsejan.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
```

Create the first post:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ cat content/first-post.md 
Title: My first post
Date: 2018-04-26 13:00
Modified: 2018-04-26 13:00
Tags: fipo
Category: dummy-data
Slug: my-first-post
Authors: Jitse-Jan
Summary: The first post of the Pelican blog on Github pages.

I am migrating my website from my VPS to Github pages as an experiment.
```

Build the website and serve its contents:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ make html && make serve
pelican /home/jitsejan/code/pelican-source/content -o /home/jitsejan/code/pelican-source/output -s /home/jitsejan/code/pelican-source/pelicanconf.py 
WARNING: No valid files found in content.
Done: Processed 0 articles, 0 drafts, 0 pages and 0 hidden pages in 0.07 seconds.
cd /home/jitsejan/code/pelican-source/output && python -m pelican.server
```

Generate the static content for the website:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ make publish
pelican /home/jitsejan/code/pelican-source/content -o /home/jitsejan/code/pelican-source/output -s /home/jitsejan/code/pelican-source/publishconf.py 
Done: Processed 1 article, 0 drafts, 0 pages and 0 hidden pages in 0.14 seconds.
```

Push the output code to the `pelican-html` repository:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ cd output/
jitsejan@dev16:~/code/jitsejan.github.io-source/output$ git add .
jitsejan@dev16:~/code/jitsejan.github.io-source/output$ git commit -m 'My first post'
jitsejan@dev16:~/code/jitsejan.github.io-source/output$ git push -u origin master
```

Push the source code to the `pelican-source` repository:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source/output$ cd ..
jitsejan@dev16:~/code/jitsejan.github.io-source$ echo '*.pyc' >> .gitignore
jitsejan@dev16:~/code/jitsejan.github.io-source$ git add .
jitsejan@dev16:~/code/jitsejan.github.io-source$ git commit -m 'My first commit'
jitsejan@dev16:~/code/jitsejan.github.io-source$ git push -u origin master
```

Now the homepage is ready on [https://jitsejan.github.io/](https://jitsejan.github.io/)!

[Inspiration link](https://fedoramagazine.org/make-github-pages-blog-with-pelican/)

## Merge the original Pelican blog

### Copy the data

Clone the old repository and overwrite the contents of the Github pages repo:

```bash
jitsejan@dev16:~/code$ git clone https://github.com/jitsejan/pelican-blog
jitsejan@dev16:~/code$ rm -rf jitsejan.github.io-source/content/
jitsejan@dev16:~/code$ rm -rf ../jitsejan.github.io-source/themes/
jitsejan@dev16:~/code$ mv pelican-blog/* jitsejan.github.io-source
```

Additionally the `DELETE_OUTPUT_DIRECTORY` had to be set to `False` again in `publishconf.py`.

### Issues
Some Python libraries were missing and the `pip install` had to be done first:

```bash
jitsejan@dev16:~/code/jitsejan.github.io-source$ pip install -r requirements.txt 
```

The `less` compiler was missing:

```bash
jitsejan@dev16:~/code$ sudo npm install -g less
```

I had to remove the ipynb plugin and reinstall it by adding it again as a submodule:

```bash
git submodule add git://github.com/danielfrg/pelican-ipynb.git plugins/ipynb
```

## Final steps
To make the Github URL work with my own domain, I had to follow several steps:

1. Add the custom domain name (`www.jitsejan.com`) to the Github Page repository in a file `CNAME` in the root (or via the Settings tab)
2. Update the DNS record for my DreamHost account and modify the two primary nameservers to point to [Cloudflare](https://www.cloudflare.com) and remove the additional ones. (Nameserver 1: janet.ns.cloudflare.com, Nameserver 2: marty.ns.cloudflare.com)
3. Add DNS records in Cloudflare. One CNAME for `www` and one CNAME for `jitsejan.com` to point to `jitsejan.github.io`.

