Title: Casting a PySpark DataFrame column to a specific datatype
Date: 2019-12-30 04:06
Modified: 2019-12-30 04:06
Category: posts
Tags: Python, PySpark, trick, dataframe
Slug: casting-a-pyspark-column-datatype
Authors: Jitse-Jan
Summary: 


```python
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
# Cast the count column to an integer
dataframe.withColumn("count", F.col("count").cast(IntegerType()))
```