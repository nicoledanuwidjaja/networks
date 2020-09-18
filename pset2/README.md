## Project 2: FTP Client

### Approach

### Challenges


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

The FTP client must execute on the command line:
```
./3700ftp [operation] param1 [param2]
```
_operation_ is a string that specifies what operation the user is attempting to perform. Valid operations are ls, mkdir, rm, rmdir, cp, and mv. Each operation requires either one or two parameters.

_param1_ and _param2_ are strings that either represent a path to a file on the local filesystem, or a URL to a file or directory on a FTP server.

FTP requests take the form of:
```
COMMAND <param> <...>\r\n
```

`COMMAND` is typically a three or four letter command that tells the FTP server to perform some action.

After each request, the FTP server will reply with at least one response. All FTP responses take the form of:
```
CODE <human readable explanation> <param>.\r\n
```

`CODE` is a three-digit integer that specifies whether the FTP server was able to complete the request.
