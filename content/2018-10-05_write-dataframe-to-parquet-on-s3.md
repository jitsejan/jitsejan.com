Title: Write a Pandas dataframe to Parquet on S3
Date: 2018-10-05-11:00
Modified: 2018-10-05-11:00
Category: posts
Tags: Python, pandas, Parquet, dataframe, AWS, S3
Slug: write-dataframe-to-parquet-on-s3
Authors: Jitse-Jan
Summary: 

Write a `pandas` dataframe to a single Parquet file on S3.

```python
# Note: make sure `s3fs` is installed in order to make Pandas use S3.
#       Credentials for AWS in the normal location ~/.aws/credentials
DESTINATION = 'my-bucket'

def _write_dataframe_to_parquet_on_s3(dataframe, filename):
    """ Write a dataframe to a Parquet on S3 """
    print("Writing {} records to {}".format(len(dataframe), filename))
    output_file = f"s3://{DESTINATION}/{filename}/data.parquet"
    dataframe.to_parquet(output_file)

_write_dataframe_to_parquet_on_s3(my_df, 'my-folder')
```

[Gist](https://gist.github.com/jitsejan/557124bcbaf0780ab4efc6054199550a)