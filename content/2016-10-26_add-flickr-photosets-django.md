Title: Add Flickr photosets to a Django site
Date: 2016-10-05 08:24
Modified: 2017-03-27 17:34
Category: posts
Tags: Django, Python, Flickr
Slug: add-flickr-photosets-django
Authors: Jitse-Jan
Summary: A short description that describes how to retrieve pictures from Flickr and add them to a Django application using the __flickrapi__.

### 1. Set up connection
(Note that I just put a dummy key, secret and userid)

```python
import flickrapi
key = '123456789abcdefghijklmn'
secret = '123456a7890'
userid = '123456@N16'
flickr = flickrapi.FlickrAPI(key, secret)
```

### 2. Retrieve the photosets

```python
from lxml import etree
sets = flickr.photosets.getList(user_id=userid)
photoset = sets.findall(".//photoset")[0]
print etree.tostring(photoset)
```
will return
``` shell
<photoset id="72157674032173850" primary="30292011566" secret="c384c894ce" server="8552" farm="9" photos="31" videos="0" needs_interstitial="0" visibility_can_see_set="1" count_views="0" count_comments="0" can_comment="0" date_create="1476484376" date_update="1476488433">
    <title>Canada 2016</title>
    <description>Visit to Toronto, Montreal and the Falls.</description>
</photoset>
```

### 3. Connect to Django
Since I want to add to pictures from Flickr to my Django webpage, I need to connect to the database.

```python
import os, sys
project_path = '/opt/env/django_project/'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
sys.path.append(project_path)
```

### 4. Load the Photoset model
Now we set the path to be the Django path, we can import the models from my blog.

```python
import django
django.setup()
from blog.models import Photoset
for field in Photoset._meta.get_fields():
    print field
```
This will show the fields of the model.
``` shell
<ManyToOneRel: blog.photo>
blog.Photoset.id
blog.Photoset.flickr_id
blog.Photoset.secret
blog.Photoset.title
blog.Photoset.description
blog.Photoset.date_create
blog.Photoset.date_update
blog.Photoset.created
blog.Photoset.modified
```

### 5. Add Flickr photosets to Django

```python
if not Photoset.objects.filter(flickr_id=photoset.get('id')).exists():
    blog_photoset = Photoset()
    blog_photoset.flickr_id = photoset.get('id')
    blog_photoset.secret = photoset.get('secret')
    blog_photoset.title = photoset.find('title').text
    blog_photoset.description = photoset.find('description').text if photoset.find('description').text is 'null' else ""
    blog_photoset.date_create = photoset.get('date_create')
    blog_photoset.date_update = photoset.get('date_update')
    blog_photoset.save()
    print "Added photoset '%s' to database!" % (blog_photoset.title)
else:
    print "Photoset '%s' already in database!" % (photoset.find('title').text)
```
In my case the photoset has already been added.
``` shell
Photoset 'Canada 2016' already in database!
```

### 6. Retrieve photos from Flickr photoset

```python
for photo in flickr.walk_set(photoset.attrib['id']):
    photo_element = flickr.photos.getinfo(photo_id=photo.get('id')).find('./photo')
    print etree.tostring(photo_element)
    break # Just print one
```
This will return the XML object of a photo.
```xml
<photo id="30326779825" secret="78076b80de" server="8140" farm="9" dateuploaded="1476484428" isfavorite="0" license="0" safety_level="0" rotation="270" originalsecret="cb36a41988" originalformat="jpg" views="1" media="photo">
    <owner nsid="45832294@N06" username="jitsejan" realname="Jitse-Jan van Waterschoot" location="" iconserver="5495" iconfarm="6" path_alias="jitsejan"/>
    <title>Looking at the city</title>
    <description/>
    <visibility ispublic="1" isfriend="0" isfamily="0"/>
    <dates posted="1476484428" taken="2016-08-26 04:14:31" takengranularity="0" takenunknown="0" lastupdate="1476700149"/>
    <editability cancomment="0" canaddmeta="0"/>
    <publiceditability cancomment="1" canaddmeta="0"/>
    <usage candownload="1" canblog="0" canprint="0" canshare="1"/>
    <comments>0</comments>
    <notes/>
    <people haspeople="0"/>
    <tags/>
    <urls>
        <url type="photopage">https://www.flickr.com/photos/jitsejan/30326779825/</url>
       </urls>
</photo>
```    

### 7. Create URL for Flickr photo

```python
# url_template = "http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg" 
url = "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_z.jpg" % photo.attrib
print url
```
Resulting URL:
``` shell
http://farm9.staticflickr.com/8140/30326779825_78076b80de_z.jpg
```

### 8. Load the Photo model

```python
from blog.models import Photo
for field in Photo._meta.get_fields():
    print field
```
Above code will show the fields of the Photo model in Django.
``` shell
blog.Photo.id
blog.Photo.flickr_id
blog.Photo.title
blog.Photo.description
blog.Photo.date_posted
blog.Photo.date_taken
blog.Photo.url
blog.Photo.image_url
blog.Photo.created
blog.Photo.modified
blog.Photo.photoset
```

### 9. Add Flickr photo to Django

```python
blog_photo = Photo()
blog_photo.flickr_id = photo.get('id')
blog_photo.title = photo.get('title')
blog_photo.description = photo.get('description') if photoset.get('description') is 'null' else ""
blog_photo.date_posted = photo_element.find('dates').attrib['posted']
blog_photo.date_taken = photo_element.find('dates').attrib['taken']
blog_photo.url = photo_element.find('urls/url').text
blog_photo.image_url = url
try:
    blog_photo.photoset = blog_photoset
except:
    blog_photo.photoset = Photoset.objects.filter(flickr_id=photoset.get('id'))[0]
if not Photo.objects.filter(flickr_id=blog_photo.flickr_id).exists():
    blog_photo.save()
    print "Added photo '%s' to database!" % (blog_photo.title)
else:
    print "Photo '%s' already in database!" % (blog_photo.title)
```
Again, the item is already in the database in my case.
``` shell
Photo 'Looking at the city' already in database!
```