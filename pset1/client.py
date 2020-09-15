import socket
import sys

# default values
NUID = '001489806'
HOST = '3700.network'
PORT = 27993

# Usage: ./client <-p port> <-s> [hostname] [NEU ID]
args = sys.argv
port_flag = '-p' in args
ssl_flag = '-s' in args

# check if optional -p flag is properly set up or not used
valid_port = (port_flag and args[port_flag + 1].isdigit()) or not port_flag

if len(args) < 6 and args[-1].isdigit() and valid_port:
    if port_flag:
        PORT = int(args[port_flag + 1])
    HOST = args[-2]
    NUID = args[-1]
else:
    print('Usage: ./client <-p port> <-s> [hostname] [NEU ID]')
    sys.exit(1)

address = (HOST, PORT)

# creates TCP/IP socket
# sockets enable data transfer with the Internet via API
# AF_INET = IPv4 address
# SOCK_STREAM = stream sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(address)
except OSError:
    s.close()
    s = None

if s is None:
    print('Socket connection failed. Stoopid')
    sys.exit(1)

# obtain information from server and respond to messages
HELLO = 'cs3700fall2020 HELLO ' + NUID + '\n'
s.sendall(bytes(HELLO))


def count_keys():
    while True:
        raw_data = ''
        msg = str(s.recv(8192)).split()

        # close socket connection
        if msg[1] == 'BYE':
            s.close()
            return msg

        key = msg[2]
        jumbalaya = msg[3]
        print(msg)
        raw_data += jumbalaya

        # read data until \n
        while '\n' not in jumbalaya:
            jumbalaya = s.recv(8192)
            raw_data += jumbalaya

        print("CURRENT KEY: %s " % key)
        print("BEGIN %s" % msg)
        key_count = str(raw_data.count(str(key)))

        COUNT = 'cs3700fall2020 COUNT ' + key_count + '\n'
        s.sendall(bytes(COUNT))
        print(COUNT)


flag = count_keys()[2]
print(flag)