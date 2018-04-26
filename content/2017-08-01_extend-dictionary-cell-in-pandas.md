Title: Extend dictionary cell to columns in Pandas dataframe
Date: 2017-08-01 23:18
Modified: 2017-08-01 23:18
Category: posts
Tags: Python, Pandas, conversion
Slug: extend-dictionary-cell-in-pandas
Authors: Jitse-Jan
Summary: 

``` python
df = pd.concat([df.drop(['meta'], axis=1), df['meta'].apply(pd.Series)], axis=1)
```