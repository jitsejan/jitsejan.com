Title: Hadoop Experiment - Spark with Pyspark in a Jupyter notebook
Date: 2017-09-22 16:17
Modified: 2017-09-22 16:17
Category: posts
Tags: Hadoop, Spark, Docker, container, mapreduce, Python
Slug: hadoop-experiment-spark-with-pyspark-in-jupyter
Authors: Jitse-Jan
Summary: Last time I started to experiment with Hadoop and simple scripts using MapReduce and Pig on a Cloudera Docker container. Now lets start playing with Spark, since this is the goto language for machine learning on Hadoop.

<center><img src="https://spark.apache.org/docs/0.9.0/img/spark-logo-hd.png" height=80 /></center>
### Docker setup
I will use the [Docker image](https://hub.docker.com/r/jupyter/pyspark-notebook/) from Jupyter. It contains Spark and Jupyter and makes developing and testing pyspark very easy. The Dockerfile will retrieve the Jupyter pyspark notebook image, add the Python requirements file and install the dependencies. It will start the Notebook server using Jupyter Lab on the given port. The resulting image can be found on my [Docker repo](https://hub.docker.com/r/jitsejan/pyspark/).
```
# Dockerfile
FROM jupyter/pyspark-notebook
ADD requirements.txt ./
RUN pip install -r requirements.txt
CMD ["start.sh", "jupyter", "lab", "--notebook-dir=/opt/notebooks", "--ip='*'", "--no-browser", "--allow-root", "--port=8559"]
```

To start the container, I use the following docker-compose.yml

```shell
version: '2'
services:
  pyspark:
    image: jitsejan/pyspark
    volumes:
      - ./notebooks:/opt/notebooks
      - ./data:/opt/data
    ports:
      - "8559:8559"
```

### Using Pyspark
```python
from pyspark import SparkConf, SparkContext
import collections
```

#### Configure the Spark connection
```python
conf = SparkConf().setMaster("local").setAppName("GameRatings")
sc = SparkContext(conf = conf)
```
Verify that the Spark context is working by creating a random RDD of 1000 values and pick 5 values.

```python
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)
```

    [820, 967, 306, 62, 448]


Next we can create an RDD from the data from the [previous](http://jitsejan.com/hadoop-experiment-mapreduce-on-cloudera.html) Hadoop notebook.
```
lines = sc.textFile("../data/nesgamedata.csv")
```
##### Experiment one
Lets calculate the average rating of the voters compared to the votes of the author.

```python
def parseLine(line):
    fields = line.split('\t')
    index = int(fields[0])
    name = fields[1]
    grade = float(fields[2])
    publisher = fields[3]
    reader_rating = float(fields[4])
    number_of_votes = int(fields[5])
    publish_year = int(fields[6])
    total_grade = float(fields[7])
    return (grade, total_grade, name, publisher, reader_rating, number_of_votes, publish_year)
```

We return the grade and the total grade as a tuple from the `parseLine` function.

```python
games_rdd = lines.map(parseLine)
games_rdd.take(2)
```




    [(12.0, 10.044444444444444, '10-Yard Fight', 'Nintendo', 10.0, 44, 1985),
     (11.0, 8.044776119402986, '1942', 'Capcom', 8.0, 66, 1985)]




Add a 1 to each line so we can sum the `total_grades`.

```python
games_mapped = games_rdd.mapValues(lambda x: (x, 1))
games_mapped.take(2)
```

    [(12.0, (10.044444444444444, 1)), (11.0, (8.044776119402986, 1))]


Sum all `total_grades` by using the key `grade`. For each row this will sum the grades and it will sum the 1's that we've added.

```python
games_reduced = games_mapped.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
games_reduced.take(2)
```

    [(12.0, (70.26902777777778, 7)), (11.0, (193.88550134591918, 25))]


Calculate the average `total_grade` for each `grade`.

```python
average_grade = games_reduced.mapValues(lambda x: x[0] / x[1])
results = average_grade.collect()
for result in results:
    print(result)
```


    (12.0, 10.03843253968254)
    (11.0, 7.755420053836767)
    (5.0, 5.05270714136425)
    (13.0, 10.26375094258694)
    (7.0, 6.212705308155384)
    (4.0, 4.909347517549459)
    (8.0, 7.0328696656678105)
    (9.0, 6.519739721431783)
    (6.0, 5.63766311790758)
    (2.0, 3.495086595355065)
    (3.0, 4.1090931800649315)
    (10.0, 6.9165990377786555)
    (1.0, 2.321295734457781)



##### Experiment two
Filter out all Nintendo games, where the publisher is the 4-th element in the row.

```python
nintendoGames = games_rdd.filter(lambda x: 'Nintendo' in x[3])
nintendoGames.take(2)
```



    [(12.0, 10.044444444444444, '10-Yard Fight', 'Nintendo', 10.0, 44, 1985),
     (5.0, 4.014705882352941, 'Balloon Fight', 'Nintendo', 4.0, 67, 1984)]

Take the year and the total grade.

```python
nintendoYears = nintendoGames.map(lambda x: (x[-1], x[1]))
nintendoYears.take(2)
```


    [(1985, 10.044444444444444), (1984, 4.014705882352941)]


Calculate the minimum grade for each year.

```python
minYears = nintendoYears.reduceByKey(lambda x, y: min(x,y))
results = minYears.collect()
for result in results:
    print('Year: {:d}\tMinimum score: {:.2f}'.format(result[0] , result[1]))
```


    Year: 1985	Minimum score: 2.00
    Year: 1984	Minimum score: 3.96
    Year: 1991	Minimum score: 2.98
    Year: 1990	Minimum score: 2.00
    Year: 1989	Minimum score: 3.99
    Year: 1988	Minimum score: 3.99
    Year: 1986	Minimum score: 2.98
    Year: 1987	Minimum score: 1.99
    Year: 1983	Minimum score: 6.02
    Year: 1992	Minimum score: 5.98
    Year: 1993	Minimum score: 6.92

Lets try using FlatMap to count the most occurring words in the titles of the NES games.

```python
words = games_rdd.flatMap(lambda x: x[2].split())
words.take(10)
```



    ['10-Yard',
     'Fight',
     '1942',
     '1943',
     '720',
     'Degrees',
     '8',
     'Eyes',
     'Abadox',
     'Adventure']




Now we count the words and sort by count.

```python
wordCounts = words.map(lambda x: (x,1)).reduceByKey(lambda x, y: x + y)
wordCountsSorted = wordCounts.map(lambda x: (x[1],x[0])).sortByKey()
results = wordCountsSorted.collect()
for count, word in reversed(results):
    print(word, count)
```


    The 20
    of 17
    Super 11
    the 11
    Baseball 9
    and 8
    2 8
    Ninja 7
    Man 7
    II 7
    Mega 6
    3 6
    Dragon 5
    Adventure 5
    Tecmo 4
    Spy 4
    version) 4
    ....

This will result in a list of words with weird characters, spaces and other unwanted content. The text can be filtered in the flatMap function.

```python
import re
def normalizeWords(text):
    """ Remove unwanted text """
    return re.compile(r'\W+', re.UNICODE).split(text[2].lower())

words_normalized = games_rdd.flatMap(normalizeWords)
wordNormCounts = words_normalized.countByValue()
for word, count in sorted(wordNormCounts.items(), key=lambda x: x[1], reverse=True):
    if word.encode('ascii', 'ignore'):
        print(word, count)

```


    the 31
    of 17
    2 12
    ii 11
    super 11
    baseball 9
    s 9
    and 8
    3 7
    man 7
    ninja 7
    dragon 6
    mega 6
    adventure 5
    adventures 4
    n 4
    donkey 4
    kong 4
    mario 4
    monster 4
    warriors 4
    version 4
    ....

We can of course improve the normalize function and use NLTK or any other language processing library to clean up the stopwords, verbs and other undesired words in the text.

The notebook can be found [here](https://github.com/jitsejan/notebooks/blob/master/notebooks/Project%20-%20Hadoop%20experiment.ipynb).

