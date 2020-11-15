import socket, argparse
import html.parser
from html.parser import HTMLParser

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

# methods for handling the parser
def get_start_tag(parser):
    parser.handle_starttag()


def end_of_page(tag):
    if tag == 'html':
        return True

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):

    def handle_endtag(self, tag):
        if tag == 'html':
            # go to next url in frontier_tracker
        if tag == '':
            # login


    def handle_data(self, data):
        print("Encountered some data  :", data)


def getMsg(subdir,cookies):
    msg = f'GET {subdir} HTTP/1.1\nHost: 3700.network\nCookie: {cookies}\n\n'
    return msg

def postMsg(nuid, pw):
    msg = f'POST /accounts/login/?next=/fakebook/ HTTP/1.1' \
          f'\nHost: 3700.network\nContent-Length: \n\n' \
          f'username={nuid}&password={pw}\n\n'
    return msg

# def readPage():


parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')

parser.hand

# run the script
while True:
    s.read

sys.exit(0)