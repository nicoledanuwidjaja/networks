#!/usr/bin/env python3
import socket
import argparse
import html.parser
import sys
from html.parser import HTMLParser

# parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()

username = args.username
# TBOW0SB4
password = args.password

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.3700.network', 80))


# DATA CHUNK SIZE
DATA_SIZE = 9000

# tracks uncrawled URLs
frontier_tracker = []
cookie = ""
secret_tickets = []
request = b'GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: www.3700.network\r\n\r\n'


# (Host, Content-Length, Content-Type, Cookie and the data to be sent)


# methods for handling the parser


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



# read one page (parsing the HTML)
# - update header cookies for next request
# - add new URLs to frontier_tracker
# - if secret ticket is found, add to secret ticket list
def readPage():
    s.sendall(request)
    result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    print(resStr)

# after reading one page
# - make new request for next URL in frontier_tracker

readPage()

sys.exit(0)