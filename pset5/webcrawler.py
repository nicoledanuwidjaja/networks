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



# DATA CHUNK SIZE
DATA_SIZE = 9000

# tracks uncrawled URLs
frontier_tracker = []
traversed = []
cookies = []
secret_tickets = []
request = b'GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: www.3700.network\r\n\r\n'
header = []


# helper methods for debugging
def printList(title, ls):
    print('\n', title, ': ')
    for l in ls:
        print(l)


# methods for handling the parser


# def login():
#     msg = f'POST /accounts/login/?next=/fakebook/ HTTP/1.1' \
#           f'\r\nHost: 3700.network\r\nContent-Length: 34\r\n' \
#           f'username={nuid}&password={pw}\r\n\r\n'
#     return msg
#
# def end_of_page(tag):
#     if tag == 'html':
#         return True
#
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#
#     def handle_endtag(self, tag):
#         if tag == 'html':
#             # go to next url in frontier_tracker
#         if tag == '':
#             # login
#
#     def handle_data(self, data):
#         print("Encountered some data  :", data)
#
#

#
# def postMsg(nuid, pw, cookie):
#     msg = f'POST /accounts/login/?next=/fakebook/ HTTP/1.1' \
#           f'\r\nHost: 3700.network\r\nContent-Length: 34\r\n' \
#           f'username={nuid}&password={pw}\r\n\r\n'
#     return msg
#
#
# parser = MyHTMLParser()

def readInitialLoginPage():
    print('READING INITIAL LOGIN PAGE')
    result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    pageList = resStr.split('\r\n')
    header = makeHeaderList(pageList)
    print('200 RETURNED')
    handleCookies(header)
    parseHTML(pageList)

def sendLoginRequest():
    global s
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.3700.network', 80))
    cookie_str = cookieString()
    # get the csrf token
    csrf = ''
    for c in cookies:
        if 'csrftoken=' in c:
            csrf = c[10:]
    data = f'username={username}&password={password}&csrfmiddlewaretoken={csrf}&next=/fakebook/'
    cl = len(data)
    msg = f'POST /accounts/login/ HTTP/1.1' \
          f'\r\nHost: www.3700.network\r\nContent-Type: application/x-www-form-urlencoded' \
          f'\r\nContent-Length: {cl}\r\n{cookie_str}\r\n\r\n' \
          f'username={username}&password={password}&csrfmiddlewaretoken={csrf}&next=/fakebook/'
    print(msg)
    request = bytes(msg, 'utf-8')
    s.sendall(request)

# read one page (parsing the HTML)
# - update header cookies for next request
# - add new URLs to frontier_tracker
# - if secret ticket is found, add to secret ticket list
def readPage(result):
    print('\nREADING NEW PAGE')
    # result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    pageList = resStr.split('\r\n')
    header = makeHeaderList(pageList)
    printList('HEADER', header)
    handleStatusCode(header, pageList)

# make header list from response
def makeHeaderList(pageList):
    header = []
    # put header in header list
    line = pageList.pop(0)
    while line != '':
        header.append(line)
        line = pageList.pop(0)
    return header

# handle status code
def handleStatusCode(header, pageList):
    # create new socket connection
    global s
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.3700.network', 80))
    statusCode = header[0]
    if '500' in statusCode:
        # resend same request
        print('500 RETURNED')
        s.sendall(request)
    elif '403' in statusCode or '404' in statusCode:
        # send next request
        print('403 RETURNED')
        sendGetRequest()
    elif '302' in statusCode:
        # send same request with new given url
        print('302 RETURNED')
        loc = ''
        for h in header:
            if 'Location' in h:
                loc = h
        loc = loc[10:]
        # handleCookies(header)
        sendGetRequest(loc)
    elif '200' in statusCode:
        # if everything is good, first update list of cookies,
        # then parse HTML body
        # then send request for next url in frontier_tracker
        print('200 RETURNED')
        handleCookies(header)
        parseHTML(pageList)
        sendNextGetRequest()


# method for appending new cookies into cookie string
def cookieString():
    cookie = 'Cookie: '
    joined_cookies = "; ".join(cookies)
    cookie += joined_cookies
    return cookie

# update list of cookies
def handleCookies(header):
    global cookies
    cookies = []
    for h in header:
        if 'Set-Cookie' in h:
            parsed_line = h.split(';')
            parsed_cookie = parsed_line[0].split(': ')
            cookies.append(parsed_cookie[1])
    # printList('COOKIES', cookies)

# get body and pass to HTML parser
def parseHTML(pageList):
    body = ''
    # get the html content to pass to html parser
    for i in pageList:
        if 'html' in i:
            body = i
            break
    # print('\nBODY: ', body)

# send GET request for next url in frontier_tracker
def sendNextGetRequest():
    global request
    sendGetRequest(frontier_tracker.pop(0))

# send new GET request based on given url
def sendGetRequest(url):
    global request
    # make new request for given URL
    parsed_url = url.split('www.3700.network')
    subdir = parsed_url[-1]
    # (Host, Content-Length, Content-Type, Cookie and the data to be sent)
    request_type = f'GET {subdir} HTTP/1.1\r\n'
    host = 'Host: www.3700.network\r\n'
    content_length = 'Content-Length: 0\r\n'
    # content_type = 'Content-Type: text/html; charset=utf-8\r\n'
    content_type = 'Content-Type: application/x-www-form-urlencoded\r\n'
    cookie = cookieString()
    msg = ''
    msg += request_type
    msg += host
    # msg += content_length
    # msg += content_type
    msg += cookie
    msg += '\r\n'
    print('MSG: ')
    print(msg)
    # SEND GET REQUEST
    request = bytes(msg, 'utf-8')
    s.sendall(request)
    print('sent')

# make initial request
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.3700.network', 80))
s.sendall(request)
# read initial response
readInitialLoginPage()
# send login request
sendLoginRequest()
# start running readPage
result = s.recv(DATA_SIZE)
while result:
    readPage(result)
    s.recv(DATA_SIZE)
sys.exit(0)