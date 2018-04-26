Title: Add CSS to Jupyter notebook
Date: 2016-11-12 11:40
Modified: 2017-03-27 17:41
Category: posts
Tags: Jupyter, notebook, CSS
Slug: add-css-to-jupyter-notebook
Authors: Jitse-Jan
Summary: 

To add some style to the notebook, Jupyter has the option to add a custom css file. This file should be located in __~/.jupyter/custom/custom.css__. If this file does not exist yet, create the directory if needed and add the stylesheet. Add the following code and refresh the notebook to see if it works.

``` css
body {
  background-color: purple;
}
```

To make it easier to modify this file, create a link from the stylesheet to the working directory for the notebooks in order to be able to modify the stylesheet in the browser.

``` shell
jitsejan@jjsvps:~/code/notebooks$ ln -s ~/.jupyter/custom/custom.css .
```