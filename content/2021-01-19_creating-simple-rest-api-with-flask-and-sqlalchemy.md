Title: Creating a simple REST API with Flask and SQLAlchemy
Date: 2021-01-19 01:17
Modified: 2021-01-19 01:17
Category: posts
Tags: Python, postgres, PostgreSQL, SQLAlchemy, Flask, REST, API
Slug: creating-simple-rest-api-with-flask-and-sqlalchemy
Authors: Jitse-Jan
Summary: As a third tutorial in my Postgres related articles I am creating a basic REST API to retrieve data through Flask and SQLAlchemy from the Postgres database.

## Introduction

In my earlier posts I have discussed how to [install Postgres](https://www.jitsejan.com/setting-up-postgres-for-python.html), make it work with Python and create a simple [scraper](https://www.jitsejan.com/scraping-with-scrapy-and-postgres.html) to pull data from a website and add it to a Postgres table. In this quick post I make a very straightforward API that **only** supports two actions:

- Retrieve all items
- Retrieve a single item

I am not planning to update the API to support full [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) but want to show how easy it is to create a Flask API on top of Postgres. This post is a very basic example that could be a minimal setup for your own project. Note that there is no security or authorization at all (which should be okay when you run it locally).

## Requirements

Install the following three packages. I often use `pipenv` but feel free to use your own environment. The first two are essential packages to get Flask working with SQLAlchemy. The latter is a package to add a config file to your Flask folder to make it easier to run your application.

```bash
$ pipenv install flask-sqlalchemy flask-Migrate python-dotenv
```

## Implement the API

A `.env` file is used to set some configuration items for the Flask application. Create the `.flaskenv` in your Flask folder and define the application, if debug mode is enabled, what environment you are running this and optionally a different port to expose your API. Read more about the dotenv in the [Flask docs](https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv).

**.flaskenv**

```ini
FLASK_APP=app
FLASK_DEBUG=True
FLASK_ENV=development
FLASK_RUN_PORT=5055
```

As you might know if you've worked with Flask before the `app.py` contains the main application that creates the API (or other backend). Since I keep this API as simple as possible I will only use the `ItemsModel` as defined below this file. The Postgres details are stored as environment variables to avoid exposing them in the code. After initializing the Flask app and configuring the link to my Postgres database I setup the database and the migration. Finally I setup two routes as explained before, one to expose all the items and one to get details for a single item. The API only supports `GET` and will error if anything else is done with the API. I know the code can still be tidier by moving the database to a different file, or moving the routes to another file but for simplicity I keep it all in a single file.

**app.py**

```python
import os

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import ItemsModel

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
username = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASS"]
database = os.environ["POSTGRES_DB"]

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{username}:{password}@{host}:{port}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/items", methods=["GET"])
def handle_items():
    if request.method == "GET":
        items = ItemsModel.query.all()
        return jsonify([item.serialize for item in items])
    else:
        return {"message": "failure"}


@app.route("/items/<item_name>", methods=["GET"])
def handle_item(item_name):
    if request.method == "GET":
        try:
            item = ItemsModel.query.filter_by(name=item_name).first_or_404()
            return jsonify(item.serialize)
        except:
            return jsonify({"error": f"Item {item_name} not found"})
    else:
        return {"message": "Request method not implemented"}


if __name__ == "__main__":
    app.run(debug=True)

```

The final file that is needed to run the API is the `models.py` that defines the model(s) I will use. As I have described before and shown in the previous articles, I have added a set of items to the database with only two properties (name and price). This will be the data that I return through my API. The `ItemsModel` looks very similar to the [model](https://github.com/jitsejan/architecture-patterns-with-python/blob/main/data-retrieval/crawl/models.py) I have defined for the scraper which makes sense since it is both build using SQLAlchemy. 

**models.py**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ItemsModel(db.Model):
    """
    Defines the items model
    """

    __tablename__ = "items"

    name = db.Column("name", db.String, primary_key=True)
    price = db.Column("price", db.Integer)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Item {self.name}>"

    @property
    def serialize(self):
        """
        Return item in serializeable format
        """
        return {"name": self.name, "price": self.price}

```

## Run the API

Since I have used the `.flaskenv` file Flask knows the application file, the port to use and the other details. Run the API using `flask run` in the API folder.

```bash
 ~/rest-api $ flask run
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5055/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 999-994-971
```

## Verify the API

Using [httpie](https://httpie.io) we can easily validate the API by calling the `items` endpoint:

```bash
$ http get localhost:5000/items
HTTP/1.0 200 OK
Content-Length: 329
Content-Type: application/json
Date: Wed, 06 Jan 2021 20:22:10 GMT
Server: Werkzeug/1.0.1 Python/3.9.1

[
    {
        "name": "Boomerang",
        "price": 300
    },
    {
        "name": "Heart Container",
        "price": 4
    },
    {
        "name": "Blue Ring",
        "price": 250
    },
    {
        "name": "Red Water of Life",
        "price": 68
    },
    {
        "name": "Food",
        "price": 60
    },
    {
        "name": "Blue Water of Life",
        "price": 40
    },
    {
        "name": "Blue Candle",
        "price": 60
    },
    {
        "name": "Arrow",
        "price": 80
    },
    {
        "name": "Bow",
        "price": 980
    },
    {
        "name": "Bomb",
        "price": 20
    }
]
```

Also the endpoint for a single item seems to work fine too as shown below.

```basn
$ http get localhost:5000/items/Bomb
HTTP/1.0 200 OK
Content-Length: 27
Content-Type: application/json
Date: Wed, 06 Jan 2021 20:22:32 GMT
Server: Werkzeug/1.0.1 Python/3.9.1

{
    "name": "Bomb",
    "price": 20
}
```

The final code can be found on [Github](https://github.com/jitsejan/architecture-patterns-with-python/tree/main/rest-api).
