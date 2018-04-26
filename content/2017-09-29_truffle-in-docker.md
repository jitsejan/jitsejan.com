Title: Running Truffle in a Docker container
Date: 2017-09-29 16:17
Modified: 2017-10-11 21:17
Category: posts
Tags: Truffle, Docker, container, dapp, Ethereum, blockchain
Slug: truffle-in-docker
Authors: Jitse-Jan
Summary: This is a short explanation on how to setup a Truffle decentralized app using Docker containers.

<style>
img.header{
  height:100px;
  width:100px;
}
</style>
<center>
<img class="header" src="http://files.jitsejan.com/logos/truffle.PNG" />
<img class="header" src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Tab_plus.svg/2000px-Tab_plus.svg.png" />
<img class="header" src="http://files.jitsejan.com/logos/docker.PNG" />
</center>
## Introduction
In my [earlier post](http://www.jitsejan.com/creating-dapp-with-truffle-and-metamask.html) about creating a decentralized application using Truffle and Metamask I used my own machine to install all dependencies and start developing. Since I am switching to Docker for most of my projects because of the flexibility, reproducability and safety of containerized environments, I also convert the Truffle project to Docker. As an inspiration I studied the [example](https://github.com/dougvk/truffle3-frontend-example) made by Douglas von Kohorn.

## Docker
### Docker installation
Make sure Docker and docker-compose are installed on the machine.
```bash
jitsejan@ssdnodes-jj-kvm:~$ sudo apt-get install docker.io docker-compose
jitsejan@ssdnodes-jj-kvm:~$ docker -v
Docker version 1.12.6, build 78d1802
jitsejan@ssdnodes-jj-kvm:~$ docker-compose -v
docker-compose version 1.8.0, build unknown
```
### TestRPC image
First of all, we need to setup a test network to play around with the Truffle app that we are going to create. Since we do not want to use the official Ethereum blockchain network, we use `testrpc` as created by Tim Coulter. See [Github](https://github.com/ethereumjs/testrpc) for the official repository.
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/testrpc$ nano Dockerfile 
```
The Dockerfile contains the few steps that are needed to create the TestRPC image. It will retrieve the Linux distro with node installed, install the node module `ethereumjs-testrpc` and open up port 8545, which is the default port for testrpc.
```bash
# Node image
FROM node:latest
# Maintainer
MAINTAINER Jitse-Jan van Waterschoot <jitsejan@gmail.com>
# Install the packages
RUN npm install -g --save ethereumjs-testrpc
# Expose port
EXPOSE 8545
# Start TestRPC
ENTRYPOINT ["testrpc"]
```
From the Dockerfile we will create the image on the local machine and push it to Docker.io.
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/testrpc$ docker build . -t jitsejan/testrpc
jitsejan@ssdnodes-jj-kvm:~/docker/testrpc$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you dont have a Docker ID, head over to https://hub.docker.com to create one.
Username (jitsejan): 
Password: 
Login Succeeded
jitsejan@ssdnodes-jj-kvm:~/docker/testrpc$ docker push jitsejan/testrpc
jitsejan@ssdnodes-jj-kvm:~/docker/testrpc$ docker images | grep testrpc
jitsejan/testrpc               latest              a5cae5578720        10 minutes ago      716 MB
```
The image can now be found at [hub.docker.com](https://hub.docker.com/r/jitsejan/testrpc/).

### Truffle image
Next we need to create the environment where we can develop our Truffle application. We will use again a Dockerfile, but in this case we will install `truffle`.

```bash
# Node image
FROM node:latest
# Maintainer
MAINTAINER Jitse-Jan van Waterschoot <jitsejan@gmail.com>
# Create code directory
RUN mkdir /code
# Set working directory
WORKDIR /code
# Install Truffle
RUN npm install -g truffle
```
We can build and push the image again, finally the image will be available locally to be used by Docker. Again I use the docker push to add the image to my [hub.docker.com](https://hub.docker.com/r/jitsejan/truffle-application/
).
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ docker images | grep truffle-application
jitsejan/truffle-application   latest              1987e7928f6b        58 minutes ago      693.3 MB
```

### Docker compose
The `docker-compose.yml` contains the information to start the two images, map the ports and start the testrpc network. It will try to retrieve the two Docker images locally and otherwise retrieve them from hub.docker.com. The testrpc is started with host 0.0.0.0 in order for the truffle3 container to access the network.
```yaml
version: '2'
services:
  testrpc:
    image: jitsejan/testrpc
    command: bash -c "testrpc -h 0.0.0.0"
    ports:
      - "7000:8545"
  truffle3:
    image: jitsejan/truffle-application
    command: bash
    stdin_open: true
    tty: true
    ports:
      - "7001:8080"
    volumes:
      - ./:/code
```
### Docker start
Once the docker-compose.yml is in place, we can start the testrpc and truffle3 container by running the following command:
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ docker-compose -f docker-compose.yml up -d
```
and verify if both containers are running:
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ docker ps
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS                    NAMES
cda7d1c5c2a0        jitsejan/truffle-application   "bash"                   6 minutes ago       Up About a minute   0.0.0.0:7001->8080/tcp   truffleapplication_truffle3_1
36f0bf0d4d25        jitsejan/testrpc               "testrpc bash -c 'tes"   9 minutes ago       Up About a minute   0.0.0.0:7000->8545/tcp   truffleapplication_testrpc_1
```
## Creating the app
Now we connect to the Truffle machine and create the application.
### Versions of the tools
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ docker attach truffleapplication_truffle3_1 
root@cda7d1c5c2a0:/code# npm -v
5.3.0
root@cda7d1c5c2a0:/code# node -v
v8.4.0
root@cda7d1c5c2a0:/code# truffle version
Truffle v3.4.11 (core: 3.4.11)
Solidity v0.4.15 (solc-js)
```
### Initialize a Truffle application
Use the unbox function of Truffle to create a sample webpack application.
```bash
root@cda7d1c5c2a0:/code# truffle unbox webpack
root@cda7d1c5c2a0:/code# ls
Dockerfile  box-img-lg.png  contracts           migrations    package-lock.json  test                truffle.js
app         box-img-sm.png  docker-compose.yml  node_modules  package.json       tmp-276YgmHxiGG8WL  webpack.config.js
```
Compile the contracts and migrate them to the network.
```bash
root@cda7d1c5c2a0:/code# truffle compile
Compiling ./contracts/ConvertLib.sol...
Compiling ./contracts/MetaCoin.sol...
Compiling ./contracts/Migrations.sol...
Writing artifacts to ./build/contracts
root@cda7d1c5c2a0:/code# truffle migrate
Could not connect to your Ethereum client. Please check that your Ethereum client:
    - is running
    - is accepting RPC connections (i.e., "--rpc" option is used in geth)
    - is accessible over the network
    - is properly configured in your Truffle configuration file (truffle.js)
```
In order to be able to migrate, we need to modify `truffle.js`. It is easier to change this is on the host machine instead of the Docker machine, since most probably there is a text editor available.
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ ls
app             box-img-sm.png  contracts           Dockerfile  node_modules  package-lock.json  tmp-276YgmHxiGG8WL  webpack.config.js
box-img-lg.png  build           docker-compose.yml  migrations  package.json  test               truffle.js
```
Lets edit the truffle.js and update the network settings.
```
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ sudo nano truffle.js 
```
Change the host from localhost to testrpc, since that is the name we assigned in our Docker setup.
```javascript
// Allows us to use ES6 in our migrations and tests.
require('babel-register')

module.exports = {
  networks: {
    development: {
      host: 'testrpc',
      port: 8545,
      network_id: '*' // Match any network id
    }
  }
}
```
With the updated network settings, lets try to migrate the contracts again to the network.
```shell
root@cda7d1c5c2a0:/code# truffle migrate
Using network 'development'.

Running migration: 1_initial_migration.js
  Deploying Migrations...
  ... 0x14946649e8489d36a12a5bbaeb61a306b6e2e52c9f33ff4d56d40f6f1472640c
  Migrations: 0x32e2f019bbdea7786e9b1d1c577f14bac8693464
Saving successful migration to network...
  ... 0x16bfd6088ce282fa7859de9b347e3cdefc3536ad987b6c0dbe12c37dda31be57
Saving artifacts...
Running migration: 2_deploy_contracts.js
  Deploying ConvertLib...
  ... 0xba333153ec8f1e5c0d51455d4dbf58e50e8cd20f9a1b7176dd846fce24aa336c
  ConvertLib: 0x97063aa24f9913c98c76f93f64d30a2d5475a7df
  Linking ConvertLib to MetaCoin
  Deploying MetaCoin...
  ... 0xa11480d9333044537a8a0e1798f6afa33ad74a80f739982e55bf02ae6a3915f2
  MetaCoin: 0x749764ff660f2572405f3a1674488077666b866a
Saving successful migration to network...
  ... 0x6d837a4071eb419f31fe055f0278889382af9fc010552ced0d8060f584054835
Saving artifacts...
```
Now we need to build and deploy the application.
```shell
root@cda7d1c5c2a0:/code# npm run build
root@cda7d1c5c2a0:/code# npm run dev
```
This will output that the application is running on localhost:8080, but visiting this link shows an error. We need to modify the settings for webpack and add the host for the development server. Change package.json 
```shell
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ sudo nano package.json 
```
and change the following line
```json
    "dev": "webpack-dev-server"
```
to
```json
    "dev": "webpack-dev-server --host 0.0.0.0"
```
to make the server accept external traffic. Run again 
```bash
root@d546db65c693:/code# npm run dev
```
and now the application is served on http://0.0.0.0:8080/. Visit the IP of the machine on which you are developing on port 7001 (remember we mapped the port from 8080 to 7001 in the docker-compose file) and the MetaCoin application should be visible. However, an error pops up.

```
There was an error fetching your accounts.
```
Why? Because the Truffle app cannot connect to the Ethereum test network yet. In order for the connection to work, we need to modify the code of the app.js inside the Truffle application and change the IP for the Web3 client to the external IP, and the port to 7000 since we mapped port 8545 to 7000 in docker-compose. Open the app.js with nano
```bash
jitsejan@ssdnodes-jj-kvm:~/docker/truffle-application$ sudo nano app/javascripts/app.js 
```
and change the line
```bash
window.web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
```
to
```bash
window.web3 = new Web3(new Web3.providers.HttpProvider("http://EXTERNAL_IP:7000"));
```
replacing the EXTERNAL_IP with the IP of the development machine where the Docker container with testrpc is running. Again run 
```bash
root@d546db65c693:/code# npm run dev
```
and this time no error should pop up when the page is visited. If everything went find you should see the MetaCoin application with 10000 META.

Hopefully this can serve as a base to create your own Dapp using Truffle.

My final code can be found on my [Github](https://github.com/jitsejan/truffle-application). 
