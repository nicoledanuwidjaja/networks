import socket, argparse

# parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()

username = args.username
password = args.password

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('http://www.3700.network/fakebook/', 80))

# tracks uncrawled URLs
frontier_tracker = []

def getMsg(subdir,cookies):
    msg = f'GET {subdir} HTTP/1.1\nHost: 3700.network\nCookie: {cookies}\n\n'
    return msg

def postMsg(nuid, pw):
    msg = f'POST /accounts/login/?next=/fakebook/ HTTP/1.1' \
          f'\nHost: 3700.network\nContent-Length: \n\n' \
          f'username={nuid}&password={pw}\n\n'
    return msg

