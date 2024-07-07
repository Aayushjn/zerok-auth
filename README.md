# Privacy-Preserving Password-Based Authentication Using Zero-Knowledge Proofs

A framework for zero-knowledge-based authentication as an alternative for traditional authentication mechanisms. 
Relying on client-server architecture, the framework ensures that passwords always remain on the client and are never 
passed to the server, and instead derives parameters from the credentials. The server-side stores these parameters as 
**password-equivalent** data. The authentication of registered user happens utilizing the concept of Zero-Knowledge 
Proofs, where the actual chosen credentials get exposed neither to the server nor the medium between the client and 
server. Zero-Knowledge Proofs require a computationally "hard problem" to carry out the authentication. Currently we 
implement a graph isomorphism-based ZKP protocol. The framework is designed such that any hard problem can be simply 
swapped easily.

## Getting Started

### Prerequisites

- Python 3.10+
- Dependencies from [requirements.txt](./requirements.txt)
- MongoDB

### Installing

Run `pip install -r requirements.txt` to install all dependencies once a Python 3.10+ virtual environment has been 
created.

## Running the code

Ensure that MongoDB is running before running the following commands.

Create a file with the following content

```dotenv
ZEROK_DB_HOST=127.0.0.1 # change as per MongoDB config
ZEROK_DB_PORT=27017 # change as per MongoDB config
ZEROK_DB_USER= # change as per MongoDB config
ZEROK_DB_PASS= # change as per MongoDB config
ZEROK_DB_NAME=zkp_users
ZEROK_BATCH_SIZE=5
ZEROK_ROUNDS=10
```

Now run `python run_server.py` to start the server. Then run `python main.py` to run the client.

### Other files

[stats.py](./stats.py) generates statistics on the graph generation schemes and helps in determining the effectiveness 
of the various approaches used.

[latency_test.py](./latency_test.py) is used for testing the time taken for registration and authentication flows to 
complete and compare the traditional authentication mechanisms with ZKP-based mechanism. Testing for various latency 
and bandwidth scenarios was done using Mininet.

## Contributors

* **Aayush Jain** - https://github.com/Aayushjn
* **Adwait Gondhalekar** - https://github.com/adwaitgondhalekar
