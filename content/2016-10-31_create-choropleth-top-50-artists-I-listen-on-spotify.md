Title: Create a choropleth for the top 50 artists I listen on Spotify
Date: 2016-10-31 23:31
Modified: 2017-03-27 17:38
Category: posts
Tags: visualization, Spotify, Python, pandas, choropleth
Slug: create-choropleth-top-50-artists-I-listen-on-spotify
Authors: Jitse-Jan
Summary: In this post I will try to make a world map to indicate where the 50 artists I listen to most on Spotify are from. This will be my first personal data science project, so bare with me. My expectation is that the majority will be in either the UK (indie bands), the US or from South-Korea (K-pop). Lets see if my hypothesis is true.

```python
# Import the settings for the notebooks
from notebooksettings import GRACENOTE_USERID, SPOTIFY_USERNAME
```

### 1. Connect to Spotify
I will use the [Spotipy](https://github.com/plamere/spotipy) library to connect to Spotify. Both reading the library and reading the top tracks will be enabled by setting the scope appropriately.


```python
import sys
import spotipy
import spotipy.util as util

# Set scope to read the library and read the top tracks
scope = 'user-library-read user-top-read'
username = SPOTIFY_USERNAME
token = util.prompt_for_user_token(username, scope)
```

### 2. Retrieve songs from Spotify
After creating a token, you can make a new Spotipy instance and connect to your account. Lets retrieve the top 50 of artists of my account and add the artists to a list.


```python
LIMIT = 50
OFFSET = 0
artists = {}
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_artists(limit=LIMIT, offset=OFFSET)
    for artist in results['items']:
        artist_id = artist['id']
        artists[artist_id] = sp.artist(artist_id)['name']
else:
    print "Can't get token for", username
```

### 3. Create a placeholder for the country mapping
To create a choropleth, I will create a list of countries using the [Pycountry](https://pypi.python.org/pypi/pycountry) library. The country data will contain the name, the three character long abbreviation, the number of occurrences of the country for the different artists and a list of artists.


```python
import pycountry
country_data = []
for cnt in pycountry.countries:
    country_data.append([cnt.name, cnt.alpha3, 0, []])
```

### 4. Create a mapping for the country name to country abbreviation
To map the country name to a three character abbreviation, we need to make a mapping linking the two together.


```python
mapping = {country.name: country.alpha3 for country in pycountry.countries}
```

### 5. Retrieve the country of origin for the artists
To find the country of origin, I will make use of the [pygn](https://github.com/cweichen/pygn) library to connect to [Gracenote](https://www.gracenote.com) and find metadata for music.

First I create a connection with pygn so I can retrieve the metadata from the Gracenote servers. Next I will find the country and map it to the right abbreviation. Finally I will increase the counter in the country data for the corresponding country and add the artist to the list.


```python
import pygn
clientID = GRACENOTE_USERID
userID = pygn.register(clientID)
for artist_name in artists.values():
    # Retrieve metadata
    metadata = pygn.search(clientID=clientID, userID=userID, artist=artist_name)
    if '2' in metadata['artist_origin'].keys():
        country = metadata['artist_origin']['2']['TEXT']
    elif len(metadata['artist_origin'].keys()) == 0:
        country = None
    else:
        country = metadata['artist_origin']['1']['TEXT']
    # Replace names
    if country == 'South Korea':
        country = 'Korea, Republic of'
    if country == 'North Korea':
        country = "Korea, Democratic People's Republic of"
    # Retrieve the mapping
    country_code = mapping.get(country, 'No country found')
    # Increase the counter for corresponding country
    for index, cnt_entry in enumerate(country_data):
        if cnt_entry[1] == country_code:
            country_data[index][2]+=1
            country_data[index][3].append(artist_name)
```

### 6. Create a dataframe from the data
Using [Pandas](http://pandas.pydata.org) we will now create a DataFrame to convert the data from the country data to a Pandas format.


```python
import pandas as pd
df = pd.DataFrame(country_data, columns=['Country name', 'Code', 'Amount', 'Artists'])
df.head()
```

### 7. Create a choropleth from the data
Using [Plotly](https://plot.ly) we can easily make a [choropleth](https://en.wikipedia.org/wiki/Choropleth_map) for the data that we just retrieved. In the data settings you indicate the type is a choropleth graph, the locations can be found in the 'Code' column and the important data is the column 'Amount'. Next we set the colors and a title and we are good to go.


```python
import plotly.plotly as py
from plotly.graph_objs import *
data = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        z = df['Amount'],
        text = df['Country name'],
        colorscale = [[0,"rgb(0, 228, 97)"], 
                      [0.35,"rgb(70, 232, 117)"],
                      [0.5,"rgb(100, 236, 138)"],
                      [0.6,"rgb(120, 240, 172)"],
                      [0.7,"rgb(140, 245, 201)"],
                      [1,"rgb(250, 250, 250)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            )
        ),
        tick0 = 0,
        zmin = 0,
        dtick = 1000,
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Number of artists'
        ),
    ) ]

layout = dict(
    title = "Countries of origin of artists I listen on Spotify",
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)
figure = dict(data=data, layout=layout)
py.iplot(figure, validate=False)
```

<iframe width="500" height="400" frameborder="0" scrolling="no" src="//plot.ly/~jitsejan/68.embed"> </iframe>

### 8. Conclusion
As we can see in the graph above, the hypothesis is not completely true. The majority is still from the States.

### 9. Extra
Looking at the same type of graph for the top 50 tracks on Spotify, ignoring artist that are double, I retrieve the following graph.

<iframe width="500" height="400" frameborder="0" scrolling="no" src="//plot.ly/~jitsejan/50.embed"> </iframe>

In this graph it is slightly more evident that lately I listened to too much K-pop.