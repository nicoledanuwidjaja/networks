## Project 4: Simple Transport Protocol
### Approach
We decided to design our packet as a struct which contained (sequence number, eof). Using this information, we passed the data packets between the senders and receivers, each having their own ability to receive packets unreliably. Our approach was to use the maximum data size per packet to create a stream of packets, each identified with a specific sequence number, so that the data could be passed correctly. In addition, we also implemented congestion avoidance using the slow start and sliding window techniques.

### Challenges
It was difficult to come up with a solid strategy for the overall design of the transport protocol. We initially struggled with the packet design, and then for the majority of the project, worked on the successful transferring and handling of the different acknowledgement (ACK) signal types, such as duplicated, reordered, dropped, and delayed acks. Each of these came with their own complexities, and we worked on using existing protocols to mitigate congestion. 

## Details
Design a simple transport protocol that provides reliable datagram service which ensures that data is delivered in order, without duplicates, missing data, or errors.

Design a custom packet format and use UDP as transport layer protocol with `socket.sendto()`. The sending program should accept data and send it across the network, and receive data and print it out in-order.

### Acceptance Criteria 
- Sender must accept data from STDIN and send data until EOF
- Sender and receiver must work together to transmit data reliably
- Receiver must print out received data to STDOUT in order without errors
- Sender and receiver must print out specified debugging messages to STDERR
- Sender and receiver must gracefully exit

The Transport Protocol should be able to transfer a file with any number of packets dropped, duplicated, and delayed, under a variety of different available bandwidths and link latencies. Datagrams generated must contain less than or equal to 1472 bytes of data per datagram. (1500 Ethernet MTU - 20 Byte IP Header - 8 Byte UDP Header)

Desirable properties include speed of file transfer and low data volume overhead to be exchanged over the network, including data bytes, headers, retransmissions, acknowledgements, etc.

### Sender
The sender must open a UDP socket to the given IP address on the given port. The data that the sender must transmit to the receiver must be supplied in STDIN. The sender must read in the data from STDIN and transmit it to the receiver via the UDP socket.

### Receiver
The receiver must bind to the specific UDP port and wait for datagrams from the sender. The receiver program must print out the data it receives from the sender to STDOUT. The data it prints must be identical to the data supplied to the sender via STDIN. Data can not be missing, reordered, or contain any bit-level errors.

Debug information is printed out via STDERR.