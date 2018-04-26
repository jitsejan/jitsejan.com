Title: Creating a dashboard with MEAN.JS
Date: 2017-04-16 18:55
Modified: 2017-03-26 16:56
Category: posts
Tags: MongoDB, Express.js, Angular 2, Node, MEAN, dashboard, D3.js
Slug: creating-dashboard-with-meanjs
Authors: Jitse-Jan
Summary: I will make a dashboard to give an overview of the refills for the car using MEAN.JS and D3.js. 

I simply keep track of the amount, price and location and try to display it in interesting graphs. This tutorial is mainly an attempt to understand the MEAN stack and work with D3.js.

## Installation of MEAN.JS
I will skip the biggest part of installing MEAN.JS itself, since it is clearly explained on their website.

Follow the instructions from [MEAN.JS](http://meanjs.org/generator.html) to generate the scaffold.
```shell
jitsejan@jjvps:~/code$ npm install -g yo
jitsejan@jjvps:~/code$ npm install -g generator-meanjs
jitsejan@jjvps:~/code$ yo meanjs
```
Answer 'No' to all questions.

## Initialization
```shell
jitsejan@jjvps:~/code$ cd mean-dashboard/
jitsejan@jjvps:~/code/mean-dashboard$ git init
jitsejan@jjvps:~/code/mean-dashboard$ git add .
jitsejan@jjvps:~/code/mean-dashboard$ git commit -m "Initial commit"
jitsejan@jjvps:~/code/mean-dashboard$ grunt
```
At this point you should see the boilerplate of the MEAN.JS application.

By changing the modules/core/client/views/home.client.view.html the frontpage can be changed. I stripped it down to the following.
```html
<section ng-controller="HomeController">
  <div class="jumbotron text-center">
    <div class="row">
      <p class="lead">
        JJ's dashboards
      </p>
    </div>
  </div>
</section>
```
I also changed the title of the page by adapting config/env/default.js.

## Change the database
Change MongoDB url in config/env/development.js from:
```
uri: process.env.MONGOHQ_URL || process.env.MONGOLAB_URI || 'mongodb://' + (process.env.DB_1_PORT_27017_TCP_ADDR || 'localhost') + '/mean-dev',
```
to
```
uri: process.env.MONGOHQ_URL || process.env.MONGOLAB_URI || 'mongodb://' + (process.env.DB_1_PORT_27017_TCP_ADDR || 'localhost') + '/mean-dashboard',
```

## Create a CRUD-module
```shell
jitsejan@jjvps:~/code/mean-dashboard$ yo meanjs:crud-module refills
```
Next I want to add more fields to the refills by changing the model.

The fields I want are:

* Date of the refill [required]
* Amount of fuel [required]
* Litre price [required]
* Total cost [required]
* Address [required]
* Type of fuel [required]
* Longitude of the location [optional]
* Latitude of the location [optional]
* Distance [optional]

To modify the model, change the code in modules/refills/server/models/refill.server.model.js.
```javascript
'use strict';

/**
 * Module dependencies.
 */
var mongoose = require('mongoose'),
  Schema = mongoose.Schema;

/**
 * Refill Schema
 */
var RefillSchema = new Schema({
  name: {
    type: String,
    default: '',
    required: 'Please fill Refill name',
    trim: true
  },
  created: {
    type: Date,
    default: Date.now
  },
  user: {
    type: Schema.ObjectId,
    ref: 'User'
  }
});

mongoose.model('Refill', RefillSchema);

```

New code:
```javascript
var RefillSchema = new Schema({
  name: {
    type: String,
    default: '',
    required: 'Please fill Refill name',
    trim: true
  },
  date: {
    type: Date,
    required: 'Please fill Refill date'
  },
  kilometers: {
    type: Number,
    default: 0,
    required: 'Please fill Refill kilometers'
  },
  volume: {
    type: Number,
    default: 0,
    required: 'Please fill Refill volume'
  },
  price: {
    type: Number,
    default: 0,
    required: 'Please fill Refill litre price'
  },
  cost: {
    type: Number,
    default: 0,
    required: 'Please fill Refill cost'
  },
  created: {
    type: Date,
    default: Date.now
  },
  user: {
    type: Schema.ObjectId,
    ref: 'User'
  }
});
```
To create a new instance, I also updated the form in `modules/refills/client/form-refill.client.view.html`, but since this is pretty straight forward I will not show the code here.

At this point you should be able to create and list the refills. Update the other views to show the new fields.

## Create the line chart
Create a directive and choose `refills` as the module and 'line-chart' as the name.
```shell
jitsejan@jjvps:~/code/mean-dashboard$ yo meanjs:angular-directive line-chart
```
This will create the file `refills/client/directives/line-chart.client.directive.js`.

Install D3 via Bower.
```shell
jitsejan@jjvps:~/code/mean-dashboard$ bower install d3 --save
```

Add the JS file to the default config in 'config/assets/default.js' to the client JS.
```javascript
...
'public/lib/d3/d3.min.js',
...
```

The challenging part will be creating the D3 visualizations. The first graph is a line chart and the directive will have the following content.
```javascript
(function () {
  'use strict';

  angular
    .module('refills')
    .directive('lineChart', lineChart);

  lineChart.$inject = ['$window'];

  function lineChart($window) {
    return {
      template: '<svg width="960" height="500"></svg>',
      restrict: 'EA',
      link: function postLink(scope, element, attrs) {
        var d3 = $window.d3;
        var data = scope.vm.refills;
        
        console.log(d3.version);
        console.log(data);
        
        var svg = d3.select('svg'),
          margin = { top: 20, right: 20, bottom: 30, left: 50 },
          width = +svg.attr('width') - margin.left - margin.right,
          height = +svg.attr('height') - margin.top - margin.bottom,
          g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
        
        // 2017-04-18T22:35:19.352Z
        var parseTime = d3.utcParse('%Y-%m-%dT%H:%M:%S.%LZ');
        
        var x = d3.scaleTime().rangeRound([0, width]);
        var y = d3.scaleLinear().rangeRound([height, 0]);
        
        var line = d3.line()
          .x(function(d) { 
            return x(parseTime(d.date)); 
          })
          .y(function(d) { 
            return y(d.kilometers); 
          });
        
        x.domain(d3.extent(data, function(d) { return parseTime(d.date); }));
        y.domain(d3.extent(data, function(d) { return d.kilometers; }));
        
        
        g.append('g')
          .attr('transform', 'translate(0,' + height + ')')
          .call(d3.axisBottom(x))
        .select('.domain')
          .remove();
          
        g.append('g')
          .call(d3.axisLeft(y))
        .append('text')
          .attr('fill', '#000')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '0.71em')
          .attr('text-anchor', 'end')
          .text('Amount of kilometers');
        
        g.append('path')
          .datum(data)
          .attr('fill', 'none')
          .attr('stroke', 'steelblue')
          .attr('stroke-linejoin', 'round')
          .attr('stroke-linecap', 'round')
          .attr('stroke-width', 1.5)
          .attr('d', line);
        
      }
    };
  }
})();
```
Finally the graph needs to be added to a view. In my case I have added it to the list view of the refills.
```html
<div ng-if="vm.refills.$resolved && vm.refills.length">
  <div line-chart></div>
</div>
```
Important note: I have used the ng-if statement in order to have my data available in the directive. Without the if-statement I was not able to get the data in properly.

When you navigate to the refills list page the graph will now be visible.

Some additional graphs. Please note that currently the graphs are not-responsive and rescaling the window will not resize the graph.
## Bar chart
```shell
jitsejan@jjvps:~/code/mean-dashboard$ yo meanjs:angular-directive bar-chart
```
`modules/refills/client/directives/bar-chart.client.directive.js`
```javascript
(function () {
  'use strict';

  angular
    .module('refills')
    .directive('barChart', barChart);

  barChart.$inject = ['$window'];

  function barChart($window) {
    return {
      template: '<svg class="bar-chart" width="960" height="500"></svg>',
      restrict: 'EA',
      link: function postLink(scope, element, attrs) {
        var d3 = $window.d3;
        var data = scope.vm.refills;
        // SVG
        var svg = d3.select('svg.bar-chart'),
          margin = { top: 20, right: 20, bottom: 130, left: 50 },
          width = +svg.attr('width') - margin.left - margin.right,
          height = +svg.attr('height') - margin.top - margin.bottom,
          g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
        
        // Graph title
        g.append('text')
          .attr('x', (width / 2))             
          .attr('y', 0 - (margin.top / 3))
          .attr('text-anchor', 'middle')  
          .style('font-size', '16px') 
          .text('Volume per refill');
          
        var parseTime = d3.time.format('%Y-%m-%dT%H:%M:%S.%LZ').parse;
        var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.5);
        var y = d3.scale.linear().range([height, 0]);
        
        x.domain(data.map(function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.volume; })]);
        // X axis
        g.append('g')
          .attr('transform', 'translate(0,' + height + ')')
          .attr('class', 'x axis')
          .call(d3.svg.axis().scale(x).orient('bottom').tickFormat(function(d){ return parseTime(d).toISOString().substring(0, 10);}))
          .selectAll('text')	
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', function(d) {
              return 'rotate(-65)';
            });
        // Y axis
        g.append('g')
          .call(d3.svg.axis().scale(y).orient('left'));
        // Bars
        g.selectAll('.bar')
          .data(data)
        .enter().append('rect')
          .attr('class', 'bar')
          .attr('x', function(d) { return x(d.date); })
          .attr('width', x.rangeBand())
          .attr('y', function(d) { return y(d.volume); })
          .attr('height', function(d) { return height - y(d.volume); });
      }
    };
  }
})();
```

## World map
```shell
jitsejan@jjvps:~/code/mean-dashboard$ yo meanjs:angular-directive world-map
```
`modules/refills/client/directives/world-map.client.directive.js`
```javascript
(function () {
  'use strict';

  angular
    .module('refills')
    .directive('worldMap', worldMap);

  worldMap.$inject = ['$window'];

  function worldMap($window) {
    return {
      template: '<svg class="world-map" width="960" height="500"></svg>',
      restrict: 'EA',
      link: function postLink(scope, element, attrs) {
        var d3 = $window.d3;
        var topojson = $window.topojson;
        var data = scope.vm.refills;
        var svg = d3.select('svg.world-map'),
          margin = { top: 20, right: 20, bottom: 130, left: 50 },
          width = +svg.attr('width') - margin.left - margin.right,
          height = +svg.attr('height') - margin.top - margin.bottom,
          scale0 = (width - 1) / 2 / Math.PI,
          g = svg.append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
          
        svg.append('rect')
          .attr('class', 'overlay')
          .attr('width', width)
          .attr('height', height);    
        
        // Define the div for the tooltip
        var div = d3.select('body').append('div')	
            .attr('class', 'tooltip')				
            .style('opacity', 0);    
      
        var projection = d3.geo.mercator()
          .center([0, 5 ])
          .scale(200)
          .rotate([0,0]);
      
        var path = d3.geo.path()
          .projection(projection);
          
        var zoom = d3.behavior.zoom()
          .on('zoom',function() {
            g.attr('transform','translate('+ 
              d3.event.translate.join(',')+')scale('+d3.event.scale+')');
            g.selectAll('circle')
              .attr('d', path.projection(projection));
            g.selectAll('path')  
              .attr('d', path.projection(projection)); 
          });
        
        // Graph title
        g.append('text')
          .attr('x', (width / 2))             
          .attr('y', 0 - (margin.top / 3))
          .attr('text-anchor', 'middle')  
          .style('font-size', '16px') 
          .text('Locations');
        
        d3.json('https://unpkg.com/world-atlas@1/world/50m.json', function(error, world) {
          if (error) throw error;
  
          g.append('path')
            .datum({ type: 'Sphere' })
            .attr('class', 'sphere')
            .attr('d', path);
        
          g.append('path')
            .datum(topojson.merge(world, world.objects.countries.geometries))
            .attr('class', 'land')
            .attr('d', path);
        
          g.append('path')
            .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
            .attr('class', 'boundary')
            .attr('d', path);

          g.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx',function(d) {
              return projection([d.longitude, d.latitude])[0];
            })
            .attr('cy',function(d) {
              return projection([d.longitude, d.latitude])[1];
            })
            .attr('r', 5)
            .style('fill', 'red');
        });
        
        svg
          .call(zoom)
          .call(zoom.event);
        
       }
    };
  }
})();

```