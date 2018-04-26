Title: Install Java version 8
Date: 2016-10-05 08:28
Modified: 2017-03-27 17:31
Category: posts
Tags: Java, Ubuntu
Slug: install-java-version-8
Authors: Jitse-Jan
Summary: I ran into an issue while re-configuring the Jira installation on my system. After an update Java 8 was needed but it is not present by default on Ubuntu 14.04. To install the JRE and JDK you need to add the repository of the webupd8team and use the Oracle Java 8 installer.

Install the common software-properties to be able to use the add-app-repository command.
 ``` shell
 jitsejan@jjsvps:~$ sudo apt-get install software-properties-common
 ```
 
 Add the Java repository to the Ubuntu sources.
 ``` shell
 jitsejan@jjsvps:~$ sudo add-apt-repository ppa:webupd8team/java
 ```
 
 Update the sources to retrieve the new Java repository.
 ``` shell
 jitsejan@jjsvps:~$ sudo apt-get update
 ```
 
 Install Java version 8.
 ``` shell
 jitsejan@jjsvps:~$ sudo apt-get install oracle-java8-installer
 ```