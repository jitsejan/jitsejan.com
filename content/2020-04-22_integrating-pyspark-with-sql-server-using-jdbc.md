Title: Integrating PySpark with SQL server using JDBC
Date: 2020-04-22 01:21
Modified: 2020-04-22 01:21
Category: posts
Tags: Python, PySpark, SQL, dataframe, Spark
Slug: integrating-pyspark-with-sql-server-using-jdbc
Authors: Jitse-Jan
Summary: In my series on connecting different sources to Spark I have explained how to connect to S3 and Redshift. To further extend my trials I show a quick demo on how to connect to a SQL server using JDBC.

First of all I need the JDBC driver for Spark in order to make the connection to a Microsoft SQL server.

```bash
$ wget https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/6.4.0.jre8/mssql-jdbc-6.4.0.jre8.jar -P /opt/notebooks/
```

The configuration is saved in `config.ini` with the following fields:

```ini
[mydb]
database = mydb
host = mydb-server.database.windows.net
username = readonly
password = mypassword
port = 1433
```

Loading the configuration is simple with `configparser`:

```python
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
```

Set the values for the connection:

```python
jdbc_url = f"jdbc:sqlserver://{config.get('mydb', 'host')}:{config.get('mydb', 'port')};database={config.get('mydb', 'database')}"
connection_properties = {
    "user": config.get('mydb', 'username'),
    "password": config.get('mydb', 'password')
}
```

When creating the SparkSession make sure the path to the JAR is correctly set:


```python
from pyspark.sql import SparkSession

jars = [
    "mssql-jdbc-6.4.0.jre8.jar",
]
spark = (SparkSession
  .builder
  .appName("PySpark with SQL server")
  .config("spark.driver.extraClassPath", ":".join(jars))
  .getOrCreate())  
```

The session is created and we can query the actual database:

```python
schema = 'dbo'
table = 'users'
```

The reading is done using the `jdbc` read option and specifying the connection details:

```python
df = spark \
    .read \
    .jdbc(jdbc_url,
          f"{schema}.{table}",
          properties=connection_properties)
```

An alternative approach is to use the same syntax as for the [Redshift article](https://www.jitsejan.com/integrating-pyspark-with-redshift.html) by omitting the `connection_properties` and use a more explicit notation.

```python
df = spark
    .read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", f"{schema}.{table}") \
    .option("user", config.get('mydb', 'username')) \
    .option("password", config.get('mydb', 'password')) \
    .load()
```
