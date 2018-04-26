Title: Create an API using Eve in Python
Date: 2017-07-25 13:28
Modified: 2017-07-25 13:28
Category: posts
Tags: Python, API, MongoDB, Eve
Slug: creating-api-using-eve-and-mongodb
Authors: Jitse-Jan
Summary: A simple instruction to create an API for an existing MongoDB database using [Eve](http://python-eve.org/).

```shell
/Users/jitsejan/code  $ mkdir eve-api
/Users/jitsejan/code  $ cd eve-api/
/Users/jitsejan/code/eve-api  $ python3 -m pip install eve
/Users/jitsejan/code/eve-api  $ touch app.py
/Users/jitsejan/code/eve-api  $ sublime app.py
```

_api.py_

```python
from eve import Eve
import settings

app = Eve(settings=settings.settings)
 
if __name__ == '__main__':
    app.run()
```

```shell
/Users/jitsejan/code/eve-api  $ touch settings.py
/Users/jitsejan/code/eve-api  $ sublime settings.py
```

_settings.py_

```python
character = {
    'schema': {
        'name': {'type': 'string'},
        'color': {'type': 'string'},
        'superpower': {'type': 'string'},
    },
}
 
 
settings = {
    'MONGO_HOST': 'localhost',
    'MONGO_DBNAME': 'nintendo-database',
    'MONGO_USERNAME': 'db-user',
    'MONGO_PASSWORD': 'db-pass',
    'RESOURCE_METHODS': ['GET'],
    'DOMAIN': {
        'character': character,
    },
}
```

``` shell
/Users/jitsejan/code/eve-api  $ python app.py
```

Use [Postman](https://www.getpostman.com/) to connect to localhost:5000 and start using your API. 
Since the character schema has been defined, the characters are listed on localhost:5000/character. You can simply search 
by name and only retrieve a specific field using additional parameters.

```
localhost:5000/character?where={"name": "Mario"}&projection={"name": 1, "superpower":1}
```