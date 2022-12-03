Title: Using PySpark with S3 (Updated)
Date: 2022-12-02 10:14
Modified: 2022-12-02 10:14
Category: posts
Tags: Python, Spark, PySpark, AWS, S3
Slug: using-pyspark-with-s3-updated
Authors: Jitse-Jan
Summary: Installing Spark on your local machine is always a challenge. For future reference I wrote down the steps to make Spark 3.3.1 work on my MacBook.

## Install Apache Spark
Install Apache Spark (3.3.1 currently) on MacOS through brew

```bash
$ brew install apache-spark
$ brew info apache-spark
==> apache-spark: stable 3.3.1 (bottled), HEAD
Engine for large-scale data processing
https://spark.apache.org/
/Users/jitsejan/homebrew/Cellar/apache-spark/3.3.1 (1,512 files, 605.3MB) *
  Poured from bottle on 2022-11-28 at 19:34:56
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/apache-spark.rb
License: Apache-2.0
==> Dependencies
Required: openjdk ✔
==> Options
--HEAD
        Install HEAD version
==> Analytics
install: 6,463 (30 days), 16,623 (90 days), 59,684 (365 days)
install-on-request: 6,459 (30 days), 16,606 (90 days), 59,625 (365 days)
build-error: 0 (30 days)
```

Note: I installed wget to easily download the JAR files.

```bash
$ brew install wget
$ wget --version
GNU Wget 1.21.3 built on darwin21.6.0.
```

## Installing JAR files
Download JAR files to enable Spark with AWS S3:

`aws-java-sdk-bundle version 1.12.349`

```bash
$ wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.349/aws-java-sdk-bundle-1.12.349.jar
```

`hadoop-aws version 3.3.1`

```bash
$ wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar
```

## Setup AWS profile 
In order to use [gimme-aws-creds](https://github.com/Nike-Inc/gimme-aws-creds) and PySpark, add the following to your `~/.aws/credentials`:

```bash
[profile local]
source_profile = org-sso
role_arn = arn:aws:iam::123456789:role/my-dev-role
```

where `org-sso` refers to the profile that is used by gimme-aws-creds. The `role_arn` is the role that you want to use with Spark and should have permissions on AWS to perform read or write actions.

Set the environment variable for `AWS_PROFILE` to the profile you have defined in the previous step. In my case this would be local. Next, create a Spark session and set the credential provider to use the AWS `ProfileCredentialsProvider`.

```python
import os

from pyspark.sql import SparkSession

# Set profile to be used by the credentials provider
os.environ["AWS_PROFILE"] = "local"
# Create Spark Session
spark = SparkSession.builder.getOrCreate()
# Make sure the ProfileCredentialsProvider is used to authenticate in Spark
spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.profile.ProfileCredentialsProvider")
Validate the code
S3_URI = "s3a://some-bucket-with-parquet-files/"
df = spark.read.parquet(S3_URI)
df.take(5)
```