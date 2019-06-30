Title: Setting up Spark with Minio as object storage
Date: 2019-06-30 23:05
Modified: 2019-06-30 23:05
Category: posts
Tags: DevOps, Ansible, data engineer, VPS, Ubuntu, Spark, Minio, object storage
Slug: setting-up-spark-with-minio-as-object-storage
Authors: Jitse-Jan
Summary: To setup one of my data projects, I need (object) storage to save my data. Using Spark I want to be able to
read and write Parquet and other file formats.

## Objective
- Install [Spark](https://spark.apache.org/)
- Install [Hadoop](https://hadoop.apache.org/)
- Install [minIO](https://min.io/)  server
- Extend [Ansible](https://www.ansible.com/) configuration


## Introduction
At work we use AWS [S3](https://aws.amazon.com/s3/) for our datalake. Since I am working on some 
data projects, I would like to have a similar experience, but without AWS and simply on my own
server. This is the reason why I chose minIO as object storage, it's free, runs on Ubuntu and 
is compatible with the AWS S3 API.

## Installation
The [Ansible configuration](https://github.com/jitsejan/vps-provision) from my [previous blog post](https://www.jitsejan.com/creating-ansible-deployment-for-ubuntu-vps.html) already 
installed an older version of Spark. During my several attempts to get minIO working with Spark, I had to try different Hadoop versions, Spark and AWS libraries to make the installation work.
I used the latest version from the Spark [download page](https://spark.apache.org/downloads.html), which at the time of writing is `2.4.3`. Since I have to use the [latest](https://hadoop.apache.org/releases.html) Hadoop
version (3.1.2), I have to get the Spark download without Hadoop. The current Spark only support Hadoop version 2.7 or lower. For all the AWS libraries that are needed, I could only get the integration to
work with version 1.11.534.

The following Java libraries are needed to get minIO working with Spark:

- [hadoop-aws-3.1.2.jar](https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.1.2/hadoop-aws-3.1.2.jar)
- [aws-java-sdk-1.11.534.jar](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.534/aws-java-sdk-1.11.534.jar)
- [aws-java-sdk-core-1.11.534.jar](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.534/aws-java-sdk-core-1.11.534.jar)
- [aws-java-sdk-dynamodb-1.11.534.jar](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-dynamodb/1.11.534/aws-java-sdk-dynamodb-1.11.534.jar)
- [aws-java-sdk-kms-1.11.534.jar](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.534/aws-java-sdk-kms-1.11.534.jar)
- [aws-java-sdk-s3-1.11.534.jar](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.534/aws-java-sdk-s3-1.11.534.jar)
- [httpclient-4.5.3.jar](https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.3/httpclient-4.5.3.jar)
- [joda-time-2.9.9.jar](https://repo1.maven.org/maven2/joda-time/joda-time/2.9.9/joda-time-2.9.9.jar)

To run the minIO server, I first create a `minio` user and `minio` group. Additionally I create the data folder that minIO will store the data. After preparing
the environment I install minIO and add it as a service `/etc/systemd/system/minio.service`. 

```bash
[Unit]
Description=Minio
Documentation=https://docs.minio.io
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/usr/local/bin/minio

[Service]
WorkingDirectory=/usr/local/

User=minio
Group=minio

PermissionsStartOnly=true

EnvironmentFile=/etc/default/minio
ExecStartPre=/bin/bash -c "[ -n \"${MINIO_VOLUMES}\" ] || echo \"Variable MINIO_VOLUMES not set in /etc/default/minio\""

ExecStart=/usr/local/bin/minio server $MINIO_OPTS $MINIO_VOLUMES

# Let systemd restart this service only if it has ended with the clean exit code or signal.
Restart=on-success

StandardOutput=journal
StandardError=inherit

# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536

# Disable timeout logic and wait until process is stopped
TimeoutStopSec=0

# SIGTERM signal is used to stop Minio
KillSignal=SIGTERM

SendSIGKILL=no

SuccessExitStatus=0


[Install]
WantedBy=multi-user.target
```

The minIO environment file located at `/etc/default/minio` contains the configuration for the volume, the port and the credentials.
```
# Minio local/remote volumes.
MINIO_VOLUMES="/minio-data/"
# Minio cli options.
MINIO_OPTS="--address :9091 "

MINIO_ACCESS_KEY="mykey"
MINIO_SECRET_KEY="mysecret"
```

```bash
$ minio version
Version: 2019-06-27T21:13:50Z
Release-Tag: RELEASE.2019-06-27T21-13-50Z
Commit-ID: 36c19f1d653adf3ef70128eb3be1a35b6b032731

```

For the complete configuration, check the [role](https://github.com/jitsejan/vps-provision/tree/master/roles/minio) in Github.

## Code
The important bit is setting the right environment variables. Make sure the following variables are set:

```bash
export HADOOP_HOME=/opt/hadoop
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
export PATH=$PATH:$HADOOP_HOME/bin
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native
export SPARK_DIST_CLASSPATH=$(hadoop classpath)
```

After setting the environment variables, we need to make sure we connect to the minIO endpoint and set the credentials. Make 
sure the `path.style.access` is set to `True`. 

```python
from pyspark import SparkContext, SparkConf, SQLContext
conf = (
    SparkConf()
    .setAppName("Spark Minio Test")
    .set("spark.hadoop.fs.s3a.endpoint", "http://localhost:9091")
    .set("spark.hadoop.fs.s3a.access.key", os.environ.get('MINIO_ACCESS_KEY'))
    .set("spark.hadoop.fs.s3a.secret.key", os.environ.get('MINIO_SECRET_KEY'))
    .set("spark.hadoop.fs.s3a.path.style.access", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
)
sc = SparkContext(conf=conf).getOrCreate()
sqlContext = SQLContext(sc)
```

Once this is done, we can simply access the bucket and read a text file (given that this bucket and text file exists), and
we are able to write a dataframe to minIO. 

```python
print(sc.wholeTextFiles('s3a://datalake/test.txt').collect())
# Returns: [('s3a://datalake/test.txt', 'Some text\nfor testing\n')]
path = "s3a://user-jitsejan/mario-colors-two/"
rdd = sc.parallelize([('Mario', 'Red'), ('Luigi', 'Green'), ('Princess', 'Pink')])
rdd.toDF(['name', 'color']).write.csv(path)
```

## Todo
Currently there seems to be an issue with reading **small** files, it will give a Parquet error that the files are not big enough to read. It seems
more like a library issue, so I should just make sure I only work on big data.

## Credits
Thanks to [atosatto](https://github.com/atosatto/ansible-minio) for the Ansible role and [minio](https://github.com/minio/cookbook/blob/master/docs/apache-spark-with-minio.md)
for the great example.