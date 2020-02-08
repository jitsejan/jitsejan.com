Title: Integrating PySpark with Redshift
Date: 2020-02-08 16:48
Modified: 2020-02-08 16:48
Category: posts
Tags: Python, PySpark, Redshift, dataframe, Spark
Slug: integrating-pyspark-with-redshift
Authors: Jitse-Jan
Summary: In my article on [how to connect to S3 from PySpark](https://www.jitsejan.com/integrating-pyspark-notebook-with-s3.html) I showed how to setup Spark with the right libraries to be able to connect to read and right from AWS S3. In the following article I show a quick example how I connect to Redshift and use the S3 setup to write the table to file. 

In my article on [how to connect to S3 from PySpark](https://www.jitsejan.com/integrating-pyspark-notebook-with-s3.html) I showed how to setup Spark with the right libraries to be able to connect to read and right from AWS S3. In the following article I show a quick example how I connect to Redshift and use the S3 setup to write the table to file. 

First of all I need the Postgres driver for Spark in order to make connecting to Redshift possible.

```bash
$ wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.6/postgresql-42.2.6.jar -P /opt/notebooks/
```

I have saved my configuration in the following variable for testing purposes. Of course it would be wise to store the details in environment variables or in a proper configuration file.

```python
config = {
    'aws_access_key': 'aaaaaa',
    'aws_secret_key': 'bbbbb',
    'aws_region': 'eu-west-2',
    'aws_bucket': 'my-bucket',
    'redshift_user': 'user',
    'redshift_pass': 'pass',
    'redshift_port': 1234,
    'redshift_db': 'mydatabase',
    'redshift_host': 'myhost',
}
```

Setting up the Spark context is straightforward. Make sure the Postgres library is available by adding it to `extraClassPath`, or copy it to the `jars` folder in the Spark installation location (`SPARK_HOME`).

```python
from pyspark import SparkContext, SparkConf, SQLContext

jars = [
    "/opt/notebooks/postgresql-42.2.6.jar"
]

conf = (
    SparkConf()
    .setAppName("S3 with Redshift")
    .set("spark.driver.extraClassPath", ":".join(jars))
    .set("spark.hadoop.fs.s3a.access.key", config.get('aws_access_key'))
    .set("spark.hadoop.fs.s3a.secret.key", config.get('aws_secret_key'))
    .set("spark.hadoop.fs.s3a.path.style.access", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set("com.amazonaws.services.s3.enableV4", True)
    .set("spark.hadoop.fs.s3a.endpoint", f"s3-{config.get('region')}.amazonaws.com")
    .set("spark.executor.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
    .set("spark.driver.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
)
sc = SparkContext(conf=conf).getOrCreate()
sqlContext = SQLContext(sc)
```

Now the Spark context is set I specify the schema and the table that I want to read from Redshift and write to S3.

```python
schema = 'custom'
table = 'postcodes'
```

The reading is done using the `jdbc` format and specifying the Redshift details:

```python
df = sqlContext.read \
               .format("jdbc") \
               .option("url", f"jdbc:postgresql://{config.get('redshift_host')}.redshift.amazonaws.com:{config.get('redshift_port')}/{config.get('redshift_db')}") \
               .option("dbtable", f"{schema}.{table}") \
               .option("user", config.get('redshift_user')) \
               .option("password", config.get('redshift_pass')) \
               .load()
```

Writing is easy since I specified the S3 details in the Spark configuration. 

```python
df.write.mode('overwrite').parquet("s3a://{config.get('aws_bucket')}/raw/{schema}/{table})
```

