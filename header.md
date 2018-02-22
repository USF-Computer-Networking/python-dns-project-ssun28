# Header of the DNS request:
| name          | length  |
| ------------- | ------- |
| tansaction ID | 2 bytes |
| QR            | 1 bit   |
| Opcode        | 4 bits  |
| AA            | 1 bit   |
| TC            | 1 bit   |
| RD            | 1 bit   |
| RA            | 1 bit   |
| X             | 3 bits  |
| Response code | 4 bits  |
| QDCOUNT       | 2 bytes |
| ANCOUNT       | 2 bytes |
| NSCOUNT       | 2 bytes |
| ARCOUNT       | 2 bytes |

# Message compression
- first 2 bits are 1
- offset (10 bits): the bit which we will begin to compress

#
