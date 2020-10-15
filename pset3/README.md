## Project 3: Simple BGP Router
### Approach
We began with the starter code and worked on implementing the different types of messages. 

The update message broadcasts the announcement to neighbors by updating the source IP and destination ip addresses of each message, as well as adding the router's ASPath to the AS list. In addition, it updates the forwarding table with a new entry with the message's network, netmask, and the source IP of the router that sent the message.

Then, we worked on the data message via forwarding data packets, which checked if the packet's destination IP address belonged to any of the source network prefixes/netmasks listed in the table. For now, we assume that there can only be one valid match and assign that as the port destination. We implemented two of the four valid scenarios where there is either no route or one possible route, then converted and sent the corresponding data packet information.

Finally, we implemented dump table requests, where we handled dump messages by responding with a copy of the current router forwarding table.

### Challenges
Understanding the overall schema of the router was a little tricky at first, but we were able to work through the network relationships!

## Details
### Acceptance Criteria
- Accept route update messages from the BGP neighbors, and forward updates as appropriate
- Accept route revocation messages from the BGP neighbors, and forward revocations as appropriate
- Forward data packets towards their correct destination
- Return error messages in cases where a data packet cannot be delivered
- Coalesce forwarding table entries for networks that are adjacent and on the same port
- Serialize your forwarding table so that it can be checked for correctness

### Description
A Border Gateway Protocol (BGP) Router is a hardware box that exchanges routing and reachability information among Autonomous Systems (AS). A network administrator would plug cables into BGP ports that connect to neighboring BGP routers, either from the same AS or another one.

The Administrator is responsible for manually configuring each port by 1) choosing the IP address that the router uses, and 2) choosing whether this port leads to a provider, peer, or customer. After this manual configuration is complete, the administrator turns on the router and contacts its neighbors and establishes BGP sessions. The neighboring routers can pass BGP protocol messages to each other, as well as pass data packets from internet users.

The router's job is to keep its forwarding table up-to-date, based on the BGP protocol messages, and also keep neighbor's forwarding tables up to date by sending BGP protocol messages to them, as well as forwarding data packets to their correct destination.

The program will open several Unix domain sockets, each corresponding to a port in the router. The router will receive messages on sockets, either a BGP command from the given neighbor or a data packet that the router must forward to the correct destination.

The command line indicates 1) the IP address used on the port, 2) the type of relationship the router has with the neighboring router:
```
./router <asn> <ip.add.re.ss-[peer,prov,cust]> [ip.add.re.ss-[peer,prov,cust]] ...[ip.add.re.ss-[peer,prov,cust]]
```

All neighboring routers have IP addresses of the form of `*.*.*.2` and all IP addresses used by the router are in the form of `*.*.*.1`.

The configuration files specify the routers that will neighbor the router in each simulation, as well as the messages being sent. The list of networks are neighboring networks, as well as their AS number, network prefix, netmask, and type.

#### Connecting to neighbors
Use UNIX domain sockets to connect to neighboring routers, one domain socket per neighbor. Packets are passed between programs on the local machine through program sending and receiving data from the simulator.

#### Handling multiple sockets
Use select() or poll() on all domain sockets that the router is connected to in order to make code single-threaded and easy to debug.

#### Messages
All messages will be in JSON format:
```
{
  "src": "<source IP>",
  "dst":   "<destination IP>",
  "type":   "<update|revoke|data|no route|dump|table>",                   
  "msg": {...}
}
```

##### Route Update Messages
Instructs router on how to forward data packets to destination on the internet. When received, the router 1) saves a copy of the announcement, 2) adds an entry to your forwarding table, and 3) sends copies of the announcement to neighboring routers.

The router should store all the information in route announcement. If the update is received from a customer, send updates to all other neighbors. Else, if the update is received from a peer or provider, send updates to your customers.
##### 