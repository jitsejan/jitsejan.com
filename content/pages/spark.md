Title: Spark cheatsheet
Date: 2019-07-07 13:51
Modified: 2019-07-07 13:51
Category: Python, Spark, PySpark
Tags: spark, pyspark, cheatsheet
Slug: spark-cheatsheet
Authors: Jitse-Jan
Summary: This is my Spark cheatsheet

Import PySpark

```python
import pyspark
```

## Setup SparkSession

```python
spark = pyspark.sql.SparkSession.builder \
        .master("local[*]") \
        .enableHiveSupport() \
        .getOrCreate()

```

## Read data

```python
json_sdf = spark.read.json("mydata.json")
```


## Convert RDD to Pandas DataFrame

```python
json_pdf = json_sdf.toPandas()
```


## Convert PySpark row to dictionary

```python
row.asDict(recursive=True)
```


## Join two dataframes

```python
import pyspark.sql.functions as F

df = df_01.alias('dfone').join(df_02.alias('dftwo'),
                               on=[F.col('dfone.id') == F.col('dftwo.id')],
                               how='left').drop('id')
```

## Select fields from dataframe

```python
df.select('id', 'name', 'country', 'amount').show()
```

## Expand JSON 

```python
df.withColumn('json',
              F.from_json(F.col('_json_col').cast('string'),
                          json_schema)).show()
```
