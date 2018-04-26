Title: Write dictionary to CSV in Python
Date: 2016-10-05 08:24
Modified: 2017-03-27 17:36
Category: posts
Tags: dictionary, CSV, Python,
Slug: write-dictionary-to-csv-python
Authors: Jitse-Jan
Summary: 

``` python
import csv

def write_dictionary_to_csv(o_file, d):
    """ Write dictionary to output file """
    with open(o_file, 'wb') as csvfile:
        outputwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        outputwriter.writerow(d.keys())
        outputwriter.writerows(zip(*d.values()))

dictionary = {"key1": [12,23,34],
              "key2": [45,56,67],
              "key3": [78,89,90]}
output_file = 'output.csv'
write_dictionary_to_csv(output_file, dictionary)
```