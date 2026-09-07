#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pelican_jupyter import markup as nb_markup
import os

AUTHOR = u'Jitse-Jan'
SITENAME = u"JJ's World"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
THEME = 'themes/middle-theme'
PLUGIN_PATHS = ['plugins']
PLUGINS = ["tipue_search", "tag_cloud", nb_markup]

DELETE_OUTPUT_DIRECTORY = False
EXTRA_HEADER = open('_nb_header.html').read() if os.path.exists('_nb_header.html') else None
NOTEBOOK_DIR = 'notebooks'
LOAD_CONTENT_CACHE = False

DISPLAY_PAGES_ON_MENU = True
TWITTER_USERNAME = 'jitsejan'
GITHUB_USERNAME = 'jitsejan'

TYPOGRIFY = False
PAGE_PATHS = ['pages']
PAGES = [
    {'url': 'pages/pandas-cheatsheet', 'title': 'Pandas cheatsheet'},
	{'url': 'pages/python-cheatsheet', 'title': 'Python cheatsheet'},
	{'url': 'pages/spark-cheatsheet', 'title': 'Spark cheatsheet'},
]

ABOUT = """<p>I'm Jitse-Jan, a data lead based in London working across data platforms, orchestration, and analytics engineering: dbt, Dagster, Snowflake, dlt, and DuckDB, with Python underneath most of it.</p>
<p>
Lately that also means working AI-assisted day to day, using Claude alongside a structured note-taking setup to keep multiple projects straight.
</p>
<p>
This blog goes back to 2016. There's a real gap in the middle, a long stretch of heads-down client work rather than writing, but the interest never stopped, and the more recent posts pick up where the site left off.
</p>
<p>
I use this page as a portfolio, cheatsheet, and historical record. Expect shell commands, working examples, and write-ups of things I built, mostly so I don't have to reinvent the wheel next time.
</p>
"""
ABOUT_IMG = "/theme/images/github_avatar.png"

GOOGLE_ANALYTICS_CODE = 'UA-86650752-1'
GOOGLE_ANALYTICS_DOMAIN = 'www.jitsejan.com'

TAG_CLOUD_STEPS = 6 	        # Count of different font sizes in the tag cloud.
TAG_CLOUD_MAX_ITEMS = 18 	    # Maximum number of tags in the cloud.
TAG_CLOUD_SORTING = 'size-rev' 	# The tag cloud ordering scheme. Valid values: random, alphabetically, alphabetically-rev, size and size-rev
TAG_CLOUD_BADGE = False	        # Optional setting : can bring badges, which mean say : display the number of each tags present on all articles.' 

TIPUE_SEARCH = True
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))

MARKUP = ("md", "ipynb")
IGNORE_FILES = [".ipynb_checkpoints"]