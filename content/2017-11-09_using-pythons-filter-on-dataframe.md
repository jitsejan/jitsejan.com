Title: Using Pythons filter to select columns in dataframe
Date: 2017-11-09 23:45
Modified: 2017-11-09 23:45
Category: posts
Tags: Python, filter, tool, lambda
Slug: using-pythons-filter-on-dataframe
Authors: Jitse-Jan
Summary: 

A simple trick to select columns from a dataframe:
```python
# Create the filter condition
condition = lambda col: col not in DESIRED_COLUMNS
# Filter the dataframe
filtered_df = df.drop(*filter(condition, df.columns))
```