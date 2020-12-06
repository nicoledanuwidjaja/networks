# Project 6 - Distributed, Replicated Key-Value Store

## Description
Build a relatively simple, distributed, replicated key-value datastore. A key-value datastore is a simple type o fdatabase that supports two API calls from clients: `put(key, value)` and `get(key)`.

`put(key, value)` allows a client application to store a key-value pair in the database
`get(key)` allows a client to retrieve a previously stored value by supplying its key.

Real-world examples of distributed key-value datastores include memcached, Redis, DynamoDB, etc.

Implement a simplified version of the Raft consensus protocol to maintain consensus among replicas.
