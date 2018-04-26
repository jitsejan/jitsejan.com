Title: Pandas cheatsheet
Date: 2017-03-26 16:47
Modified: 2017-03-26 16:47
Category: pandas
Tags: pandas, cheatsheet
Slug: pandas-cheatsheet
Authors: Jitse-Jan
Summary: This is my Pandas cheatsheet

This is my [Pandas](http://pandas.pydata.org) cheatsheet. 

Note that I import pandas the 'standard' way:
``` python
import pandas as pd
```
## Convert with dataframes
### Create dataframe from a dictionary
``` python
character_df = pd.DataFrame.from_dict(characters)
```

### Create dictionary from dataframe
``` python
characters = character_df.to_dict(orient='records')
```

### Convert CSV to dataframe
``` python
character_df = pd.DataFrame.from_csv("characters.csv", sep='\t', encoding='utf-8')
```

### Convert dataframe to CSV
``` python
character_df.to_csv('characters.csv', sep='\t', encoding='utf-8')
```

### Convert database query to dataframe
``` python
db = create_engine('postgresql://%s:%s@%s:%d/characters' % (POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT))
character_df = pd.read_sql_query('SELECT * FROM "character_collection"', con=db)
```

## Cleaning dataframes
### Replace in column
``` python
character_df['name'] = character_df['name'].str.replace('-', ' ')
```
### Regex replace in whole dataframe
``` python
character_df.replace(r'-',r' ', regex=True, inplace=True)
```
### Regex extract in column
``` python
character_df['introduction_year'] = character_df['date_of_introduction'].str.extract('(\d{4})-..-..', expand=True)
```
### Remove all Not-a-Numbers
``` python
character_df = character_df.replace({'NaN': None}, regex=True)
```
### Rename a column
``` python
character_df.rename(columns={'name': 'character_name'}, inplace=True)
```
### Drop a column
``` python
character_df = character_df.drop('origin', axis=1)
```
### Drop a row
Drop all rows where the name is NaN.
``` python
character_df.dropna(subset = ['name'], inplace=True)
```

### Delete a column
``` python
del character_df['special_diet']
```
### Convert to integer
``` python
character_df['introduction_year'] = character_df['introduction_year'].fillna(-1).astype('int64')
```
### Convert to category
``` python
character_df['superpower'] = character_df['superpower'].astype('category')
```

### Convert string to list
``` python
# Convert a string with surrounding brackets and quotes to a list
def convert_string_to_list(column):
    """ Convert unicode string to list """
    return column.str.strip('{}').astype(str).apply(lambda x: x.split(',')[0].strip("\"") if len(x) > 0 else "")
character_df['superpowers'] = convert_string_to_list(character_df['superpowers'])
```

### Create column from index
``` python
character_df.index.names = ['Name']
character_df = character_df.reset_index()
```

### Extend dictionary cell to columns
``` python
df = pd.concat([df.drop(['meta'], axis=1), df['meta'].apply(pd.Series)], axis=1)
```

## Find data
### Describe the data
``` python
character_df['age'].describe()
```
### Unique values
``` python
characters = character_df['character_name'].unique()
```

### Field contains
``` python
character_df[character_df['name'].str.contains("Koopa").fillna(False)]
```

### Count by
``` python
character_df.groupby(['superpowers']).count()
```

### Loop through data
``` python
for element in character_df.index:
    superpower = character_df.iloc[element]['superpower']
    if not pd.isnull(superpower):
       print 'Super!'
```

### Substract 
Substract two consecutive cells
``` python
df['difference'] = df['amount'] - df['amount'].shift(+1)
```

### Add a maximum column for a groupby
``` python
df['group_maximum'] = df.groupby(['category'])['score'].transform(max)
```

### Create category based on values
``` python
def set_category(row):
    if row['score'] < float(row['maximum']/3):
        return 'beginner'
    elif row['score'] >= float(row['maximum']/3*2):
        return 'expert' 
    else:
        return 'intermediate'

df['category'] = df.apply(set_category, axis=1)
```

### Apply lambda function
``` python
df['inverse_number'] = df['number'].apply(lambda x: x**(-1))
``` 

