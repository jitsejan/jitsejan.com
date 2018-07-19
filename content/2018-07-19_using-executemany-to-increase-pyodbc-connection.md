Title: Using executemany to increase PyODBC connection
Date: 2018-07-19 16:13
Modified: 2018-07-19 16:13
Category: posts
Tags: Python, pandas, Azure, dataframe, PyODBC, 
Slug: using-executemany-to-increase-pyodbc-connection
Authors: Jitse-Jan
Summary: 

I recently had to insert data from a Pandas dataframe into a Azure SQL database using `pandas.to_sql()`. This was performing very poorly and seemed to take ages, but since  PyODBC introduced [executemany](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany) it is easy to improve the performance: simply add an event listener that activates the `executemany` for the cursor. For 2300 records I did a small comparison 8.67s and 7.22s versus 5min 57s and 5min 26s, so roughly 50 times faster for this small example dataset.


```python
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool

wh_conn = pyodbc.connect(f"DRIVER={config[name]['driver']};SERVER={config[name]['server']},{config[name]['port']};DATABASE={config[name]['database']};UID={config[name]['username']};PWD={config[name]['password']}")
engine = create_engine("mssql+pyodbc://", poolclass=StaticPool, creator=lambda: wh_conn)

@event.listens_for(engine, 'before_cursor_execute')
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True
        
df.to_sql(name='Table',
          con=engine,
          schema='Schema',
          index=False,
          if_exists='replace')
```
