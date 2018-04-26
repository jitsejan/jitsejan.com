Title: Getting started with the Hortonworks Hadoop Sandbox
Date: 2017-09-01 12:16
Modified: 2017-09-01 12:16
Category: posts
Tags: Hadoop, Hortonworks, Docker, container, virtualization
Slug: getting-started-with-hortonworks-sandbox
Authors: Jitse-Jan
Summary: Using the Docker HDP image from [Hortonworks](https://hortonworks.com/downloads/#sandbox), it is easy to spin up an Hadoop environment onto your machine.

<center><img src="https://cdn.datafloq.com/vendor/logo/Hortonworks-logo.png" height=80/></center>

Download the HDP Docker image from Hortonworks.
```shell
jitsejan@ssdnodes-jj-kvm:~/downloads$ wget https://downloads-hortonworks.akamaized.net/sandbox-hdp-2.6.1/HDP_2_6_1_docker_image_28_07_2017_14_42_40.tar
```

Load the Docker image from the TAR-file.
```shell
jitsejan@ssdnodes-jj-kvm:~/downloads$ docker load -i HDP_2_6_1_docker_image_28_07_2017_14_42_40.tar
jitsejan@ssdnodes-jj-kvm:~/downloads$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
anaconda3docker_anaconda   latest              4faa1524bf2d        18 hours ago        3.397 GB
sandbox-hdp                latest              c3cef4760133        4 weeks ago         12.2 GB
continuumio/anaconda3      latest              f3a9cb1bc160        12 weeks ago        2.317 GB
```

Download and run the start-up script.
```shell
jitsejan@ssdnodes-jj-kvm:~/downloads$ wget https://raw.githubusercontent.com/hortonworks/data-tutorials/master/tutorials/hdp/sandbox-deployment-and-install-guide/assets/start_sandbox-hdp.sh
jitsejan@ssdnodes-jj-kvm:~/downloads$ chmod +x start_sandbox-hdp.sh
jitsejan@ssdnodes-jj-kvm:~/downloads$ ./start_sandbox-hdp.sh
```

Verify the container is started.
```shell
jitsejan@ssdnodes-jj-kvm:~/downloads$ docker ps
CONTAINER ID        IMAGE               COMMAND               CREATED             STATUS              PORTS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         NAMES
26bdf90de81b        sandbox-hdp         "/usr/sbin/sshd -D"   About an hour ago   Up About an hour    0.0.0.0:1000->1000/tcp, 0.0.0.0:1100->1100/tcp, 0.0.0.0:1220->1220/tcp, 0.0.0.0:1988->1988/tcp, 0.0.0.0:2049->2049/tcp, 0.0.0.0:2100->2100/tcp, 0.0.0.0:2181->2181/tcp, 0.0.0.0:3000->3000/tcp, 0.0.0.0:4040->4040/tcp, 0.0.0.0:4200->4200/tcp, 0.0.0.0:4242->4242/tcp, 0.0.0.0:5007->5007/tcp, 0.0.0.0:5011->5011/tcp, 0.0.0.0:6001->6001/tcp, 0.0.0.0:6003->6003/tcp, 0.0.0.0:6008->6008/tcp, 0.0.0.0:6080->6080/tcp, 0.0.0.0:6188->6188/tcp, 0.0.0.0:8000->8000/tcp, 0.0.0.0:8005->8005/tcp, 0.0.0.0:8020->8020/tcp, 0.0.0.0:8032->8032/tcp, 0.0.0.0:8040->8040/tcp, 0.0.0.0:8042->8042/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:8082->8082/tcp, 0.0.0.0:8086->8086/tcp, 0.0.0.0:8088->8088/tcp, 0.0.0.0:8090-8091->8090-8091/tcp, 0.0.0.0:8188->8188/tcp, 0.0.0.0:8443->8443/tcp, 0.0.0.0:8744->8744/tcp, 0.0.0.0:8765->8765/tcp, 0.0.0.0:8886->8886/tcp, 0.0.0.0:8888-8889->8888-8889/tcp, 0.0.0.0:8983->8983/tcp, 0.0.0.0:8993->8993/tcp, 0.0.0.0:9000->9000/tcp, 0.0.0.0:9995-9996->9995-9996/tcp, 0.0.0.0:10000-10001->10000-10001/tcp, 0.0.0.0:10015-10016->10015-10016/tcp, 0.0.0.0:10500->10500/tcp, 0.0.0.0:10502->10502/tcp, 0.0.0.0:11000->11000/tcp, 0.0.0.0:15000->15000/tcp, 0.0.0.0:15002->15002/tcp, 0.0.0.0:15500-15505->15500-15505/tcp, 0.0.0.0:16000->16000/tcp, 0.0.0.0:16010->16010/tcp, 0.0.0.0:16020->16020/tcp, 0.0.0.0:16030->16030/tcp, 0.0.0.0:18080-18081->18080-18081/tcp, 0.0.0.0:19888->19888/tcp, 0.0.0.0:21000->21000/tcp, 0.0.0.0:33553->33553/tcp, 0.0.0.0:39419->39419/tcp, 0.0.0.0:42111->42111/tcp, 0.0.0.0:50070->50070/tcp, 0.0.0.0:50075->50075/tcp, 0.0.0.0:50079->50079/tcp, 0.0.0.0:50095->50095/tcp, 0.0.0.0:50111->50111/tcp, 0.0.0.0:60000->60000/tcp, 0.0.0.0:60080->60080/tcp, 0.0.0.0:2222->22/tcp, 0.0.0.0:1111->111/tcp   sandbox-hdp
```

Login to the machine and run the first Hadoop command.
```shell
jitsejan@ssdnodes-jj-kvm:~/downloads$ ssh 127.0.0.1 -p 2222 -l maria_dev
[maria_dev@sandbox ~]$ hadoop fs -ls
Found 2 items
drwxr-xr-x   - maria_dev hdfs          0 2017-09-01 09:29 .Trash
drwxr-xr-x   - maria_dev hdfs          0 2017-09-01 08:16 hive
```