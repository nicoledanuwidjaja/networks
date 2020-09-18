## Project 1: Socket Basics
### Approach
Tackled understanding the in's and out's of creating a client program for communicating with a socket using TCP/IP protocol. Used [Python documentation](https://docs.python.org/3/library/socket.html#example) examples to illustrate proper usages of `connect`, `sendall`, and `recv(bytes)`.

Worked on testing the program for potential problems with malformed input data at several steps of the program: command line arguments, socket communication, correct calculations for respective message types, and eventual termination of the program.

Command line arguments (-p for port, -s for ssl connection) were implemented and were tested for variable NUIDs, port numbers, and hostnames. The program was separated into three main functions: `create_socket`, `process_msg`, and `count_keys`.

`create_socket`: created the TCP/IP socket connection

`process_msg`: encode and process various message types received from server

`count_keys`: received message data from server and performed count calculations for given key

### Challenges
Initially had difficulties understanding why data received from the server was in a different form than expected (misshaped `FIND` messages) and then eventually realized that the client program failed to account for the entire string of random characters within the `FIND` message by stopping searching with `socket.recv(bytes)` prematurely as opposed to searching until the `\n` newline is found. Because of the nature of sending and receiving messages through the socket, it was difficult to troubleshoot why exactly was my program failing.


## Details
### Description
Implement a client program which communicates with a server using sockets. The server will ask the program to do some basic string manipulation and counting. If the program successfully counts all of the strings, then the server will return a unique secret flag.

### Protocol
Server runs on `3700.network` machine and listens for requests on a TCP socket bound to `port 27993`.

There are four types of messages: HELLO, FIND, COUNT, and BYE. Each message is an ASCII string consisting of multiple fields separated by spaces (0x20) and terminated with a line feed (0x0A, \n). The maximum length of each message is 8192 bytes.

Once the socket is connected, the client sends a HELLO message to the server.

```
cs3700fall2020 HELLO [your NEU ID]\n
```

The server will reply with a FIND message:
```
cs3700fall2020 FIND [A single ASCII symbol] [A string of random characters]\n
```
The client must count the number of occurrences of the [ASCII symbol] in the [random characters] and send a COUNT message to the server.
```
cs3700fall2020 COUNT [the count of the given symbol in the given string]\n
```
If the  count is incorrect, the server will terminate the connection. Otherwise, the server will either send another FIND message or return a BYE message:
```
cs3700fall2020 BYE [a 64 byte secret flag]\n
```
Once the program has received the BYE message, it can close the connection to the server, and return a secret flag (64-bit).

### Submission
The client program executes on the command line:
```
$ ./client <-p port> <-s> [hostname] [NEU ID]
```
The -p port parameter is optional; it specifies the TCP port that the server is listening on.

If this parameter is not supplied on the command line, your program must assume that the port is 27993.

The -s flag is optional; if given, the client should use an SSL encrypted socket connection. Your client only needs to support -s if you are trying to get the extra credit point.

The [hostname] parameter is required, and specifies the name of the server (either a DNS name or an IP address in dotted notation).

The [NEU ID] parameter is required. Your code must support NEU IDs that have leading zeroes (do not strip them!).

The program should print exactly one line of output: the secret flag from the server's BYE message. If the program encounters an error, it may print an error message before terminating.
