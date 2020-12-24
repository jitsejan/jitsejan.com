Title: Scraping data based on xpaths
Date: 2020-12-24 20:02
Modified: 2020-12-24 20:02
Category: posts
Tags: Python, scraping, xpath, requests
Slug: scraping-with-xpaths
Authors: Jitse-Jan
Summary: A quick example on how to use xpaths to find values in a website based on certain elements. TLDR: `"//tr[th//text()[contains(., 'Cost(s)')]]/td"` will find the `td` where the `th` of the same row contains the text _Costs(s)_.

For a small project I need to retrieve the cost of an item from the following HTML syntax:

```html
<table>
    <tr>
        <th>Name</th>
        <td>Boomerang</td>
    </tr>
    <tr>
        <th>Cost(s)</th>
        <td>300</td>
    </tr>
    <tr>
        <th>Description</th>
        <td>A wonderful boomerang</td>
    </tr>
</table>
```

It is difficult to get to this item because not every page has the same table, and not every table has the cost mentioned. The goal is to retrieve both the `name` and the `price` of an item. To keep things tidy I will use a `dataclass` for the items. Here I can define that the name will be a string and the price an integer as well as overwrite the print function for a single item.

```python
@dataclass(frozen=True)
class Item:
    name: str
    price: int
        
    def __repr__(self):
        return (f'{self.__class__.__name__}'
            f'(name={self.name}, price={self.price})')
```

I am crawling data from https://zelda.gamepedia.com since it has a very complete overview of all the Zelda data. I use a simple function to get the XML tree from the page source using `requests` with `lxml.html`. `BeautifulSoup` and other fancy packages would work too but I like to stick to more basic libraries for simplicity.

```python
import lxml.html
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}
session = requests.Session()
session.headers = HEADERS

def _get_tree_from_url(url: str) -> lxml.html.etree:
    resp = session.get(url)
    return lxml.html.fromstring(resp.text)
```

The links to all the items are inside the `gallerybox` div and are easy to retrieve using `cssselect`. The following function is a generator that returns the links to all items mentioned on the Legend of Zelda page.

```python
def _get_item_links() -> Iterator[str]:
    items_url = f"{BASE_URL}/Items_in_The_Legend_of_Zelda"
    tree = _get_tree_from_url(items_url)
    for elem in tree.cssselect("li.gallerybox .gallerytext p a"):
        yield f"{BASE_URL}{elem.attrib['href'].split('#')[0]}"
```

The next bit takes care of finding the right row in the table to retrieve the price and the name of the item. The **name** is retrieved from the `meta` tag with the `og:title` property by getting the `content` attribute. I wrote it with `cssselect` but this could easily be rewritten as xpath with `"//meta[@property='og:title']/@content"`. The more tricky part is to find the cell of the table where the header of the row contains a certain text. For the xpath you will need to find the `tr` for which the table header `contains()` a certain string and return the text of the div inside the cell.

```python
def get_item_details(link: str) -> Item:
    tree = _get_tree_from_url(link)
    try:
        name = tree.cssselect("meta[property='og:title']")[0].attrib['content']
        price = int(tree.xpath("//tr[th//text()[contains(., 'Cost(s)')]]/td/div")[0].text)
        return Item(name, price)
    except:
        pass # No price for this item
```

Putting it all together:

```python
from dataclasses import dataclass
import lxml.html
import requests
from typing import Iterator

BASE_URL = "https://zelda.gamepedia.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

@dataclass(frozen=True)
class Item:
    name: str
    price: int
        
    def __repr__(self):
        return (f'{self.__class__.__name__}'
            f'(name={self.name}, price={self.price})')


def _get_tree_from_url(url: str) -> lxml.html.etree:
    resp = session.get(url)
    return lxml.html.fromstring(resp.text)

def get_item_links() -> Iterator[str]:
    items_url = f"{BASE_URL}/Items_in_The_Legend_of_Zelda"
    tree = _get_tree_from_url(items_url)
    for elem in tree.cssselect("li.gallerybox .gallerytext p a"):
        yield f"{BASE_URL}{elem.attrib['href'].split('#')[0]}"

def get_item_details(link: str) -> Item:
    tree = _get_tree_from_url(link)
    try:
        name = tree.cssselect("meta[property='og:title']")[0].attrib['content']
        price = int(tree.xpath("//tr[th//text()[contains(., 'Cost(s)')]]/td/div")[0].text)
        return Item(name, price)
    except:
        pass # No price for this item

session = requests.Session()
session.headers = HEADERS
items = []
for link in get_item_links():
    item_data = get_item_details(link)
    (items.append(item_data) if item_data is not None else None)

items.sort(key=lambda x: x.price, reverse=True)
print(items)
# [Item(name=Bow, price=980), Item(name=Boomerang, price=300), Item(name=Blue Ring, price=250), Item(name=Arrow, price=80), Item(name=Red Water of Life, price=68), Item(name=Blue Candle, price=60), Item(name=Food, price=60), Item(name=Blue Water of Life, price=40), Item(name=Bomb, price=20), Item(name=Heart Container, price=4)]
```