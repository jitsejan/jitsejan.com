#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
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
#PLUGINS = ['liquid_tags.literal', 'assets', "tag_cloud", 'tipue_search', 'ipynb.markup']
PLUGINS = [ 'assets', "tag_cloud", 'tipue_search']

DELETE_OUTPUT_DIRECTORY = False
EXTRA_HEADER = open('_nb_header.html').read() if os.path.exists('_nb_header.html') else None
NOTEBOOK_DIR = 'notebooks'
LOAD_CONTENT_CACHE = False

DISPLAY_PAGES_ON_MENU = True
# FACEBOOK_USERNAME = 'jitsejan'
FLICKR_USERNAME = 'jitsejan'
LINKEDIN_USERNAME = 'jitsejan'
SPOTIFY_USERNAME = 'jitsejan'
TWITTER_USERNAME = 'jitsejan'
BITBUCKET_USERNAME = 'jitsejan'
GITHUB_USERNAME = 'jitsejan'
BLOCKS_USERNAME = 'jitsejan'
DOCKER_USERNAME = 'jitsejan'

TYPOGRIFY = False
PAGE_PATHS = ['pages']
PAGES = [
    # {'url': 'pages/latex-cheatsheet', 'title': 'Latex cheatsheet'},
	{'url': 'pages/pandas-cheatsheet', 'title': 'Pandas cheatsheet'},
	{'url': 'pages/python-cheatsheet', 'title': 'Python cheatsheet'},
	{'url': 'pages/spark-cheatsheet', 'title': 'Spark cheatsheet'},
	# {'url': 'pages/splunk-cheatsheet', 'title': 'Splunk cheatsheet'},
		]

ABOUT = """<p>I am the Head Of Data at <a href="https://www.lendinvest.com">LendInvest</a> in London. I have a passion for the field of machine learning, pattern recognition, big data, blockchain and ubiquitous computing.</p>
<p>
While I mainly work in Python, I try to experiment with different languages and frameworks when I can. Lately I have been experimenting with Javascript a bit more, since both
for visualizations as for modern web applications it is the go-to language. 
</p>
<p>
I am using this page as a portfolio and showcase, but mainly as a cheatsheet. That is why you will mainly find shell commands, short scripts or notebooks just for myself to not reinvent the wheel.
</p>
"""
ABOUT_IMG = "/theme/images/JJ_Montreal.png"

GOOGLE_ANALYTICS_CODE = 'UA-86650752-1'
GOOGLE_ANALYTICS_DOMAIN = 'www.jitsejan.com'

TAG_CLOUD_STEPS = 6 	        # Count of different font sizes in the tag cloud.
TAG_CLOUD_MAX_ITEMS = 23 	    # Maximum number of tags in the cloud.
TAG_CLOUD_SORTING = 'random' 	# The tag cloud ordering scheme. Valid values: random, alphabetically, alphabetically-rev, size and size-rev
TAG_CLOUD_BADGE = False	        # Optional setting : can bring badges, which mean say : display the number of each tags present on all articles.' 

TIPUE_SEARCH = True
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))

MARKUP = ('md', 'ipynb')
