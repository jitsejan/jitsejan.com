Title: Setting up a private Ethereum blockchain
Date: 2017-05-01 10:19
Modified: 2017-05-01 10:19
Category: posts
Tags: vps, ether, ethereum, Linux, geth, blockchain
Slug: setting-up-private-ethereum-blockchain
Authors: Jitse-Jan
Summary: Following the steps from the [etcdocs.org](http://ethdocs.org/en/latest/network/test-networks.html), I try to set up a private blockchain to perform my first -fake- transaction.

## Setup
For this experiment, I will use three Linux machines running Ubuntu. Machine one will be used as the base, the second machine will send some Ether to the third machine.

```shell
jitsejan@jjvps:~$ uname -a
Linux jjvps 2.6.32-042stab123.1 #1 SMP Wed Mar 22 15:21:30 MSK 2017 x86_64 x86_64 x86_64 GNU/Linux
jitsejan@jjvps:~$ geth version
Geth
Version: 1.6.0-stable
Git Commit: facc47cb5cec97b22c815a0a6118816a98f39876
Architecture: amd64
Protocol Versions: [63 62]
Network Id: 1
Go Version: go1.8.1
Operating System: linux
GOPATH=
GOROOT=/usr/lib/go-1.8
```

```shell
jitsejan@jjschi1:~$ uname -a
Linux jjschi1 2.6.32-042stab108.8 #1 SMP Wed Jul 22 17:23:23 MSK 2015 x86_64 x86_64 x86_64 GNU/Linux
jitsejan@jjschi1:~$ geth version
Geth
Version: 1.6.0-stable
Git Commit: facc47cb5cec97b22c815a0a6118816a98f39876
Architecture: amd64
Protocol Versions: [63 62]
Network Id: 1
Go Version: go1.8.1
Operating System: linux
GOPATH=
GOROOT=/usr/lib/go-1.8
```

```shell
jitsejan@jjschi2:~$ uname -a
Linux jjschi2 2.6.32-042stab094.7 #1 SMP Wed Oct 22 12:43:21 MSK 2014 x86_64 x86_64 x86_64 GNU/Linux
jitsejan@jjschi2:~$ geth version
Geth
Version: 1.6.0-stable
Git Commit: facc47cb5cec97b22c815a0a6118816a98f39876
Architecture: amd64
Protocol Versions: [63 62]
Network Id: 1
Go Version: go1.8.1
Operating System: linux
GOPATH=
GOROOT=/usr/lib/go-1.8
```

## Create new user accounts
Repeat the following for all the machines.

```shell
jitsejan@jjschi1:~$ geth account new
WARN [05-01|06:51:51] No etherbase set and no accounts found as default 
Your new account is locked with a password. Please give a password. Do not forget this password.
Passphrase: 
Repeat passphrase: 
Address: {fb82f6d873addc0032a08aaa05bb1c338ce49b45}
```

## Create a genesis file
Create a genesis file with the 3 addresses from the newly created accounts. Set an initial balance to the accounts so we can transfer some 'money'. Set the gasLimit to the maximum and the difficulty low.

```shell
jitsejan@jjvps:~$ nano jitsejansGenesis.json 
```

```json
{
    "config": {
        "chainId": 15,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "nonce": "0x0000000000000042",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "difficulty": "0x4000",
    "alloc": {},
    "coinbase": "0x0000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": "0xffffffff",
    "alloc": {
        "0xfb82f6d873addc0032a08aaa05bb2c338ce49b45": { "balance": "20000000000000000000" },
        "0xc257beaea430afb3a09640ce7f020c906331f805": { "balance": "40000000000000000000" },
        "0xe86ee31b7d32b743907fa7438c422a1803717deb": { "balance": "40000000000000000000" }
    }    
}
```

Copy the genesis file to the second machine and third machine.

```shell
jitsejan@jjschi1:~$ nano jitsejansGenesis.json
```

```shell
jitsejan@jjschi2:~$ nano jitsejansGenesis.json
```


## Initialize the blockchain
Initialize the blockchains on all three machines.
```shell
jitsejan@jjsvps:~$ geth init jitsejansGenesis.json 
INFO [05-01|06:56:35] Allocated cache and file handles         database=/home/jitsejan/.ethereum/geth/chaindata cache=128 handles=1024
INFO [05-01|06:56:35] Writing custom genesis block 
INFO [05-01|06:56:35] Successfully wrote genesis state         hash=86a3b9…deee1b
```

## Start the blockchain
On the first machine, start the blockchain.

```shell
jitsejan@jjvps:~$ geth --networkid 23 --nodiscover --maxpeers 2  --port 30333 console 
```
Get information about the hosting node.

```shell
> admin.nodeInfo.enode
"enode://342a11d352151b3dfeb78db02a4319e1255c9fb49bc9a1dc44485f7c1bca9cc638540833e4577016f9a6180d1e911d907280af9b3892c53120e1e30619594eba@[::]:30333?discport=0"
```

## Connect to the blockchain
With the node information from the previous step, we can now create a static nodes files on the second and third machine to connect to the running blockchain.

```shell
jitsejan@jjschi1~$ nano ~/.ethereum/static-nodes.json
```

Replace the `[::]` with the IP address of the first machine and copy the file on the third machine too.

```json
[
"enode://84f9c7f807a58f98643ac2bff9ea6691bf6be36fe6d0ccd0ad838a83501d16c1027269a82c3251104a10da5982e4fe905de41ae84dd44ba78e8cfb1659d355e8@192.123.345.567:30303?discport=0"
]
```

Restart the blockchain on the first machine.

```shell
jitsejan@jjsvps:~$ geth --networkid 23 --nodiscover --maxpeers 1 --port 30333 console
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
20
```

Connect to the blockchain with the second machine and third machine.

```shell
jitsejan@jjschi1:~$ geth --networkid 23 --port 30333 console
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
40
```                                                              

Once you perform a mining action, by default Ether will reward you with 5 ether.

```shell
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
40
> miner.start();admin.sleepBlocks(1);miner.stop();
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
45
```

## Perform a transaction
### Unlock the sending machine

```shell
> personal.unlockAccount('0x1c1ab1dcc7054c35a6029b0904cbead5aab37c54')
Unlock account 0x1c1ab1dcc7054c35a6029b0904cbead5aab37c54
Passphrase: 
true
```

### Send the transaction
```shell
> eth.sendTransaction({from: '0x1c1ab1dcc7054c35a6029b0904cbead5aab37c54', to: '0xfb82f6d873addc0032a08aaa05bb1c338ce49b45', value: web3.toWei(23, "ether")})
INFO [05-01|15:09:47] Submitted transaction                    fullhash=0x9ea76acbba2ad0bf65dc9b4295bfd7f2836435329a1fee9162b0649f35855ad3 recipient=0xfb82f6d873addc0032a08aaa05bb2c338ce49b45
"0x9ea76acbba2ad0bf65dc9b4295bfd7f2836435329a1fee9162b0649f35855ad3"
```

Check for pending transactions. The transaction should be queued.

```shell
> eth.pendingTransactions
[{
    blockHash: null,
    blockNumber: null,
    from: "0x1c1ab1dcc7054c35a6029b0904cbead5aab37c54",
    gas: 90000,
    gasPrice: 20000000000,
    hash: "0xf63024c9828ff5b77e63c118667394b285735da9ad53d01bf44aa8044b824955",
    input: "0x",
    nonce: 0,
    r: "0x14ac03d0f4f55b4aa73b4f1f9f04752174bdf304366c994e8e4d26448e7decba",
    s: "0x3ca7ab2f856d5e1edd6b6429df9b7be7a3c08d4afd4b2ac5a4ca9bdad2ec0caf",
    to: "0xfb82f6d873addc0032a08aaa05bb1c338ce49b45",
    transactionIndex: 0,
    v: "0x41",
    value: 3000000000000000000
> net.peerCount
1
> net.listening
true
> txpool.status
{
  pending: 1,
  queued: 0
}
```

On the receiving machine we start the mining to receive the transaction.

``` shell
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
96
> miner.start(1);admin.sleepBlocks(1);miner.stop();
INFO [05-01|10:51:14] Updated mining threads                   threads=1
INFO [05-01|10:51:14] Starting mining operation 
INFO [05-01|10:51:14] Commit new mining work                   number=96 txs=1 uncles=0 elapsed=335.481µs
INFO [05-01|10:51:14] 🔗 block reached canonical chain          number=14 hash=b323e7…3daf34
INFO [05-01|10:51:20] Successfully sealed new block            number=96 hash=8d2949…3f8a32
INFO [05-01|10:51:20] 🔨 mined potential block                  number=96 hash=8d2949…3f8a32
INFO [05-01|10:51:20] Commit new mining work                   number=97 txs=0 uncles=0 elapsed=772.386µs
true
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
124.00042
```

On the sending machine we check again the balance. 

```shell
> balance = web3.fromWei(eth.getBalance(eth.accounts[0]), "ether");
405.99958
```

We can see that indeed the 23 Ether got deducted, plus 0.00042 Ether to pay for the gas. The balance of the receiving machine got another 5 Ether for the mining action
and got paid for the gas. If we perform a transaction from the second to the third machine, but perform the mining on the first machine, the third machine will only
get the amount transferred while the first machine receives the mining bonus and the payment for the gas.