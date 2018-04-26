Title: Fancy select boxes using FontAwesome
Date: 2017-06-20 23:21
Modified: 2017-06-20 23:21
Category: posts
Tags: front-end, FontAwesome, design, javascript
Slug: select-boxes-with-font-awesome
Authors: Jitse-Jan
Summary: A simple example on how to use Font Awesome for fancy select boxes.

See the example on my [bl.ocks.org](https://bl.ocks.org/jqadrad/5d8a76d9bb4e6d91c2009a46ad36468a).

## index.html
The necessary JS and CSS files are included. Two select boxes are added to the main container.
```html
<head>
  <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
  <script type="text/javascript" src="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="script.js"></script>
  <link rel="stylesheet" type="text/css" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
  <div class="container">
    <div class="row">
      <h1>Drinks</h1>
      <div class="input-group col-md-12">
        <input id="coffee_cb" type="checkbox" class="coffee drink_cb" checked />
        <label for="coffee_cb"></label>
        <input id="wine_cb" type="checkbox" class="wine drink_cb" checked />
        <label for="wine_cb"></label>
      </div>
    </div>
    <div class="row">
      <h1>Selected filter</h1>
      <table>
        <tr>
          <th>Coffee</th>
          <td id="filterValCoffee"></td>
        </tr>
        <tr>
          <th>Wine</th>
          <td id="filterValWine"></td>
        </tr>
      </table>
    </div>
  </div>
</body>
```

## style.css
The checkbox itself is hidden and a background using FontAwesome is used instead.
```css
body {
  margin: 30px;
}

input[type=checkbox] {
  display: none;
}

input[type=checkbox] + label {
  color: black;
  font-size: 28px;
}

input[type=checkbox] + label:before {
  font-family: FontAwesome;
  display: inline-block;
  width: 50px;
  height: 50px;
  padding: 2px;
  background-color: white;
  text-align: center;
  -webkit-border-radius: 50%;
  -moz-border-radius: 50%;
  border-radius: 50%;
  border: black 2px solid;
  margin: 5px;
}

input[type=checkbox].coffee + label:before {
  content: "\f0f4";
}

input[type=checkbox].wine + label:before {
  content: "\f000";
}
input[type=checkbox]:checked + label:before {
  color: white;
  background-color: black;
}
```

## script.js
Retrieve the value of the checkboxes and set the HTML of its corresponding element.
```javascript
$( document ).ready(function() {

  function setItemValues() {
    $("#coffee_cb").is(":checked") ? coffeeCheck = 'Yes' : coffeeCheck = 'No';
    $("#wine_cb").is(":checked") ? wineCheck = 'Yes' : wineCheck = 'No';
    $('#filterValCoffee').html(coffeeCheck);
    $('#filterValWine').html(wineCheck);
  }

  $('.drink_cb').change(function() {
    setItemValues();
  });

  setItemValues();
});
```