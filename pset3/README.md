## Project 3: Simple BGP Router
### Approach

### Challenges


## Details
### Description
A Border Gateway Protocol (BGP) Router is a hardware box that exchanges routing and reachability information among Autonomous Systems (AS). A network administrator would plug cables into BGP ports that connect to neighboring BGP routers, either from the same AS or another one.

The Administrator is responsible for manually configuring each port by 1) choosing the IP address that the router uses, and 2) choosing whether this port leads to a provider, peer, or customer.

After this manual configuration is complete, the administrator turns on the router and contacts its neighbors and establishes BGP sessions. The neighboring routers can pass BGP protocol messages to each other, as well as pass data packets from internet users.

The router's job is to kep its forwarding table up-to-date, based on the BGP protocol messages, and also keep neighbor's forwarding tables up to date by sending BGP protocol messages to them, as well as forwarding data packets to their correct destination.

