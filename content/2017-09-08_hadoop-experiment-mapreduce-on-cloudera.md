Title: Hadoop Experiment - MapReduce on Cloudera
Date: 2017-09-08 15:17
Modified: 2017-09-08 15:17
Category: posts
Tags: Hadoop, Cloudera, Docker, container, virtualization, mapreduce
Slug: hadoop-experiment-mapreduce-on-cloudera
Authors: Jitse-Jan
Summary: This post describes my first experiment with the Cloudera environment by trying to use the basic MapReduce method on a simple dataset.

<center><img src="http://community.cloudera.com/html/assets/cloudera-logo.png" width=100/></center>

In this example I will extract data with NES reviews from http://videogamecritic.com. I will create a dataframe, add some extra fields and save the data to a CSV-file. This file will be used for a simple MapReduce script.

Note: I have a Docker container running with Selenium instead of installing all dependencies on my system. See [this page](https://hub.docker.com/r/selenium/standalone-chrome/).

## Extract script
The script below is used to retrieve the data. It is ugly code, but it is doing the job.
```python
import lxml.html
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd

URL = 'http://videogamecritic.com/nes.htm'

def map_rating(rating):
    """ Function to convert the rating to a number """
    if (rating == "A+"): return 1;
    if (rating == "A"): return 2;
    if (rating == "A-"): return 3;
    if (rating == "B+"): return 4;
    if (rating == "B"): return 5;
    if (rating == "B-"): return 6;
    if (rating == "C+"): return 7;
    if (rating == "C"): return 8;
    if (rating == "C-"): return 9;
    if (rating == "D+"): return 10;
    if (rating == "D"): return 11;
    if (rating == "D-"): return 12;
    if (rating == "F"): return 13;
    if (rating == "F-"): return 14;
    return 15;

resp = requests.get(URL)
if resp.status_code != 200:
    raise Exception('GET '+link+' {}'.format(resp.status_code))
tree= lxml.html.fromstring(resp.content)
gamepages = ['http://videogamecritic.com/' + game.get('href') for game in tree.cssselect('h3 a')]
driver = webdriver.Remote("http://localhost:4444/wd/hub", DesiredCapabilities.CHROME)
gamedata = []
for page in gamepages:
    # Retrieve the data
    driver.get(page)
    data = lxml.html.fromstring(driver.page_source)
    # Extract the fields
    grades = [elem.text_content() for elem in data.cssselect('div[class*=\'hdr\']')]
    names = [elem.text_content() for elem in data.cssselect('div[class*=\'hdl\']')]
    metadata = [elem.text_content() for elem in data.cssselect('div[class*=\'mdl\']')]
    votes = [elem.text_content() for elem in data.cssselect('div[class*=\'vote\']')]
    # Append to dataset
    gamedata += list(zip(names, votes, grades, metadata))
driver.quit()
##
# DataFrame magic
##
df = pd.DataFrame.from_dict(gamedata)
df = df.rename(columns={0: "name", 1: "vote", 2: "grade", 3: "publisher"})
# Extract and convert data
df['reader_rating'] = df['vote'].str.extract('Readers:\s(.*?)\s\(', expand=True)
df['reader_rating']  = df['reader_rating'].apply(lambda x: map_rating(x)).astype('int')
df['number_of_votes'] = df['vote'].str.extract('\((\d*)\svotes\)', expand=True).astype('int')
df['grade'] = df['grade'].str.replace("Grade:", "").str.strip().apply(lambda x: map_rating(x)).astype('int')
df['publish_year'] = df['publisher'].str.extract('\((\d*)\)Reviewed', expand=True)
df['publisher'] = df['publisher'].str.extract("Publisher:\s(.*?)\s\(", expand=True)
df.drop('vote', axis=1, inplace=True)
# Calculate the total grade
df['total_grade'] = (df['grade'] + df['reader_rating']*df['number_of_votes']) / (df['number_of_votes']+1)
# Corrections
df['publisher'] = df['publisher'].str.replace('Electrobrain', 'Electro Brain')
# Save to file
df.to_csv('nesgamedata.csv', sep='\t', header=False)
```
This will result in the following file.
```shell
0	10-Yard Fight	12	Nintendo	10	44	1985	10.044444444444444
1	1942	11	Capcom	8	65	1985	8.045454545454545
2	1943	5	Capcom	4	58	1988	4.016949152542373
3	720 Degrees	13	Tengen	11	24	1989	11.08
4	8 Eyes	13	Taxan	10	30	1989	10.096774193548388
5	Abadox	11	Abadox	6	34	1989	6.142857142857143
6	Adventure Island	7	Hudson Soft	6	63	1987	6.015625
7	Adventure Island 2	4	Hudson Soft	5	40	1990	4.975609756097561
8	Adventure Island 3	4	Hudson Soft	5	27	1992	4.964285714285714
9	Adventures in the Magic Kingdom	5	Capcom	8	23	1990	7.875
...
```

## MapReduce script
Calculate how often what rating is used.

1. Map the reader ratings
2. Reduce to counts per rating

Lets create the script that will perform my first MapReduce action. The content of the following cell will be saved to a file which can in turn be used to perform the mapping and reducing.
```python
from mrjob.job import MRJob
from mrjob.step import MRStep

class GamesBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings)
        ]
    
    def mapper_get_ratings(self, _, line):
        (index, name, grade, publisher, reader_rating, number_of_votes, publish_year, total_grade) = line.split('\t') 
        yield reader_rating, 1
        
    def reducer_count_ratings(self, key, values):
        yield key, sum(values)
        
if __name__ == '__main__':
    GamesBreakdown.run()
```
## Execution
To use Hadoop, the command should look like the following and should be run on the Hadoop machine, with the hadoop-streaming-jar argument only given in case the .jar is not found:
```shell
python gamesbreakdown.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar nesgamedata.csv
```
To do this, upload the `nesgamesdata.csv` file and the script `gamesbreakdown.py` to HDFS, using the Hue files view and upload functionality. Next copy them to the local folder to be used in the command. Of course other methods to get the files locally on the Hadoop machine can be used.

I am using the [Cloudera Quickstart image](https://hub.docker.com/r/cloudera/quickstart/) to experiment with Docker and Cloudera and the `docker-compose.yml` contains the following:
```
version: '2'
services:
  cloudera:
    hostname: quickstart.cloudera
    command: /usr/bin/docker-quickstart
    tty: true
    privileged: true
    image: cloudera/quickstart:latest
    volumes:
      - ./data:/opt/data
    ports:
      - "8020:8020"
      - "8022:22"     # ssh
      - "7180:7180"   # Cloudera Manager
      - "8888:8888"   # HUE
      - "11000:11000" # Oozie
      - "50070:50070" # HDFS REST Namenode
      - "2181:2181"
      - "11443:11443"
      - "9090:9090"
      - "8088:8088"
      - "19888:19888"
      - "9092:9092"
      - "8983:8983"
      - "16000:16000"
      - "16001:16001"
      - "42222:22"
      - "8042:8042"
      - "60010:60010"
      - "8080:8080"
      - "7077:7077"

```
Connect to the machine and verify the file is present:
```shell
jitsejan@ssdnodes-jj-kvm:~/cloudera_docker$ docker exec -ti clouderadocker_cloudera_1 bash
[root@quickstart /]# cd home/
[root@quickstart home]# mkdir gamedata && cd $_
[root@quickstart gamedata]# hadoop fs -get gamedata/gamesbreakdown.py gamesbreakdown.py
[root@quickstart gamedata]# hadoop fs -get gamedata/nesgamedata.csv nesgamedata.csv
[root@quickstart gamedata]# ll
total 20
-rw-r--r-- 1 root root   590 Sep  5 13:42 gamesbreakdown.py
-rw-r--r-- 1 root root 15095 Sep  5 13:56 nesgamedata.csv
```
Install the mrjob library on the Cloudera container.
```shell
[root@quickstart gamedata]# yum install python-pip -y
[root@quickstart gamedata]# pip install mrjob
```

Run the script without using Hadoop to verify the installation.
```shell
[root@quickstart gamedata]# python gamesbreakdown.py nesgamedata.csv
No configs found; falling back on auto-configuration
Creating temp directory /tmp/gamesbreakdown.root.20170905.135809.859796
Running step 1 of 1...
Streaming final output from /tmp/gamesbreakdown.root.20170905.135809.859796/output...
"10"    15
"11"    14
"12"    12
"13"    4
"2"     9
"3"     28
"4"     44
"5"     34
"6"     48
"7"     31
"8"     28
"9"     15
Removing temp directory /tmp/gamesbreakdown.root.20170905.135809.859796...
```

Now use Hadoop to start the cluster magic.
```shell
[root@quickstart gamedata]# python gamesbreakdown.py -r hadoop nesgamedata.csv
No configs found; falling back on auto-configuration
Looking for hadoop binary in $PATH...
Found hadoop binary: /usr/bin/hadoop
Using Hadoop version 2.6.0
Looking for Hadoop streaming jar in /home/hadoop/contrib...
Looking for Hadoop streaming jar in /usr/lib/hadoop-mapreduce...
Found Hadoop streaming jar: /usr/lib/hadoop-mapreduce/hadoop-streaming.jar
Creating temp directory /tmp/gamesbreakdown.root.20170905.135908.241472
Copying local files to hdfs:///user/root/tmp/mrjob/gamesbreakdown.root.20170905.135908.241472/files/...
Running step 1 of 1...
  packageJobJar: [] [/usr/jars/hadoop-streaming-2.6.0-cdh5.7.0.jar] /tmp/streamjob3556720292725669631.jar tmpDir=null
  Connecting to ResourceManager at /0.0.0.0:8032
  Connecting to ResourceManager at /0.0.0.0:8032
  Total input paths to process : 1
  number of splits:2
  Submitting tokens for job: job_1504618114531_0001
  Submitted application application_1504618114531_0001
  The url to track the job: http://quickstart.cloudera:8088/proxy/application_1504618114531_0001/
  Running job: job_1504618114531_0001
  Job job_1504618114531_0001 running in uber mode : false
   map 0% reduce 0%
   map 50% reduce 0%
   map 100% reduce 0%
   map 100% reduce 100%
  Job job_1504618114531_0001 completed successfully
  Output directory: hdfs:///user/root/tmp/mrjob/gamesbreakdown.root.20170905.135908.241472/output
Counters: 49
        File Input Format Counters
                Bytes Read=19191
        File Output Format Counters
                Bytes Written=86
        File System Counters
                FILE: Number of bytes read=2307
                FILE: Number of bytes written=358424
                FILE: Number of large read operations=0
                FILE: Number of read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=19527
                HDFS: Number of bytes written=86
                HDFS: Number of large read operations=0
                HDFS: Number of read operations=9
                HDFS: Number of write operations=2
        Job Counters
                Data-local map tasks=2
                Launched map tasks=2
                Launched reduce tasks=1
                Total megabyte-seconds taken by all map tasks=8678400
                Total megabyte-seconds taken by all reduce tasks=3588096
                Total time spent by all map tasks (ms)=8475
                Total time spent by all maps in occupied slots (ms)=8475
                Total time spent by all reduce tasks (ms)=3504
                Total time spent by all reduces in occupied slots (ms)=3504
                Total vcore-seconds taken by all map tasks=8475
                Total vcore-seconds taken by all reduce tasks=3504
        Map-Reduce Framework
                CPU time spent (ms)=2450
                Combine input records=0
                Combine output records=0
                Failed Shuffles=0
                GC time elapsed (ms)=367
                Input split bytes=336
                Map input records=282
                Map output bytes=1737
                Map output materialized bytes=2313
                Map output records=282
                Merged Map outputs=2
                Physical memory (bytes) snapshot=651063296
                Reduce input groups=12
                Reduce input records=282
                Reduce output records=12
                Reduce shuffle bytes=2313
                Shuffled Maps =2
                Spilled Records=564
                Total committed heap usage (bytes)=679477248
                Virtual memory (bytes) snapshot=4099473408
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
Streaming final output from hdfs:///user/root/tmp/mrjob/gamesbreakdown.root.20170905.135908.241472/output...
"10"    15
"11"    14
"12"    12
"13"    4
"2"     9
"3"     28
"4"     44
"5"     34
"6"     48
"7"     31
"8"     28
"9"     15
Removing HDFS temp directory hdfs:///user/root/tmp/mrjob/gamesbreakdown.root.20170905.135908.241472...
Removing temp directory /tmp/gamesbreakdown.root.20170905.135908.241472...
```
Now lets add another reducer step to sort the counts of the ratings.
```python
from mrjob.job import MRJob
from mrjob.step import MRStep

class GamesBreakdownUpdate(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer=self.reducer_sorted_output)
        ]
    
    def mapper_get_ratings(self, _, line):
        (index, name, grade, publisher, reader_rating, number_of_votes, publish_year, total_grade) = line.split('\t') 
        yield reader_rating, 1
        
    def reducer_count_ratings(self, key, values):
        yield str(sum(values)).zfill(2), key
        
    def reducer_sorted_output(self, count, ratings):
        for rating in ratings:
            yield rating, count
        
if __name__ == '__main__':
    GamesBreakdownUpdate.run()
```
```shell
[root@quickstart gamedata]# python gamesbreakdownupdate.py nesgamedata.csv
No configs found; falling back on auto-configuration
Creating temp directory /tmp/gamesbreakdownupdate.root.20170905.142738.885314
Running step 1 of 2...
Running step 2 of 2...
Streaming final output from /tmp/gamesbreakdownupdate.root.20170905.142738.885314/output...
"13"	"04"
"2"	    "09"
"12"	"12"
"11"	"14"
"10"	"15"
"9"	    "15"
"3"	    "28"
"8"	    "28"
"7"	    "31"
"5"	    "34"
"4"	    "44"
"6"	    "48"
Removing temp directory /tmp/gamesbreakdownupdate.root.20170905.142738.885314...
```
That concludes my first experiments with Hadoop and MapReduce. Next step: using Pig or Spark to calculate similar statistics without all the overhead.