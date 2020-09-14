import socket
import sys

host = '3700.network'
port = 27993
address = (host, port)

# creates TCP/IP socket
# sockets enable data transfer with the Internet via API
# AF_INET = IPv4 address
# SOCK_STREAM = stream sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Creating socket connection on %s on port %s' % address)

try:
    s.connect(address)
except OSError as msg:
    s.close()
    s = None

if s is None:
    print('Socket connection failed. Stoopid')
    sys.exit(1)

# obtain information from server
msg = s.recv(8192)

s.close()
print("Data: %s" % msg.decode('ascii'))