# Project 5: Web Crawler

### Approach
For our web crawler, we worked on implementing our own HTTP requests and responses from scratch. First, we created a POST request that logged into the Fakebook server with our credentials and stored a session cookie. 

As part of our implementation, we built a custom header for each request and parsed the responses in order to extract necessary session cookies. We created a GET request that would use this session cookie and crawl through the data using our implementation of the HTTPParser class. In order to crawl each page, we scraped the links found on the page, and parsed through the content to find any flags. Then, we stored links found in our frontier tracker, represented as a deque to store untraversed URLs. The deque stores the order of these references and pops off the next link to visit the corresponding page. This process continues until the frontier tracker is empty or if all five flags have been found. 

### Challenges
Initially creating the structure of the headers and the requests was challenging, but after we figured out how to structure the POST and GET requests, we were able to use the HTTPParser class to parse through the data. Other challenges were ensuring that the socket connection would not time out, as well as handling the different response code cases.

## Details
Implement a web crawler that gathers data from Fakebook. A web crawler (robot, spider, scraper) is a piece of software that automatically gathers and traverses documents on the web. Web crawlers are a fundamental component of today's web.

### Fakebook
- *Homepage*: Fakebook homepage displays some welcome text and links to several random Fakebook users' personal profiles.
- *Personal Profiles*: Each Fakebook user has a profile page that includes their name, basic demographic information, and a link to their list of friends.
- *Friends List*: Each Fakebook user is friends with one or more other Fakebook users. This page lists the user's friends and has links to their personal profiles.

To browse Fakebook, you must first login with a username and password.

### Acceptance Criteria
The goal is to collect 5 secret flags hidden on the Fakebook website. The flags are unique for each student, and the pages that contain the flags will be different for each student.

The web crawler must execute on the command line using the following syntax:

`./webcrawler [username] [password]`

Secret flags may be hidden on any page on Fakebook. Each secret flag is a 64-charachter long sequence of random alphanumerics. All secret flags have the following format:

`<h2 class='secret-flag' style='color:red'>FLAG: 64-characters</h2>`

### Implementation
The crawler must implement HTTP/1.1 and must have certain HTTP headers that must be included in requests.

Encouraged headers: 
- Connection: Keep-Alive
- Accept-Encoding: gzip

HTTP/1.1 servers support chunked encoding, and the client must be able to reconstruct data by combining the chunks.

Strategy: Store uncrawled URLs in an execution stack and track URLs that have already been crawled. Lastly, only crawl target domains and ensure that each URL passed is valid.

#### HTTP Protocol
- GET: download HTML pages
- POST: login to Fakebook
- Cookie Management: Fakebook returns session cookie to crawler upon sucessful login, and should store and submit cookie along each HTTP GET request.

#### Status Codes
- 200: OK
- 302: Found - HTTP Redirect, use new URL given by server in Location header
- 403: Forbidden - Abandon URL
- 404: Not Found - Abandon URL
- 500: Internal Server Error - Retry URL request until successful


