## A simple DNS Server

* Make our own DNS Server from scratch without any 3rd party libraries
* Differences between UDP and TCP
* DNS Headers and how each of the different types of headers will affect how our requests are interpreted
*  DNS compression
* How to send responses from the server to the client whenever we receive a DNS Request
* Be implementing the header section of the DNS response
* Setting the question count in the response
* Loading our zone files into our server when it boots up

**More details can be found at [https://www.ietf.org/rfc/rfc1035.txt](https://www.ietf.org/rfc/rfc1035.txt) .**

#### command:
    one terminal: $ sudo python3 dns.py
    another terminal: $ dig www.google.com@127.0.0.1
