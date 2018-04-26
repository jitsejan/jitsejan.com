title: Hadoop Experiment - Using Pig
Date: 2017-10-03 09:36
Modified: 2017-10-03 09:36
Category: posts
Tags: Hadoop, Pig, Docker, Cloudera, mapreduce
Slug: hadoop-experiment-pig-scripting
Authors: Jitse-Jan
Summary: In my previous posts I have already shown simple examples of using MapReduce and Spark with Pyspark. A missing piece moving from MapReduce to Spark is the usage of Pig scripts. This posts shows an example howto use a Pig script.

<center><img src="https://mapr.com/products/product-overview/apache-pig/assets/pig-image.png" height=80/></center>

## Pig
Using the [Pig language](https://pig.apache.org/docs/r0.7.0/piglatin_ref2.html), we can make a script to perform the MapReduce actions similar to the [previous post](http://jitsejan.com/hadoop-experiment-mapreduce-on-cloudera.html). Note that I will be using the same CSV file as before.


`gamedata_01.pig`
```
gamedata = LOAD 'nesgamedata.csv' AS (index:int, name:chararray, grade:chararray, publisher:chararray, reader_rating:chararray, number_of_votes:int, publish_year:int, total_grade:chararray);

DESCRIBE gamedata;

DUMP gamedata;
```
```shell
[root@quickstart gamedata]# pig -f gamedata_01.pig
...
(269,Winter Games,12,Epyx,13,24,1987,12.96)
(270,Wizards and Warriors,9,Rare,6,55,1987,6.053571428571429)
(271,World Games,6,Epyx,9,8,1986,8.666666666666666)
(272,Wrath of the Black Manta,7,Taito,6,31,1989,6.03125)
(273,Wrecking Crew,10,Nintendo,8,18,1985,8.105263157894736)
(274,Xevious,5,Namco,6,36,1988,5.972972972972973)
(275,Xexyz,10,Hudson Soft,5,26,1989,5.185185185185185)
(276,Yoshi,5,Nintendo,6,41,1992,5.976190476190476)
(277,Yoshi's Cookie,5,Nintendo,7,23,1993,6.916666666666667)
(278,Zanac,2,Pony,3,21,1986,2.9545454545454546)
(279,Zelda II: The Adventure of Link,3,Nintendo,4,112,1989,3.9911504424778763)
(280,Zelda, The Legend of,3,Nintendo,3,140,1986,3.0)
(281,Zombie Nation,4,Kaze,8,26,1991,7.851851851851852)
```

Now lets calculate the average rating given by users for each different rating given by the author of the website for all Nintendo games.

`gamedata_02.pig`
```
gamedata = LOAD 'nesgamedata.csv' AS (index:int, name:chararray, grade:int, publisher:chararray, reader_rating:int, number_of_votes:int, publish_year:int, total_grade:float);

gamesNintendo = FILTER gamedata BY publisher == 'Nintendo';

gamesRatings = GROUP gamesNintendo BY grade;

averaged = FOREACH gamesRatings GENERATE group as rating,
        AVG(gamesNintendo.total_grade) AS avgRating;

DUMP averaged;
```

Run the script on the Hadoop machine:
```shell
[root@quickstart gamedata]# pig -f gamedata_02.pig
...
(1,2.321279764175415)
(2,3.3024109601974487)
(3,3.7930258750915526)
(4,3.0212767124176025)
(5,5.381512546539307)
(6,5.773015689849854)
(7,6.020833492279053)
(8,9.833333015441895)
(9,6.624411582946777)
(10,8.105262756347656)
(12,8.070609092712402)
(13,10.066511631011963)
```
From this we can observe that on average the users do not really agree with the author on the ratings. Often the author gives higher grades to a game than the users.

