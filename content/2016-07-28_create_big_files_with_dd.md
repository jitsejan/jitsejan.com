Title: Create big files with dd
Date: 2016-07-28 10:45
Modified: 2017-03-26 16:57
Category: posts
Tags: shell
Slug: create-big-files-with-dd
Authors: Jitse-Jan
Summary:

Use dd in Unix to create files with a size of 2.7 GB.
``` shell
#!/bin/ksh
dir=/this/is/my/outputdir/
numGig=2.7
factor=1024
memLimit=$(expr $numGig*$factor*$factor*$factor | bc)
cd $dir
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 ; do
   dd if=/dev/urandom of=dummy_$i.xml count=204800 bs=$factor
done
```