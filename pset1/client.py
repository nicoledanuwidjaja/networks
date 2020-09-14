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
print('Socket connected to %s on port %s' % address)

try:
    s.connect(address)
except OSError as msg:
    s.close()
    s = None

if s is None:
    print('Socket connection failed. Stoopid')
    sys.exit(1)

# obtain information from server and respond to messages
HELLO = b'cs3700fall2020 HELLO 001489806\n'
s.sendall(HELLO)


def count_keys():
    while True:
        raw_data = ''
        msg = s.recv(8192).split()

        if msg[1] == 'BYE':
            bye = msg
            s.close()
            return bye

        key = msg[2]
        jumbalaya = msg[3]
        print(jumbalaya)
        raw_data += jumbalaya

        # read data until \n
        while '\n' not in jumbalaya:
            jumbalaya = s.recv(8192)
            raw_data += jumbalaya

        print("CURRENT KEY: %s " % key)
        print(raw_data)
        key_count = str(raw_data.count(str(key)))

        COUNT = 'cs3700fall2020 COUNT ' + key_count + '\n'
        s.sendall(bytes(COUNT))
        print(bytes(COUNT))


# f2c8b1629cec0f3d145ca192a9921a026574498378500bf60190c9168f1b9635
flag = count_keys().split()[2]