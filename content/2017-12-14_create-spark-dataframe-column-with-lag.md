Title: Create Spark dataframe column with lag
Date: 2017-12-14 21:25
Modified: 2017-12-14 21:25
Category: posts
Tags: Python, lag, pyspark, dataframe
Slug: create-spark-dataframe-column-with-lag
Authors: Jitse-Jan
Summary: 

Create a lagged column in a PySpark dataframe:
```python
from pyspark.sql.functions import monotonically_increasing_id, lag
from pyspark.sql.window import Window

# Add ID to be used by the window function
df = df.withColumn('id', monotonically_increasing_id())
# Set the window
w = Window.orderBy("id")
# Create the lagged value
value_lag = lag('value').over(w)
# Add the lagged values to a new column
df = df.withColumn('prev_value', value_lag)
```