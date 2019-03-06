Title: Creating Pandas dataframe from Azure Table Storage
Date: 2018-06-08 11:00
Modified: 2018-06-08 11:00
Category: posts
Tags: Python, pandas, Azure, dataframe, generator
Slug: creating-dataframe-from-table-storage
Authors: Jitse-Jan
Summary: 

```python
import pandas as pd
from azure.cosmosdb.table.tableservice import TableService

CONNECTION_STRING = "DUMMYSTRING"
SOURCE_TABLE = "DUMMYTABLE"

def set_table_service():
    """ Set the Azure Table Storage service """
    return TableService(connection_string=CONNECTION_STRING)

def get_dataframe_from_table_storage_table(table_service, filter_query):
    """ Create a dataframe from table storage data """
    return pd.DataFrame(get_data_from_table_storage_table(table_service,
                                                          filter_query))

def get_data_from_table_storage_table(table_service, filter_query):
    """ Retrieve data from Table Storage """
    for record in table_service.query_entities(
        SOURCE_TABLE, filter=filter_query
    ):
        yield record

fq = "PartitionKey eq '12345'"
ts = set_table_service()
df = get_dataframe_from_table_storage_table(table_service=ts,
                                            filter_query=fq)

```
