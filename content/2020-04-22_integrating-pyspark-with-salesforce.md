Title: Integrating PySpark with Salesforce
Date: 2020-04-22 02:01
Modified: 2020-04-22 02:01
Category: posts
Tags: Python, PySpark, Salesforce, dataframe, Spar
Slug: integrating-pyspark-with-salesforce
Authors: Jitse-Jan
Summary: Another connection with PySpark that I needed for one of the projects at work. For our daily sync with Salesforce we use Python with [simple-salesforce](https://github.com/simple-salesforce/simple-salesforce) which makes it easy to pull data, but for Spark it takes a little more effort to get data out. 

To get a connection in Spark with Salesforce the advice is to use the `spark-salesforce` library. In order to make this work several dependencies need to be added. Make sure the core libraries to support XML are also downloaded. 

```bash
$ wget https://repo1.maven.org/maven2/com/springml/spark-salesforce_2.11/1.1.1/spark-salesforce_2.11-1.1.1.jar 
$ wget https://repo1.maven.org/maven2/com/springml/salesforce-wave-api/1.0.9/salesforce-wave-api-1.0.9.jar
$ wget https://repo1.maven.org/maven2/com/force/api/force-partner-api/40.0.0/force-partner-api-40.0.0.jar
$ wget https://repo1.maven.org/maven2/com/force/api/force-wsc/40.0.0/force-wsc-40.0.0.jar
$ wget https://repo1.maven.org/maven2/com/fasterxml/jackson/dataformat/jackson-dataformat-xml/2.10.3/jackson-dataformat-xml-2.10.3.jar
$ wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.10.3/jackson-core-2.10.3.jar
```

The configuration is saved in `config.ini` with the following fields:

```ini
[salesforce]
username = mail@jitsejan.com
password = securePassw0rd
token = sal3sforceT0ken
```

Loading the configuration is done using `configparser`:

```python
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
```

When creating the SparkSession make sure the paths to the differents JARs are correctly set:

```python
from pyspark import SparkSession

jars = [
    'spark-salesforce_2.11-1.1.1.jar',
    'salesforce-wave-api-1.0.9.jar',
    'force-partner-api-40.0.0.jar',
    'force-wsc-40.0.0.jar',
    'jackson-dataformat-xml-2.10.3.jar',
    'jackson-core-2.10.3.jar',
]
spark = (SparkSession
  .builder
  .appName("PySpark with Salesforce")
  .config("spark.driver.extraClassPath", ":".join(jars))
  .getOrCreate())  
```

The session is created and we are ready to pull some data:

```python
soql = "SELECT name, industry, type, billingaddress, sic FROM account"  
df = spark \
     .read \
     .format("com.springml.spark.salesforce") \
     .option("username", config.get('salesforce', 'username')) \
     .option("password", f"{config.get('salesforce', 'password')}{config.get('salesforce', 'token')}") \
     .option("soql", soql) \
     .load()
```
