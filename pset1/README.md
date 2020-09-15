## Project 1: Socket Basics
### Approach
Tackled understanding the in's and out's of creating a client program for communicating with a socket using TCP/IP protocol. Used [Python documentation](https://docs.python.org/3/library/socket.html#example) examples to illustrate proper usages of `connect`, `sendall`, and `recv(bytes)`.

Also worked on testing the program for potential problems with malformed input data at several steps of the program: command line arguments, socket communication, correct calculations for respective message types, and eventual termination of the program. 

### Challenges
Initially had difficulties understanding why data received from the server was in a different form than expected (misshaped `FIND` messages) and then eventually realized that the client program failed to account for the entire string of random characters within the `FIND` message by stopping searching with `socket.recv(bytes)` prematurely as opposed to searching until the `\n` newline is found.