Title: Getting started with Elasticsearch
Date: 2016-08-06 13:51
Modified: 2017-03-27 16:06
Category: posts
Tags: elasticsearch
Slug: getting-started-with-elasticsearch
Authors: Jitse-Jan
Summary: A short summary of my first experience with Elasticsearch.

#### Install ElasticSearch
``` shell
$ mkdir ~/es
$ cd ~/es
$ wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.5/elasticsearch-2.3.5.tar.gz
$ tar -xzvf elasticsearch-2.3.5.tar.gz
$ cd elasticsearch-2.3.5/
$ ./bin/elasticsearch -d
$ curl http://127.0.0.1:9200
```
At this point you should see something like
``` json
{
  "name" : "Gailyn Bailey",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "2.3.5",
    "build_hash" : "90f439ff60a3c0f497f91663701e64ccd01edbb4",
    "build_timestamp" : "2016-07-27T10:36:52Z",
    "build_snapshot" : false,
    "lucene_version" : "5.5.0"
  },
  "tagline" : "You Know, for Search"
}
```

#### Create the ES index for the posts
In the mappings part we want to differentiate between finding a hit in the title or in the body. A hit of the search in the title has twice as much value as a hit in the body.
``` python
#!/usr/bin/env python
data = {
    "settings": {
        "number_of_shards": 4,
        "number_of_replicas": 1
    },
    "mappings": {
        "blog": {
            "properties": {
                "title": { "type": "string", "boost": 4 },
                "body": { "type": "string", "boost": 2 },
            }
        }
    }
}
import json, requests
response = requests.put('http://127.0.0.1:9200/blog_index/', data=json.dumps(data))
print response.text
```
#### Add the entries
``` python
#!/usr/bin/env python
import json, requests
from blog.models import Entry

data = ''
for p in Entry.objects.all():
    data += '{"index": {"_id": "%s"}}\n' % p.pk
    data += json.dumps({
        "title": p.title,
        "body": p.body
    })+'\n'
response = requests.put('http://127.0.0.1:9200/blog_index/blog/_bulk', data=data)
print response.text
```
#### Search the entries
``` python
#!/usr/bin/env python
import json, requests
data = {
     "query": {
         "query_string": { "query": "python" }
     }
}
response = requests.post('http://127.0.0.1:9200/blog_index/blog/_search', data=json.dumps(data))
print response.json()
```
This gives the following reply:
``` json
{
  "hits": {
    "hits": [
      {
        "_score": 0.63516665,
        "_type": "blog",
        "_id": "4",
        "_source": {
          "body": "```python\r\n\"\"\" samples\/crawl_01.py \"\"\"\r\n################################################################################\r\n# Application:      WebParser example 01\r\n# File:             samples\/crawl_01.py\r\n# Goal:\r\n# Input:\r\n# Output:\r\n# Example:\r\n#\r\n# History:          2016-06-27 - JJ     Creation of the file\r\n#

...

main\r\n################################################################################\r\nif __name__ == \"__main__\":\r\n    main()\r\n```",
          "title": "Simple webcrawling in Python "
        },
        "_index": "blog_index"
      },
      {
        "_score": 0.4232868,
        "_type": "blog",
        "_id": "7",
        "_source": {
          "body": "This is a simple script to crawl information from a website when the content is dynamically loaded.\r\n```\r\n\"\"\" samples\/crawl_02.py \"\"\"\r\n################################################################################\r\n# Application:      WebParser example 02\r\n# File:             samples\/crawl_01.py\r\n# Goal:             Retrieve content when JavaScript is used in page\r\n# Input:\r\n# Output:\r\n# Example:\r\n#\r\n# History:          2016-06-27 - JJ     Creation of the file\r\n

...

main\r\n################################################################################\r\nif __name__ == \"__main__\":\r\n    main()\r\n```",
          "title": "Webcrawling in Python using Selenium"
        },
        "_index": "blog_index"
      },
      {
        "_score": 0.35721725,
        "_type": "blog",
        "_id": "13",
        "_source": {
          "body": "#### Installation\r\nUse the [Anaconda](https:\/\/www.continuum.io\/downloads \"Anaconda\") package. It will make starting with Data Science way easier, since almost all necessary packages are included and you can start right away.\r\n

...

[Source](http:\/\/twiecki.github.io\/blog\/2014\/11\/18\/python-for-data-science\/ \"Twiecki@Github\")",
          "title": "Get started with data science in Python"
        },
        "_index": "blog_index"
      }
    ],
    "total": 3,
    "max_score": 0.63516665
  },
  "_shards": {
    "successful": 4,
    "failed": 0,
    "total": 4
  },
  "took": 23,
  "timed_out": false
}
```
Each result will get a score and the results will be ordered accordingly. Of course the better the search query, the more the score will say about the likeliness of the result matching your query.