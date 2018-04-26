Title: Simple webcrawling in Python
Date: 2016-07-28 12:45
Modified: 2017-03-26 18:26
Category: posts
Tags: python, webcrawl, lxml
Slug: simple-webcrawling-python
Authors: Jitse-Jan
Summary: Simple webcrawling in Python

```python
""" samples/crawl_01.py """
################################################################################
# Application:      WebParser example 01
# File:             samples/crawl_01.py
# Goal:
# Input:
# Output:
# Example:
#
# History:          2016-06-27 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
import lxml.html
import urllib2

################################################################################
# Definitions
################################################################################
HEADER = {'Accept-Language': 'nl-NL',
          'User-Agent': """Mozilla/5.0 (Windows; U;
                                    Windows NT 6.1;
                                    nl-NL;
                                    rv:1.9.1.5)
                       Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);
                       nl-NL"""}
################################################################################
# Classes
################################################################################
class WebParser(object):
    """ Definition of the WebParser """
    def __init__(self, *args, **kwargs):
        """ Initialize the WebParser """
        super(WebParser, self).__init__(*args, **kwargs)

    @staticmethod
    def parse_page(url):
        """ Open URL and return the element tree of the page """
        req = urllib2.Request(url, headers=HEADER)
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
        return tree

    @staticmethod
    def find_css_element(etree, element):
        """ Find an element in the element tree and return it """
        return etree.cssselect(element)

################################################################################
# Functions
################################################################################
def main():
    """ Main function """
    parser = WebParser()
    etree = parser.parse_page('http://isitweekendyet.com/')
    divs = parser.find_css_element(etree, 'div')
    print divs[0].text.strip()

################################################################################
# main
################################################################################
if __name__ == "__main__":
    main()
```