#!/usr/bin/env python3
import socket
import argparse
import html.parser
import sys
import datetime
import time
from collections import deque
from html.parser import HTMLParser

# parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()

username = args.username
# TBOW0SB4 (Michelle), FPYDCAIB (Nicole)
password = args.password

# DATA CHUNK SIZE
DATA_SIZE = 9000

# tracks uncrawled URLs
frontier_tracker = deque([]) # store URLs to visit in queue
traversed = [] # store visited URLs to avoid loop
cookies = [] # store cookies obtained from logging in
flags = [] # store secret flags found on pages
request = b'GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: www.3700.network\r\n\r\n'
header = []
url_count = 0

# helper methods for debugging
def printList(title, ls):
    print('\n', title, ': ')
    for l in ls:
        print(l)

# checks if a link is valid
def validLink(link):
    return ('fakebook' in link) and (link not in traversed) and (link not in frontier_tracker)

# handles 'a' tags
def handleATag(attrs):
    (href, link) = attrs[0]
    if validLink(link):
        frontier_tracker.append(link)
        # print(link)

# handles possible error
def handleError(attrs):
    for attr in attrs:
        (type, val) = attr
        if type == 'class' and val == 'errorlist':
            print("There was an error.")
            sys.exit(1)

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            handleATag(attrs)
        if tag == 'ul':
            handleError(attrs)

    def handle_endtag(self, tag):
        return None

    def handle_data(self, data):
        # print(data)
        if "FLAG" in data:
            print("Found flag!")
            flags.append(data[6:])
            # print(data)


def readInitialLoginPage():
    # print('READING INITIAL LOGIN PAGE')
    result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    pageList = resStr.split('\r\n')
    while '403' in pageList[0] or '404' in pageList[0]:
        s.sendall(request)
        result = s.recv(DATA_SIZE)
        resStr = result.decode('utf-8')
        pageList = resStr.split('\r\n')
    header = makeHeaderList(pageList)
    # print('200 RETURNED')
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
    # print(msg)
    request = bytes(msg, 'utf-8')
    s.sendall(request)

# read one page (parsing the HTML)
# - update header cookies for next request
# - add new URLs to frontier_tracker
# - if secret ticket is found, add to secret ticket list
def readPage(result):
    # print('\nREADING NEW PAGE')
    # result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    pageList = resStr.split('\r\n')
    # print(pageList)
    header = makeHeaderList(pageList)
    handleCookies(header)
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
        # print('500 RETURNED')
        s.sendall(request)
    elif '403' in statusCode or '404' in statusCode:
        # send next request
        print('403 RETURNED')
        sendNextGetRequest()
    elif '302' in statusCode:
        # send same request with new given url
        # print('302 RETURNED')
        # printList("302", header)
        loc = ''
        for h in header:
            if 'Location' in h:
                loc = h
        loc = loc[10:]
        # cookies.pop(-1)
        handleCookies(header)
        sendGetRequest(loc)
    elif '200' in statusCode:
        # if everything is good, first update list of cookies,
        # then parse HTML body
        # then send request for next url in frontier_tracker
        # print('200 RETURNED')
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
    # cookies = []
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
#     print('\nBODY: ', body)
    parser = MyHTMLParser()
    parser.feed(body)

# send GET request for next url in frontier_tracker
def sendNextGetRequest():
    global request
    # next_link = frontier_tracker.pop(0)
    if not frontier_tracker:
        print("Frontier is empty!")
        sys.exit(1)
    sendGetRequest(frontier_tracker.popleft())

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
    msg += '\r\n\r\n'
    # print('MSG: ')
    # print(msg)
    # SEND GET REQUEST
    request = bytes(msg, 'utf-8')
    s.sendall(request)
    print(url)
    # add traversed url to traversed
    traversed.append(url)


# run program
start = datetime.datetime.now()
print("Start Time: ", start)
# set up network connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.3700.network', 80))
# make initial request
s.sendall(request)
# read initial response
readInitialLoginPage()
# send login request
sendLoginRequest()
# start running readPage
result = s.recv(DATA_SIZE)

while result:
    readPage(result)
    if len(flags) >= 5:
        printList('FLAGS', flags)
        end = datetime.datetime.now()
        print("End Time: ", end)
        print("Total Time: ", (end - start).total_seconds())
        sys.exit(0)
    else:
        result = s.recv(DATA_SIZE)
        url_count += 1
#         print("Url count: " + str(url_count))
#         print("Flags: " + str(flags))

print("Flags: " + str(flags))


