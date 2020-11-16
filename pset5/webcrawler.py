#!/usr/bin/env python3
import socket
import argparse
import struct
import html.parser
import sys
from html.parser import HTMLParser

# parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()
username = args.username
# TBOW0SB4 (Michelle), FPYDCAIB (Nicole)
password = args.password

# establish socket connection with Fakebook
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.3700.network', 80))

# DATA CHUNK SIZE
DATA_SIZE = 9000

frontier_tracker = [] # store URLs to visit in queue
crawled_URLs = [] # store visited URLs to avoid loop
cookie = "" # store cookies? wut this
secret_flags = [] # store secret flags found on pages
request = b'GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: www.3700.network\r\n\r\n'

# TODO: THE PLAN!!
# Start at root URL (Login)
# Get webpage documents and add each link found on the webpage to our queue, uncrawled_URLs
# Keep recursing and visiting all links until queue is empty (We can use BFS!)
# - Make sure we don't re-add URLs we already visited to the queue again
# - Look for secret flags!
# - Validate each URL to make sure they're still on Fakebook (www.3700.network)
# - Add more TODO if anything is missing
# This sounds like fun :D
# Anyways, I could definitely be wrong or just being super confusing, so feel free to change anything!

# (Host, Content-Length, Content-Type, Cookie and the data to be sent)
class MyHTMLParser(HTMLParser):
    # prints out attributes of a tag
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

        # if tag is a potential flag, check attributes and add to secret flags
        if tag == 'h2':
            for attr in attrs:
                print("     attr:", attr)
                if attr[0] == 'class' and attr[1] != 'secret-flag':
                    break
                if attr[0] == 'style' and attr[1] != 'color:red':
                    break
            # this should return the secret flag data
            flag = handle_data(tag):
            secret_flags.append(flag)


    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        if tag == 'html':
            # TODO: placement undecided; add all urls to frontier_tracker?
            handle_url(restStr)
            # go to next url in frontier_tracker
            next_url = frontier_tracker.pop()
            # TODO: make request to scrape next url

        if tag == '':
            # login

    # TODO NEEDS WORK
    # parses through page HTML content and stores unvisited urls in frontier
    def handle_url(self, url):
        if url.startswith('<a>'):
            # get url
            # if scraped_url not in crawled_URLs:
                # frontier_tracker.append(scraped_url)

    # prints out raw data of HTML page
    def handle_data(self, data):
        print("HTML CONTENT:", data)
        return data


# methods for handling the parser
def end_of_page(tag):
    if tag == 'html':
        return True

# get request for receiving web content
def getMsg(subdir, cookies):
    msg = f'GET {subdir} HTTP/1.1\nHost: 3700.network\nCookie: {cookies}\n\n'
    byte_msg = bytes(msg, 'utf-8')
    s.sendall(byte_msg)
    print("GET Request made to Fakebook: ", subdir)

# TODO: Get cookies from POST request
# post request for logging into Fakebook
def postMsg(nuid, pw):
    msg = f'POST /accounts/login/?next=/fakebook/ HTTP/1.1' \
          f'\nHost: 3700.network\nContent-Length: \n\n' \
          f'username={nuid}&password={pw}\n\n'
    byte_msg = bytes(msg, 'utf-8')
    s.sendall(byte_msg)
    print("POST Request made to Fakebook")

# read one page (parsing the HTML)
# - update header cookies for next request
# - add new URLs to frontier_tracker
# - if secret ticket is found, add to secret ticket list
def readPage():
    s.sendall(request)
    result = s.recv(DATA_SIZE)
    resStr = result.decode('utf-8')
    print(resStr)
    return resStr


# check if url starts with http://www.3700.network
def isValidURL(url):
    regex = ("((http|https)://)(www.3700.network)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    checker = re.compile(regex)
    # checks if the regex of url is valid
    return url and re.search(checker, url)



# TODO: Figure out how to organize this
parser = MyHTMLParser()
# login and receive cookies
postMsg(username, password)
# after reading one page
# - make new request for next URL in frontier_tracker
content = readPage()
# TODO: undecided where this stuff should go
parser.feed(content)

sys.exit(0)