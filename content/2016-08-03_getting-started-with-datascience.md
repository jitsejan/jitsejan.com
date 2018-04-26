Title: Getting started with data science in Python
Date: 2016-08-03 14:55
Modified: 2017-03-27 14:50
Category: posts
Tags: anaconda, datascience, pandas, seaborn
Slug: getting-started-with-datascience
Authors: Jitse-Jan
Summary: A short summary of my first attempts to start with data science.

#### Installation
Use the [Anaconda](https://www.continuum.io/downloads "Anaconda") package. It will make starting with Data Science way easier, since almost all necessary packages are included and you can start right away.
``` shell
$ cd ~/Downloads
$ wget http://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh
$ bash Anaconda2-4.1.1-Linux-x86_64.sh
$ source ~/.bashrc
$ conda --version
$ conda update conda
```

#### Examples
##### Make your first Data Frame
``` python
#!/usr/bin/env python
import pandas as pd

df = pd.DataFrame({ 'A' : 1.,
                    'B' : pd.Timestamp('20130102'),
                    'C' : pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D' : pd.Series([1, 2, 1, 2], dtype='int32'),
                    'E' : pd.Categorical(["test", "train", "test", "train"]),
                    'F' : 'foo' })

df.groupby('E').sum().D
```

##### Create your first plots
First update Seaborn
``` shell
$ conda install seaborn
```
Next, create a plot of an example dataset
``` python
#!/usr/bin/env python
import seaborn as sns

# Load one of the data sets that come with seaborn
tips = sns.load_dataset("tips")
tips.head()

sns.jointplot("total_bill", "tip", tips, kind='reg');
sns.lmplot("total_bill", "tip", tips, col="smoker");
```

[Source](http://twiecki.github.io/blog/2014/11/18/python-for-data-science/ "Twiecki@Github")