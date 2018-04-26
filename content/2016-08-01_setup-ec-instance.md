Title: Setting up an AWS EC instance
Date: 2016-08-01 09:33
Modified: 2017-03-27 14:43
Category: posts
Tags: Amazon, EC, VPS
Slug: setup-ec-instance
Authors: Jitse-Jan
Summary: A short description of how to set up an instance at AWS EC

* Go to the [EC page](https://eu-central-1.console.aws.amazon.com/ec2/v2/home?region=eu-central-1#Instances:sort=instanceId)
* Launch Instance
* Select **Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - ami-87564feb**
* Select **t2.micro (Free tier eligible)**
* Select **Next: Configure Instance Details**
* Select **Next: Add Storage**
* Select **Next: Tag Instance**
* Give a _Name_ to the Instance
* Select **Next: Configure Security Group**
* Create a new security group
* Add a _Security group name_
* Add a _Description_
* Add rule by clicking **Add Rule**
* First rule should be **Custom TCP Rule, TCP Protocol, Port 80 for source Anywhere**
* Click on **Launch**
* Select **Review and launch**
* In the pop-up, select **Create a new key pair**
* Fill in a _Key pair name_
* Download the _Key Pair_ and save in a <u>secure</u> location
* Go to the [instance page](https://eu-central-1.console.aws.amazon.com/ec2/v2/home?region=eu-central-1#Instances:sort=instanceId) and wait until the machine is ready

* On your computer, change the permissions of the key pair you just downloaded
``` shell
      $ chmod 400 keypairfile.pem
```
* Connect to the machine via ssh. Click on the Connect button in the instance overview for connection information
``` shell
      $ ssh -i keypairfile.pem ec2-xx-xx-x-xx.eu-central-1.compute.amazonaws.com
```