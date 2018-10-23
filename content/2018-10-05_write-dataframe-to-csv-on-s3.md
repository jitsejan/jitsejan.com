Title: Write a Pandas dataframe to CSV on S3
Date: 2018-10-05-11:00
Modified: 2018-10-05-11:00
Category: posts
Tags: Python, pandas, CSV, dataframe, AWS, S3
Slug: write-dataframe-to-csv-on-s3
Authors: Jitse-Jan
Summary: 

Write a `pandas` dataframe to a single CSV file on S3.

```python
import boto3
from io import StringIO

DESTINATION = 'my-bucket'

def _write_dataframe_to_csv_on_s3(dataframe, filename):
    """ Write a dataframe to a CSV on S3 """
    print("Writing {} records to {}".format(len(dataframe), filename))
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep="|", index=False)
    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(DESTINATION, filename).put(Body=csv_buffer.getvalue())

_write_dataframe_to_csv_on_s3(my_df, 'my-folder')
```

[Gist](https://gist.github.com/jitsejan/e24c6f9b288a839f40edd1ce944a747e)