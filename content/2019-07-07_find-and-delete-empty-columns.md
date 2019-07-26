Title: Find and delete empty columns in Pandas dataframe
Date: 2019-07-07-14:09
Modified: 2019-07-07-14:09
Category: posts
Tags: Python, pandas
Slug: find-and-delete-empty-columns-pandas-dataframe
Authors: Jitse-Jan
Summary: 

```python
# Find the columns where each value is null
empty_cols = [col for col in df.columns if df[col].isnull().all()]
# Drop these columns from the dataframe
df.drop(empty_cols,
        axis=1,
        inplace=True)
```