## Project 1: Socket Basics
### Description
Implement a client program which communicates with a server using sockets. The server will ask the program to do some basic string manipulation and counting. If the program successfully counts all of the strings, then the server will return a unique secret flag.

### Protocol
Server runs on `3700.network` machine and listens for requests on a TCP socket bound to `port 27993`.

Four types of messages: HELLO, FIND, COUNT, and BYE. Each message is an ASCII string consisting of multiple fields separated by spaces (0x20) and terminated with a line feed (0x0A, \n). The maximum length of each message is 8192 bytes.

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