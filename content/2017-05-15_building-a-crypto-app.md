Title: Building a crypto app with ExpressJS, MongoDB and D3.js
Date: 2017-05-15 23:21
Modified: 2017:05-15 23:21
Category: posts
Tags: notebook, Python, Jupyter, cryptocurrency, D3.js, Express.js, MongoDB
Slug: building-a-crypto-app
Authors: Jitse-Jan
Summary: In this post I will describe my initial version of my crypto app, an application where I will simply show some data of my experiments with crypto currencies. Data is handled by Python, put in MongoDB and displayed using ExpressJS and D3.js.

In this post I will describe my initial version of my crypto app, an application where I will simply show some data of my experiments with crypto currencies. Data is handled by Python, put in MongoDB and displayed using ExpressJS and D3.js.

The post is a bit long, but I try give my steps as clear as possible so it can be of any help to anyone.

## Structure of the application
The final structure of the app will look like the following.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app$ tree
.
├── app.js
├── data
│   ├── mining.csv
│   └── wallet.csv
├── notebook
│   └── CSV to MongoDB.ipynb
├── package.json
├── public
│   └── css
│       └── style.css
└── views
    ├── pages
    │   ├── index.ejs
    │   ├── mining.ejs
    │   └── wallet.ejs
    └── partials
        ├── footer.ejs
        ├── head.ejs
        └── header.ejs

7 directories, 11 files
```

## Version check
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ git --version
git version 2.11.0 (Apple Git-81)
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ npm -v
4.2.0
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ node -v
v7.10.0
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ python --version
Python 3.6.0 :: Anaconda 4.3.1 (x86_64)
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ jupyter --version
4.2.1
```

## Initialize
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ git init
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ npm init
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ echo node_modules >> .gitignore
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ git add . && git commit -am "Initial commit"
```

## Create the back-end using a Jupyter notebook
Using Python we will read two CSV files and add them to MongoDB.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ echo notebook/.ipynb_checkpoints >> .gitignore
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app/notebook  $ jupyter notebook
```
### Content of the notebook
<hr/>
{% notebook csv_to_mongodb.ipynb %}
<hr/>
Now the data is in the database we are ready to create the front-end.

## Create the front-end
First install the packages we need and save them to `package.json`.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ npm install --save express mongoose ejs mongodb
```
This will result in the following `package.json`.
```json
{
  "name": "crypto-app",
  "version": "1.0.0",
  "description": "Simple app to track some crypto investments",
  "main": "app.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [
    "crypto",
    "Python",
    "mongoose",
    "expressjs"
  ],
  "author": "jitsejan",
  "license": "ISC",
  "dependencies": {
    "ejs": "^2.5.6",
    "express": "^4.15.2",
    "mongodb": "^2.2.26",
    "mongoose": "^4.9.9"
  }
}
```

### The core
I will create three pages. A blank frontpage, a page for the wallet data and a page for the mining data. First we need setup the 
application in `app.js`. This file is responsible for the database connection and serving the templates for each route containing
the correct data.

```javascript
// Requirements
var express 	   = require('express');
var app 		   = express();
var mongoose 	   = require('mongoose');
// Make sure we can use HTML and JavaScript interchangeably
app.set('view engine', 'ejs');
// Database connection
mongoose.connect('mongodb://localhost/crypto-data'); 
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function callback () {
    console.log('Connected to Mongo database');
});
// Define the schema using Mongoose
var Schema = mongoose.Schema;
// The Mining schema should be the same as the data we put in Python
var miningSchema = new Schema({
    Date: Date,
    BTC: Number,
    DRK: Number,
    LTC: Number
});
// Create the model
var Mining = db.model('mining', miningSchema);
// The Wallet schema should be the same as the data we put in Python
var walletSchema = new Schema({
    Time: Date,
    BTC: Number,
    DOGE: Number,
    ETH: Number,
    LTC: Number,
    REP: Number
});
// Create the model
var Wallet = db.model('wallet', walletSchema);

// Create the route for the frontpage
app.get('/', function(req, res) {
	res.render('pages/index', { title: 'Home' });
});
// Create the route to the mining page
app.get('/mining', function(req, res) {
  Mining.find({}, null, {sort: {'Date':+1}}, function (err, minings){
    console.log(minings);
    res.render('pages/mining', { title:'Mining', minings: minings });
  })
});
// Create the route to the wallet page
app.get('/wallet', function(req, res) {
  Wallet.find({}, null, {sort: {'Time':+1}}, function (err, wallets){
    console.log(wallets);
    res.render('pages/wallet', { title:'Wallet', wallets: wallets });
  })
});
// Define the public directory (where the stylesheet lives)
// Normally this would be a subdirectory 'public/css/'
app.use(express.static(__dirname));
// Start the app on port 3000
app.listen(3000);
console.log('listening on port 3000');
```

### Partials

To easily create templates for the different pages, I will first create the partials for the head, footer and header. I will use Bootstrap
to make creating the layout easier.

`head.ejs`
```ejs
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="">
<meta name="author" content="">
<title>Crypto app</title>
<!-- Bootstrap Core CSS -->
<link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet">
<!-- Custom CSS -->
<link rel="stylesheet" type="text/css" href="public/css/style.css">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.3/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
<![endif]-->
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script>
```

`header.ejs`
```ejs
<!-- Navigation -->
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    <div class="container">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Crypto app</a>
        </div><!-- /.navbar-header -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
                <li>
                    <a href="./mining">Mining</a>
                </li>
                <li>
                    <a href="./wallet">Wallet</a>
                </li>
            </ul>
        </div><!-- /.navbar-collapse -->
    </div><!-- /.container -->
</nav>
```

`footer.ejs`
```ejs
<p class="text-center text-small text-muted">© Copyright 2017 - Crypto app</p>

<!-- JQuery JS-->
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<!-- Bootstrap Core JS -->
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
```

### Pages
Now creating the pages is simple. The frontpage is currently empty and will simply look like this:

`index.ejs`

```ejs
<!DOCTYPE html>
<html lang="en">
<head>
<% include ../partials/head %>
</head>
<body>
    <header>
        <% include ../partials/header %>
    </header>
    <main class="main wrap">
        <div class="container clear-top">
            <div class="row">
                <div class="col-lg-12 text-center">
                    <h1><%-title%></h1>
                </div>
            </div><!-- /.row -->
        </div><!-- /.container -->
    </main>
    <footer class="footer">
        <% include ../partials/footer %>
    </footer>
</body>
</html>
```

The mining page template is identical to the frontpage, but we add a placeholder for the D3.js graph and show the data in a table.

`mining.ejs`

```ejs
<!DOCTYPE html>
<html lang="en">
<head>
<% include ../partials/head %>
</head>
<body>
    <header>
        <% include ../partials/header %>
    </header>
    <main class="main wrap">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center">
                    <h1><%-title%></h1>
                </div>
            </div><!-- /.row -->
            <div class="row chart-container">
                <svg class="svg-chart" width="960" height="500">
                <!-- placeholder for the chart -->
                </svg>
            </div><!-- /.row -->
            <div class="row">
                <div class="col-lg-12">
                    <table class="table">
                      <tr>
                        <th>Date</th>
                        <th>BTC</th>
                        <th>DRL</th>
                        <th>LTC</th>
                      </tr>
                    <% minings.forEach(function(mining) { %>
                       <tr>
                         <td><%= mining.Date %></td>
                         <td><%= mining.BTC %></td>
                         <td><%= mining.DRK %></td>
                         <td><%= mining.LTC %></td>
                       </tr>
                    <% }); %>
                    </table>
                </div>
            </div><!-- /.row -->
        </div><!-- /.container -->
    </main>
    <footer>
        <% include ../partials/footer %>
    </footer>
</body>
</html>
```
Next I append te template with a Javascript block containing the D3.js graph code.
```ejs
// Convert the bitcoins data to the data we can use in DS.js
var data = <%- JSON.stringify(minings) %>;

var svg = d3.select('svg'),
    margin = {
        top: 20,
        right: 50,
        bottom: 100,
        left: 50
    },
    width = +svg.attr('width') - margin.left - margin.right,
    height = +svg.attr('height') - margin.top - margin.bottom,
    g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
// Graph title
g.append('text')
    .attr('x', (width / 2))
    .attr('y', 0 - (margin.top / 3))
    .attr('text-anchor', 'middle')
    .style('font-size', '16px')
    .text('Mining chart');
// Function to convert a string into a time
var parseTime = d3.time.format('%Y-%m-%dT%H:%M:%S.%LZ').parse;
// Function to show specific time format
var formatTime = d3.time.format('%e %B');
var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
        return "<span style='color:red'>" + d.worth + " </span> <strong>" + d.currency + "</strong>";
    })
svg.call(tip);
var color = d3.scale.category10();

color.domain(d3.keys(data[0]).filter(function(key) {
    return key !== "Date" && key !== "_id";
}));
// Correct the types
data.forEach(function(d) {
    d.date = parseTime(d.Date);
});
var rewards = color.domain().map(function(name) {
    return {
        name: name,
        values: data.map(function(d) {
            return {
                date: d.date,
                worth: +d[name],
                currency: name
            };
        })
    };
});
var num_bars = d3.keys(rewards).length;
var num_days = data.length;
var y = d3.scale.linear().range([height, 0]);

y.domain([
    0,
    d3.max(rewards, function(c) {
        return d3.max(c.values, function(v) {
            return v.worth;
        });
    })
]);
var x0 = d3.scale.ordinal()
    .domain(d3.range(num_days))
    .rangeBands([0, width], .2);
var x1 = d3.scale.ordinal()
    .domain(d3.range(num_bars))
    .rangeBands([0, x0.rangeBand()]);
var color = d3.scale.category10();
var xAxis = d3.svg.axis()
    .scale(x0)
    .tickFormat(function(d) {
        return formatTime(parseTime(data[d].Date));
    })
    .orient("bottom");
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
g.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Amount");
g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", function(d) {
        return "rotate(-90)"
    });
// Add the bars
g.append("g").selectAll(".bar")
    .data(rewards)
    .enter().append("g")
    .style("fill", function(d, i) {
        return color(i);
    })
    .attr("transform", function(d, i) {
        return "translate(" + x1(i) + ",0)";
    })
    .selectAll("rect")
    .data(function(d) {
        return d.values;
    })
    .enter().append("rect")
    .attr("class", "bar")
    .attr("width", x1.rangeBand())
    .attr("height", function(d) {
        return height - y(d.worth);
    })
    .attr("x", function(d, i) {
        return x0(i);
    })
    .attr("y", function(d) {
        return y(d.worth);
    })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);
var legend = g.append("g")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
    .attr("text-anchor", "end")
    .selectAll("g")
    .data(rewards)
    .enter().append("g")
    .attr("transform", function(d, i) {
        return "translate(0," + i * 20 + ")";
    });
legend.append("rect")
    .attr("x", width - 19)
    .attr("width", 19)
    .attr("height", 19)
    .attr("fill", function(d, i) {
        return color(i);
    })
legend.append("text")
    .attr("x", width - 24)
    .attr("y", 9.5)
    .attr("dy", "0.32em")
    .text(function(d) {
        return d.name;
    });
```
For the wallet page I have a similar approach.

`wallet.ejs`
```ejs
<!DOCTYPE html>
<html lang="en">
<head>
<% include ../partials/head %>
</head>
<body>
    <header>
        <% include ../partials/header %>
    </header>
    <main class="main wrap">
        <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center">
                    <h1><%-title%></h1>
                </div>
            </div><!-- /.row -->
            <div class="row chart-container">
                <svg class="svg-chart" width="960" height="500">
                <!-- placeholder for the chart -->
                </svg>
            </div><!-- /.row -->
            <div class="row">
                <div class="col-lg-12">
                    <table class="table">
                        <tr>
                            <th>Date</th>
                            <th>BTC</th>
                            <th>DOGE</th>
                            <th>ETH</th>
                            <th>LTC</th>
                            <th>REP</th>
                        </tr>
                        <% wallets.forEach(function(wallet) { %>
                        <tr>
                            <td><%= wallet.Time %></td>
                            <td><%= wallet.BTC %></td>
                            <td><%= wallet.DOGE %></td>
                            <td><%= wallet.ETH %></td>
                            <td><%= wallet.LTC %></td>
                            <td><%= wallet.REP %></td>
                        </tr>
                        <% }); %>
                    </table>
                </div>
            </div><!-- /.row -->
        </div><!-- /.container -->
    </main>
    <footer>
        <% include ../partials/footer %>
    </footer>
</body>
</html>
```
and the Javascript
```ejs
// Convert the bitcoins data to the data we can use in DS.js
var data = <%- JSON.stringify(wallets) %>;
// Draw a line chart
var svg = d3.select('svg.svg-chart'),
    margin = {
        top: 20,
        right: 50,
        bottom: 30,
        left: 50
    },
    width = +svg.attr('width') - margin.left - margin.right,
    height = +svg.attr('height') - margin.top - margin.bottom,
    g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
// Graph title
g.append('text')
    .attr('x', (width / 2))
    .attr('y', 0 - (margin.top / 3))
    .attr('text-anchor', 'middle')
    .style('font-size', '16px')
    .text('Wallet chart');
// Function to convert a string into a time
var parseTime = d3.time.format('%Y-%m-%dT%H:%M:%S.%LZ').parse;
// Function to show specific time format
var formatTime = d3.time.format('%e %B');

// Set the X scale
var x = d3.time.scale().range([0, width], 0.5);
// Set the Y scale
var y = d3.scale.linear().range([height, 0]);
// Set the color scale
var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    // .interpolate("basis")
    .x(function(d) {
        return x(d.date);
    })
    .y(function(d) {
        return y(d.worth);
    });
// Select the important columns
color.domain(d3.keys(data[0]).filter(function(key) {
    return key !== "Time" && key !== "_id";
}));
// Correct the types
data.forEach(function(d) {
    d.date = parseTime(d.Time);
});

var currencies = color.domain().map(function(name) {
    return {
        name: name,
        values: data.map(function(d) {
            return {
                date: d.date,
                worth: +d[name]
            };
        })
    };
});
// Set the X domain
x.domain(d3.extent(data, function(d) {
    return d.date;
}));
// Set the Y domain
y.domain([
    d3.min(currencies, function(c) {
        return d3.min(c.values, function(v) {
            return v.worth;
        });
    }),
    d3.max(currencies, function(c) {
        return d3.max(c.values, function(v) {
            return v.worth;
        });
    })
]);
// Set the X axis
g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
// Set the Y axis
g.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Value (USD)");

// Draw the lines
var currency = g.selectAll(".currency")
    .data(currencies)
    .enter().append("g")
    .attr("class", "currency");

currency.append("path")
    .attr("class", "line")
    .attr("d", function(d) {
        return line(d.values);
    })
    .style("stroke", function(d) {
        return color(d.name);
    });
// Add the circles
currency.append("g").selectAll("circle")
    .data(function(d) {
        return d.values
    })
    .enter()
    .append("circle")
    .attr("r", 2)
    .attr("cx", function(dd) {
        return x(dd.date)
    })
    .attr("cy", function(dd) {
        return y(dd.worth)
    })
    .attr("fill", "none")
    .attr("stroke", function(d) {
        return color(this.parentNode.__data__.name)
    });
// Add label to the end of the line
currency.append("text")
    .attr("class", "label")
    .datum(function(d) {
        return {
            name: d.name,
            value: d.values[d.values.length - 1]
        };
    })
    .attr("transform", function(d) {
        return "translate(" + x(d.value.date) + "," + y(d.value.worth) + ")";
    })
    .attr("x", 3)
    .attr("dy", ".35em")
    .text(function(d) {
        return d.name;
    });
// Add the mouse line
var mouseG = g.append("g")
    .attr("class", "mouse-over-effects");

mouseG.append("path")
    .attr("class", "mouse-line")
    .style("stroke", "black")
    .style("stroke-width", "1px")
    .style("opacity", "0");

var lines = document.getElementsByClassName('line');

var mousePerLine = mouseG.selectAll('.mouse-per-line')
    .data(currencies)
    .enter()
    .append("g")
    .attr("class", "mouse-per-line");

mousePerLine.append("circle")
    .attr("r", 7)
    .style("stroke", function(d) {
        return color(d.name);
    })
    .style("fill", "none")
    .style("stroke-width", "2px")
    .style("opacity", "0");

mousePerLine.append("text")
    .attr("class", "hover-text")
    .attr("dy", "-1em")
    .attr("transform", "translate(10,3)");

// Append a rect to catch mouse movements on canvas
mouseG.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'none')
    .attr('pointer-events', 'all')
    .on('mouseout', function() { // on mouse out hide line, circles and text
        d3.select(".mouse-line")
            .style("opacity", "0");
        d3.selectAll(".mouse-per-line circle")
            .style("opacity", "0");
        d3.selectAll(".mouse-per-line text")
            .style("opacity", "0");
    })
    .on('mouseover', function() { // on mouse in show line, circles and text
        d3.select(".mouse-line")
            .style("opacity", "1");
        d3.selectAll(".mouse-per-line circle")
            .style("opacity", "1");
        d3.selectAll(".mouse-per-line text")
            .style("opacity", "1");
    })
    .on('mousemove', function() { // mouse moving over canvas
        var mouse = d3.mouse(this);

        d3.selectAll(".mouse-per-line")
            .attr("transform", function(d, i) {

                var xDate = x.invert(mouse[0]),
                    bisect = d3.bisector(function(d) {
                        return d.date;
                    }).left;
                idx = bisect(d.values, xDate);

                d3.select(this).select('text')
                    .text(y.invert(y(d.values[idx].worth)).toFixed(2));

                d3.select(".mouse-line")
                    .attr("d", function() {
                        var data = "M" + x(d.values[idx].date) + "," + height;
                        data += " " + x(d.values[idx].date) + "," + 0;
                        return data;
                    });
                return "translate(" + x(d.values[idx].date) + "," + y(d.values[idx].worth) + ")";
            });
    });
```
Last thing we need to add is some custom style to the pages and graphs.
`style.css`
```css
html, body{
    height: 100%;
}
body {
	background-color: #eee;
    padding-top: 70px;
    padding-bottom: 70px;
}
.wrap{
	min-height: 100%;
}
.text-small{
	font-size: small;
}
.chart-container{
	margin: 0px auto;
	padding: 40px;
}
.main {
  overflow:auto;
  padding-bottom:50px; 
}
.footer {
  position: relative;
  margin-top: -50px;
  height: 50px;
  clear:both;
  padding-top:20px;
} 

/* Visualization */
path { 
	stroke-width: 1;
	fill: none;
	stroke-linejoin: round;
	stroke-linecap: round;
}
circle { 
  stroke-width: 1;
  fill: steelblue
}
.axis path,
.axis line {
  fill: none;
  stroke: grey;
  stroke-width: 1;
  shape-rendering: crispEdges;
}
.legend, .label, .hover-text{
	font-size: x-small;
	background-color: white;
}

.axis text {
  font: 10px sans-serif;
}
.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.bar:hover {
  fill: orangered ;
}
.d3-tip {
  line-height: 1;
  font-weight: bold;
  padding: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  border-radius: 2px;
}
/* Creates a small triangle extender for the tooltip */
.d3-tip:after {
  box-sizing: border-box;
  display: inline;
  font-size: 10px;
  width: 100%;
  line-height: 1;
  color: rgba(0, 0, 0, 0.8);
  content: "\25BC";
  position: absolute;
  text-align: center;
}
/* Style northward tooltips differently */
.d3-tip.n:after {
  margin: -1px 0 0 0;
  top: 100%;
  left: 0;
}
```
And that is it. Now by running the server, the application can be viewed on port 3000 of your localhost!
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/crypto-app  $ node app.js
```

## Result
I did not deploy the application on a server (yet) so it cannot be viewed. However, I have put my code on [Bitbucket](https://bitbucket.org/jitsejan/crypto-app) and the two
charts can be viewed as [Gist](http://gist.github.com/jqadrad) or [bl.ocks.org](http://bl.ocks.org/jqadrad).

The line chart can be viewed on [this](https://bl.ocks.org/jqadrad/a58719d82741b1642a2061c071ae2375) page. Using [rawgit](http://raw.git.com)
I was able to display it using an iframe.

<center>
<iframe src="https://rawgit.com/jqadrad/a58719d82741b1642a2061c071ae2375/raw/53bd826b39abcd55cbbfa2fd06a1e6b7e3bc5ce6/index.html" width="960" height="500" marginwidth="0" marginheight="0" scrolling="no" frameBorder="0"></iframe>
</center>

The bar chart can be viewed on [this](http://bl.ocks.org/jqadrad/819518e2dd11cb1eec6132837186db93) page. Because I am using an additional
library to create fancy tooltips, the iframe won't load properly.

Check my [Github repo](https://github.com/jitsejan/crypto-app-javascript-express-mongoose) for the source code.