Title: Python cheatsheet
Date: 2017-03-26 16:48
Modified: 2017-03-26 16:48
Category: python
Tags: python, cheatsheet
Slug: python-cheatsheet
Authors: Jitse-Jan
Summary: This is my Python cheatsheet

This is my [Python](https://www.python.org/) cheatsheet

### Pretty print a dictionary
``` python
print json.dumps(characters[:1], indent=4)
```

### Find index of item in dictionary
``` python
index = next(index for (index, d) in enumerate(characters) if d["name"] == 'Mario')
```
## Databases
### Retrieve from Postgresql
``` python
import psycopg2
connnection = psycopg2.connect(database="character_db",
                               user="character_user",
                               password="character1234",
                               host="localhost",
                               port='5433')
cursor = connnection.cursor()
cursor.execute("SELECT * FROM \"characters\"")
characters = cursor.fetchall()
```

### Dictionary to CSV
``` python
import csv
def write_dictionary_to_csv(o_file, d):
    """ Write dictionary to output file """
    with open(o_file, 'wb') as csvfile:
        outputwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        outputwriter.writerow(d.keys())
        outputwriter.writerows(zip(*d.values()))

output_file = 'output.csv'
write_dictionary_to_csv(output_file, data)
```

## Web crawling
### Use urllib2 to retrieve page content
``` python
import urllib2
req = urllib2.Request('http://www.mariowiki.com')
data = urllib2.urlopen(req).read()
```

### Set header for urllib2
``` python
import urllib2
# Header to request a page with NL as country
HEADER = {'Accept-Language': 'nl-NL',
       'User-Agent': """Mozilla/5.0 (Windows; U;
                                    Windows NT 6.1;
                                    nl-NL;
                                    rv:1.9.1.5)
                       Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);
                       nl-NL"""}
req = urllib2.Request('http://www.mariowiki.com', headers=HEADER)
data = urllib2.urlopen(req).read()
```
### Use requests to retrieve page content
``` python
import requests
resp = requests.get('http://www.mariowiki.com')
data = resp.content
```
### Use Selenium to retrieve page content
``` python
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://www.mariowiki.com')
data = browser.page_source
browser.quit()
```
### Scroll down in Selenium
``` python
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```
### Find an element and click in Selenium
By CSS selector:
``` python
browser.find_element_by_css_selector('#clickme').click()
```
By attribute:
``` python
browser.find_element_by_xpath('//input[@title="Open page"]').click()
```
### Make a list of links with cssselect 
``` python
import lxml.html
tree = lxml.html.fromstring(data)
links = ['http://www.mariowiki.com'+link.get('href') for link in tree.cssselect('div[role*=\'navigation\'] a')]
```

### Switch between tabs with Selenium
``` python
browser.switch_to.window(window_name=browser.window_handles[1])
browser.quit()
browser.switch_to.window(window_name=browser.window_handles[0])
```

## Pickle
Use the pickle libary to save a variable to a file and load it again.
```python
import pickle
colors = ['blue', 'red']
pickle.dump( colors, open( "colors.p", "wb" ) )
saved_colors = pickle.load( open( "colors.p", "rb" ) )
saved_colors
```

## Filter
A simple trick to select columns from a dataframe:
```python
# Create the filter condition
condition = lambda col: col not in DESIRED_COLUMNS
# Filter the dataframe
filtered_df = df.drop(*filter(condition, df.columns))
```

## Use seaborn to create heatmap
```python
import seaborn as sns
sns.heatmap(df\
            .groupby(['field_a', 'field_b'])['amount']\
            .sum()\
            .to_frame()\
            .reset_index()\
            .pivot('field_a', 'field_b', 'amount'));
```
or 

```python
sdf = df\
        .groupby(['field_a', 'field_b'])['amount']\
        .sum()\
        .reset_index()
sns.heatmap(sdf.pivot('genre', 'country', 'view_hours'))
```