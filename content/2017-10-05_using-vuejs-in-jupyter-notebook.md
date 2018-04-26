Title: Using Vue.js in a Jupyter notebook
Date: 2017-10-05 22:47
Modified: 2017-10-11 22:48
Category: posts
Tags: Jupyter, notebook, VueJS, JavaScript, frontend
Slug: using-vuejs-in-jupyter-notebook
Authors: Jitse-Jan
Summary: Another experiment: using the progressive JavaScript Framework [Vue.js](https://vuejs.org) in a Jupyter notebook. 

<style>
img.header{
  height: 10%;
  margin-top: 10px;
}
</style>
<div class="row">
  <div class="col-md-2 col-xs-2 col-sm-2 col-sm-offset-1 col-xs-offset-1 col-md-offset-1"><img class="img-responsive" src="http://www.canadastop100.com/national/images/ct2017_english.png"/></div>
  <div class="col-md-2 col-xs-2 col-sm-2"><img class="img-responsive" src="https://cdn4.iconfinder.com/data/icons/wirecons-free-vector-icons/32/add-128.png"/></div>
  <div class="col-md-2 col-xs-2 col-sm-2"><img class="img-responsive" src="https://freepythontips.files.wordpress.com/2013/07/python_logo_notext.png"/></div>
  <div class="col-md-2 col-xs-2 col-sm-2"><img class="img-responsive" src="https://cdn4.iconfinder.com/data/icons/wirecons-free-vector-icons/32/add-128.png "/></div>
  <div class="col-md-2 col-xs-2 col-sm-2"><img class="img-responsive" src="https://vuejs.org/images/logo.png"/></div>
</center>
</div>

## Objectives
* Generate data using webcrawling with requests from [Canada's Top 100](http://www.canadastop100.com)
* Use of [Scrapy](https://scrapy.org)
* Use of Pandas
* Integrate VueJS in a notebook
* Create simple table with filter functionality

## Scraping data
### Approach
To scrape the data, we will use the Scrapy library. Instead of writing our own scrapers, it is faster for this tutorial to simply use a proper library that was build to scrape for you.

1. Load the main page
2. Find all company links
3. For each company link, open the corresponding page
4. For each company page, find all ratings

### Markup for companies links
```html
<div id="winners" class="page-section">
...
  <li><span><a target="_blank" href="http://content.eluta.ca/top-employer-3m-canada">3M Canada Company</a></span></li>
...
</div>
```
This corresponds with the Python code from the CompanySpider class:
```python
for href in response.css('div#winners a::attr(href)').extract():
```

### Markup for ratings

```html
<h3 class="rating-row">
    <span class="nocolor">Physical Workplace</span>
    <span class="rating">
        <span class="score" title="Great-West Life Assurance Company, The's physical workplace is rated as exceptional. ">A+</span>
    </span>
</h3>
```
## Python crawler
The crawler in Scrapy is defined in the following code snippet.
```python
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class CompanySpider(scrapy.Spider):
    name = "companies"
    start_urls = [
        "http://www.canadastop100.com/national/"
    ]
    custom_settings = {
        'LOG_LEVEL': logging.CRITICAL,
        'FEED_FORMAT':'json',               
        'FEED_URI': 'canadastop100.json' 
    }
    
    def parse(self, response):
        for href in response.css('div#winners a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_company)
            
    def parse_company(self, response):
        name = response.css('div.side-panel-wrap div.widget h4::text').extract_first()
        for rating in response.css('h3.rating-row')[1:]:
            yield {
                'name': name,
                'title': rating.css('span.nocolor::text').extract_first(),
                'value': rating.css('span.rating span.score::text').extract_first(),
            }
```

Make sure the output file does not exist in the directory where the script is going to be executed.
```bash
rm canadastop100.json
```

Next we need to define the crawling processor with the following:
```python
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(CompanySpider)
process.start()
```
Executing this will give the following result:

    2017-10-06 12:09:45 [scrapy.utils.log] INFO: Scrapy 1.4.0 started (bot: scrapybot)
    2017-10-06 12:09:45 [scrapy.utils.log] INFO: Overridden settings: {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}

## Preparing data

```python
import pandas as pd
```
Read the output file from the scraper.
```python
df = pd.read_json('canadastop100.json')
df.head()
```



<div class="row">
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe table table-responsive">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>title</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bell Canada</td>
      <td>Physical Workplace</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bell Canada</td>
      <td>Work Atmosphere &amp; Communications</td>
      <td>A</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bell Canada</td>
      <td>Financial Benefits &amp; Compensation</td>
      <td>A</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bell Canada</td>
      <td>Health &amp; Family-Friendly Benefits</td>
      <td>B</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Bell Canada</td>
      <td>Vacation &amp; Personal Time-Off</td>
      <td>B</td>
    </tr>
  </tbody>
</table>
</div>


Get the unique names in the database.
```python
len(df['name'].unique())
```

    101

Filter out the companies without a title.
```python
df = df[df['title'].notnull()]
```

The unique elements in the value column are given by
```python
df['value'].unique()
```
and result in

    array(['A+', 'A', 'B', 'B+', 'B-', 'A-', 'C+'], dtype=object)

Lets map these values to a number to make it easier to work them in the dataset. Define the mapping:

```python
mapping = {'A+': 10,
           'A': 9,
           'A-': 8,
           'B+': 7,
           'B': 6,
           'B-': 5,
           'C+': 4}
```

and apply the mapping to the value column:

```python
df['value'] = df['value'].map(mapping)
```

Now we need to transpose the dataframe, since we want a matrix with the companies per row and the different scores as a column.

```python
df = df.pivot(index='name', columns='title', values='value')
```

We add a column to get the total score:

```python
df['Total Score'] = df.sum(axis=1)
```

The dataframe has the following layout after adding the extra column:

```python
df.head()
```

<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe table table-responsive">
  <thead>
    <tr style="text-align: right;">
      <th>title</th>
      <th>Community Involvement</th>
      <th>Employee Engagement &amp; Performance</th>
      <th>Financial Benefits &amp; Compensation</th>
      <th>Health &amp; Family-Friendly Benefits</th>
      <th>Physical Workplace</th>
      <th>Training &amp; Skills Development</th>
      <th>Vacation &amp; Personal Time-Off</th>
      <th>Work Atmosphere &amp; Communications</th>
      <th>Total Score</th>
    </tr>
    <tr>
      <th>name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3M Canada Company</th>
      <td>10</td>
      <td>7</td>
      <td>9</td>
      <td>9</td>
      <td>10</td>
      <td>9</td>
      <td>6</td>
      <td>10</td>
      <td>70</td>
    </tr>
    <tr>
      <th>Aboriginal Peoples Television Network Inc. / APTN</th>
      <td>9</td>
      <td>6</td>
      <td>7</td>
      <td>9</td>
      <td>7</td>
      <td>9</td>
      <td>9</td>
      <td>9</td>
      <td>65</td>
    </tr>
    <tr>
      <th>Accenture Inc.</th>
      <td>10</td>
      <td>9</td>
      <td>7</td>
      <td>9</td>
      <td>7</td>
      <td>7</td>
      <td>6</td>
      <td>9</td>
      <td>64</td>
    </tr>
    <tr>
      <th>Agrium Inc.</th>
      <td>10</td>
      <td>7</td>
      <td>7</td>
      <td>6</td>
      <td>10</td>
      <td>10</td>
      <td>8</td>
      <td>9</td>
      <td>67</td>
    </tr>
    <tr>
      <th>Air Canada</th>
      <td>10</td>
      <td>6</td>
      <td>9</td>
      <td>7</td>
      <td>9</td>
      <td>10</td>
      <td>4</td>
      <td>6</td>
      <td>61</td>
    </tr>
  </tbody>
</table>
</div>

As a last step we need to attach the dataframe to the body of the notebook by using some JavaScript. We import the proper libraries

```python
from IPython.display import HTML, Javascript, display
```

and attach the dataframe, after converting, to the window.

```python
Javascript("""§
           window.companyData={};
           """.format(df.reset_index().to_json(orient='records')))
```

    <IPython.core.display.Javascript object>

Write to JSON file on disk if you want. This can be used in turn to move to the server where the VueJS application will be deployed. 

```python
df.reset_index().to_json('canadastop100.json', orient='records')
```

## Visualizing data
Next step is to visualize the data using VueJS. VueJS can be included from https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.0/vue. This notebook will make use of the example of the [grid-component](https://vuejs.org/v2/examples/grid-component.html) from the official documentation to create a table representing the crawled data.

Add the requirement to the notebook.

```python
%%javascript
require.config({
    paths: {
        vue: "https://cdnjs.cloudflare.com/ajax/libs/vue/2.4.0/vue"
    }
});
```


    <IPython.core.display.Javascript object>

Define the template for displaying the data in a table using the x-template script type and the VueJS syntax.

```python
%%html
<script type="text/x-template" id="data-template">
  <table class="canada">
    <thead>
      <tr>
        <th v-for="key in columns"
          @click="sortBy(key)"
          :class="{ active: sortKey == key }">
          {{ key | capitalize }}
          <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="entry in filteredData">
        <td v-for="key in columns">
          {{entry[key]}}
        </td>
      </tr>
    </tbody>
  </table>
</script>
```


<script type="text/x-template" id="data-template">
  <table class="canada">
    <thead>
      <tr>
        <th v-for="key in columns"
          @click="sortBy(key)"
          :class="{ active: sortKey == key }">
          {{ key | capitalize }}
          <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'">
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="entry in filteredData">
        <td v-for="key in columns">
          {{entry[key]}}
        </td>
      </tr>
    </tbody>
  </table>
</script>

Define the main HTML that contains the template we defined earlier.

```python
%%html
<div id="vue-app">
  <form id="search">
    Search <input name="query" v-model="searchQuery">
  </form>
  <data-grid
    :data="gridData"
    :columns="gridColumns"
    :filter-key="searchQuery">
  </data-grid>
</div>
```


<div id="vue-app">
  <form id="search">
    Search <input name="query" v-model="searchQuery">
  </form>
  <data-grid
    :data="gridData"
    :columns="gridColumns"
    :filter-key="searchQuery">
  </data-grid>
</div>

Initialize the VueJS application using Javascript by extracting the data from the window, attaching the component with the table for the data and creating a new Vue instance.

```python
%%javascript
require(['vue'], function(Vue) {
    console.log(Vue.version);
    var companyData = window.companyData;
    console.log(JSON.stringify(companyData));
    Vue.component('data-grid', {
      template: '#data-template',
      props: {
        data: Array,
        columns: Array,
        filterKey: String
      },
      data: function () {
        var sortOrders = {}
        this.columns.forEach(function (key) {
          sortOrders[key] = 1
        })
        return {
          sortKey: '',
          sortOrders: sortOrders
        }
      },
      computed: {
        filteredData: function () {
          var sortKey = this.sortKey
          var filterKey = this.filterKey && this.filterKey.toLowerCase()
          var order = this.sortOrders[sortKey] || 1
          var data = this.data
          if (filterKey) {
            data = data.filter(function (row) {
              return Object.keys(row).some(function (key) {
                return String(row[key]).toLowerCase().indexOf(filterKey) > -1
              })
            })
          }
          if (sortKey) {
            data = data.slice().sort(function (a, b) {
              a = a[sortKey]
              b = b[sortKey]
              return (a === b ? 0 : a > b ? 1 : -1) * order
            })
          }
          return data
        }
      },
      filters: {
        capitalize: function (str) {
          return str.charAt(0).toUpperCase() + str.slice(1)
        }
      },
      methods: {
        sortBy: function (key) {
          this.sortKey = key
          this.sortOrders[key] = this.sortOrders[key] * -1
        }
      }
    })

    var vueApp = new Vue({
      el: '#vue-app',
      data: {
        searchQuery: '',
        gridColumns: Object.keys(companyData[0]),
        gridData: companyData
      }
    })
  
});
```


    <IPython.core.display.Javascript object>

Attach a style to make the table more attractive.

```python
%%html
<style>
table.canada {
  border: 2px solid rgb(102, 153, 255);
  border-radius: 3px;
  background-color: #fff;
}

table.canada th {
  background-color: rgb(102, 153, 255);
  color: rgba(255,255,255,0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

table.canada td {
  background-color: #f9f9f9;
}

table.canada th, table.canada td {
  min-width: 120px;
  padding: 10px 20px;
}

table.canada th.active {
  color: #fff;
}

table.canada th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}
</style>
```


<style>
table.canada {
  border: 2px solid rgb(102, 153, 255);
  border-radius: 3px;
  background-color: #fff;
}

table.canada th {
  background-color: rgb(102, 153, 255);
  color: rgba(255,255,255,0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

table.canada td {
  background-color: #f9f9f9;
}

table.canada th, table.canada td {
  min-width: 120px;
  padding: 10px 20px;
}

table.canada th.active {
  color: #fff;
}

table.canada th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}
</style>

The result can also be tested on the [jsfiddle](https://jsfiddle.net/jitsejan/rxxjhgf6) that I have created. The source for the page can be found in my [Vue](https://github.com/jitsejan/vuejs/tree/master/grid-example-01) repository and is visible on my [bl.ocks.org](https://bl.ocks.org/jitsejan/ccf44862b5e90e67c689858c63016bd1).  The notebook can be found on my [Github](https://github.com/jitsejan/notebooks/blob/master/notebooks/Project%20-%20Using%20JavaScript%20%26%20VueJS.ipynb) and the final result is shown on [this](http://vue.jitsejan.com/grid-example-01/) page.

<iframe width="100%" height="400" src="//jsfiddle.net/jitsejan/rxxjhgf6/embedded/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>