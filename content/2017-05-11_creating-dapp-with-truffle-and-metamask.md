Title: Setting up a Dapp with Truffle and Metamask
Date: 2017-05-11 23:09
Modified: 2017-05-11 23:09
Category: posts
Tags: ether, ethereum, Truffle, Metamask, blockchain
Slug: creating-dapp-with-truffle-and-metamask
Authors: Jitse-Jan
Summary: Inspired by the [article](https://medium.com/metamask/developing-ethereum-dapps-with-truffle-and-metamask-aa8ad7e363ba) by [Dan Finlay](https://twitter.com/danfinlay) and the [video](https://www.youtube.com/watch?v=muWuHIPeXb4) by [Tim Coulter](https://twitter.com/timothyjcoulter), I had my first attempt creating the scaffold for a Truffle application and checking it with Metamask.

## Update npm
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code $ sudo npm install -g npm
```
## Update nodejs
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code $ sudo npm install -g n
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code $ sudo n stable
```
## Install geth
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ brew tap ethereum/ethereum
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ brew install ethereum
```

## Check versions
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ sw_vers
ProductName:	Mac OS X
ProductVersion:	10.12.4
BuildVersion:	16E195
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ geth version
Geth
Version: 1.6.1-stable
Git Commit: 021c3c281629baf2eae967dc2f0a7532ddfdc1fb
Architecture: amd64
Protocol Versions: [63 62]
Network Id: 1
Go Version: go1.8.1
Operating System: darwin
GOPATH=
GOROOT=/usr/local/Cellar/go/1.8.1/libexec
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ node -v
v7.10.0
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ npm -v
4.2.0
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ python -V
Python 2.7.13 :: Anaconda 4.3.1 (x86_64)
```

## Create structure for the app
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ mkdir truffle-dapp
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code  $ cd truffle-dapp/ && git init && npm init
```

## Install web3 and testrpc
Note that you need to use Python 2.7 in order to be able to install the Ethereum testrpc.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ npm install ethereumjs-testrpc web3 --save --python=python2.7
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ echo node_modules/ >> .gitignore
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ git commit -a -m "Initial commit"
```

## Start the testrpc
This includes 10 unlocked accounts with 100 Ether each.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ node_modules/.bin/testrpc
Secp256k1 bindings are not compiled. Pure JS implementation will be used.
EthereumJS TestRPC v3.0.5

Available Accounts
==================
(0) 0x21af84b1d1b0c26dd470d1e13074d784981a1ca7
(1) 0xebf0475f0c9dec6d39d353cab90d10b27f0575a8
(2) 0xc0ffba2ed3bbe73e123cc31fa01215fdd9be3233
(3) 0x5868efd6f3255925268c53e523a81164f4d86733
(4) 0xb3ff5cf0790e67e46fad5e476967d1bd42e9a288
(5) 0x6581ff04d20ad77025d2775c6479bbcf1d292f0c
(6) 0x105a59eb345e602a38553432e7a18360ac3040a8
(7) 0x8febd769876d764d8d1a7bb3d3d4360df9282401
(8) 0xb15505faddaa401f23738843956eab8ab0078d74
(9) 0x56e5a52e65329c75314ec9642725fd272ac908f8

Private Keys
==================
(0) b4b11e97ab1055d41ae8b93d76cb699cc637ab6c45ac3ce769208b37ac7d4e9f
(1) a1222fd97545205ff2e10143a8e6bbe89ea3aa429b4cef64e641885c302a8e4c
(2) 879f33b2dc93fc3add7ab2f189f00c5cf77490090d7d9c46cb4883dd65ece305
(3) 3ced2c7e98b75eb8220edf8109d934ba229d3d5c996d7a297d0ad3961b716275
(4) 3bbaeaa98f28ad987c71815c0f07a79be3bc89c1391ae808ea0af98b61201914
(5) ec6b3c03a904bd7650c803cccb5cf29ccdaa444af336103c021af782b866873c
(6) b1584edd48d57a35acc1176b1a02f7d5c5401e3e00495ce859cf76f8be24b207
(7) 9aa9ce75c4165b30c4847262a4cbb634a2f199228b3386b92e5fa184830bc95b
(8) 68ab448c5a453ea723561b63fb756879bae3fbb44fc003311de62827023ca49a
(9) 674cf39b8c96a8793bf6e0c6c0b3a7c234644eaf7536de1406148fd8699fede7

HD Wallet
==================
Mnemonic:      search romance drip card right human valley tilt depart detail nation rich
Base HD Path:  m/44'/60'/0'/0/{account_index}

Listening on localhost:8545
```

Note. The mnemonic with the 12 words will be used later in Metamask.

## Connect to the testrpc
Create a client and check the balance.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ node
> Web3 = require('web3')
{ [Function: Web3]
  providers:
   { HttpProvider: [Function: HttpProvider],
     IpcProvider: [Function: IpcProvider] } }
> web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
> primary = web3.eth.accounts[0];
'0x914cb49b14a339d000858dc4c8b4cb0e9195c574'
> web3.fromWei(web3.eth.getBalance(primary), "ether").toString()
'100'
```

## Install the Truffle scaffold
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ npm install truffle --save --python=python2.7
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ truffle version
Truffle v3.2.2
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ truffle init webpack
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ git add .
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ git commit -m "Truffle init"
```

## Compile
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ truffle compile
Compiling ./contracts/ConvertLib.sol...
Compiling ./contracts/MetaCoin.sol...
Compiling ./contracts/Migrations.sol...
Writing artifacts to ./build/contracts
```

## Migrate
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ truffle migrate
```

## Deploy
Start the server in the development environment.
```shell
jitsejan@Jitse-Jans-MacBook-Pro  /Users/jitsejan/code/truffle-dapp  $ npm run dev
```
Now by accessing localhost:8080 the web application is visible and we can send some MetaCoin.

Open up Google Chrome and make sure [Metamask](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?authuser=2) is installed. Next open up Metamask and restore from DEN and fill in the 12 words that the testrpc showed you before. Make sure you are connected to localhost:8545.

Click in Metamask on the icon on the top to switch accounts. Click on add and the other accounts will appear. We can now choose one of the other 9 accounts to send some MetaCoin. Click on the copy icon next to the account and enter it in the input field in the form. Add the amount of MetaCoin you want to send and hit Send MetaCoin. Metamask will show a pop-up asking you to accept the transaction.

Once the MetaCoin are sent, the amount on the frontpage are reduced. Clicking again on Metamask will show the history of transactions.



