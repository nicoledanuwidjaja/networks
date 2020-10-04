## Project 2: FTP Client

### Approach
I approached this by first tackling the command line, and then working through each of the commands, keeping the recommended order in mind. I was able to use some of Go's libraries, such as flag, io, and net to connect to the TCP/IP channels, as well as connect and manipulate files.

### Challenges
The main challenges were similar to the first assignment, where receiving data from the server was sometimes inconsistent. I found that this was difficult to debug, and mainly occurred for receiving data from the server. While I didn't have problems with uploading files, I found that I need to be more cautious of properly reading the instructions in the future in order to avoid splurging time on simple mistakes.




## Details

### Description
Develop a client for File Transfer Protocol (FTP). The client must login to a remote FTP server and perform several operations on the remote server. Implement all FTP request and response code by yourself, using libraries to create socket connections and parse URLs.

### Objectives
- Command line parsing
- Connection establishment
- MKD and RMD
- PASV and LIST
- STORE, RETR, and DELE

### Protocol
The FTP server is available at ftp://3700.network.

The client will run on the command line and must support the following six operations: directory listing, making directories, file deletion, directory deletion, copying files to and from the FTP server, and moving files to and from the FTP server.

Commands: `ls`, `mkdir`, `rm`, `rmdir`, `cp`, `mv`

The FTP client must execute on the command line:
```
./3700ftp [operation] param1 [param2]
```
_operation_ is a string that specifies what operation the user is attempting to perform. Valid operations are ls, mkdir, rm, rmdir, cp, and mv. Each operation requires either one or two parameters.

_param1_ and _param2_ are strings that either represent a path to a file on the local filesystem, or a URL to a file or directory on a FTP server.


#### FTP requests
FTP requests take the form of:
```
COMMAND <param> <...>\r\n
```

`COMMAND` is typically a three or four letter command that tells the FTP server to perform some action.
__
After each request, the FTP server will reply with at least one response. All FTP responses take the form of:
```
CODE <human readable explanation> <param>.\r\n
```

`CODE` is a three-digit integer that specifies whether the FTP server was able to complete the request.

The FTP client should be able to send the following commands: `USER`, `PASS`, `TYPE`, `MODE`, `STRU`, `LIST`, `DELE`, `MKD`, `RMD`, `STOR`, `RETR`, `QUIT`, `PASV`


#### Socket Connections
FTP protocol requires connecting with two socket connections: 
1. Control Channel: Client opens to FTP server on `Port 21` for sending and receiving requests and responses
2. Data Channel: Client asks FTP server to open data channel on second port to upload and download data with `PASV` command

The server responds with a message:
```
227 Entering Passive Mode (192,168,150,90,195,149)
```
`Code 227` indicates success. The six numbers are the IP address `(192.168.150.90)` and port number that the client should connect a TCP/IP socket to in order to create the data channel.
The two port numbers represent the top and bottom 8-bits of the port number. `(195 << 8) + 149 = 50069`

Once the data transfer is complete, the data channel must be closed by the sender. One PASV data channel must be opened per operation. The control channel must stay open while the data channel is open. Once the data channel is closed, the client can end the FTP session by sending `QUIT` to the FTP server on the control channel and closing the control socket. 