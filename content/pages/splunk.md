Title: Splunk cheatsheet
Date: 2017-03-26 16:48
Modified: 2017-03-26 16:48
Category: splunk
Tags: splunk, cheatsheet
Slug: splunk-cheatsheet
Authors: Jitse-Jan
Summary: This is my Splunk cheatsheet

This is my [Splunk](https://www.splunk.com/) cheatsheet.

### Replace single quote with double quote
```
| rex mode=sed "s/\'/\"/g" field=myfield
```
### Extract JSON data from an JSON array
The following will try to find ten matches for strings contained in curly brackets. Next it will be expanded to a multi value field so we can use _spath_ on each extracted field.
```
| rex max_match=10 "(?<json_field>{[^}]+})" field=myjsonarrayfield
| mvexpand json_field
| spath input=json_field 
| rename field_in_json_field AS field
```

### Drilldown of areachart
``` xml
<drilldown>
    <set token="form.character">$click.name2$</set>
</drilldown>
```

### Create a range between limits
``` 
| eval range_field = mvrange(start, end, step) 
| mvexpand range_field 
| stats count by range_field
```

### Frequency of Splunk restarts
```
index=_internal "Splunkd starting" | timechart span=1d count(_raw) as Event
```
