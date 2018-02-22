#!/usr/bin/env python
""" dns.py
    A simple DNS Server program.
    Make our own DNS Server from scratch without any 3rd 
    party libraries.
    Be manipulating individual bit's when our sever responds to queries.
    reference: https://www.youtube.com/watch?v=HdrPWGZ3NRo&index=1&list=PLBOh8f9FoHHhvO5e5HF_6mYvtZegobYX2
    
    Shihao Sun
"""
# Using UDP protocol
import socket
import glob
import json

# DNS server using Port 53 by default, when we use dig command it will send
# request to port 53
port = 53

# ip address of the look back
ip = '127.0.0.1'

# socke.AF_INET is for ipv4
# socket.SOCK_DGRAM  is for UDP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))


def loadZone():
    jsonZone = {}
    zoneFiles = glob.glob('zones/*.zone')

    for zone in zoneFiles:
        with open(zone) as zoneData:
            data = json.load(zoneData)
            zoneName = data["$origin"]
            jsonZone[zoneName] = data

    return jsonZone

zoneData = loadZone()

def getFlags(flags):
    rFlags = ''

    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])

    # first byte of the response
    # the QR for the response always be 1
    QR = '1'
    OPCODE = ''
    for bit in range(1, 5):
        OPCODE += str(ord(byte1) & (1 << bit))

    AA = '1'
    TC = '0'
    RD = '0'

    # second byte of the response
    RA = '0'
    Z = '000'
    RCODE = '0000'


    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder = 'big') \
    + int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')


def getQuestionDomain(data):
    print('data=',data)
    x = 0
    y = 0
    state = 0
    expectedLength = 0
    domainString = ''
    domainParts = []
    for byte in data:
        if state == 1:
            if byte != 0:
                 domainString += chr(byte)
            x += 1
            if x == expectedLength:
                domainParts.append(domainString)
                domainString = ''
                state = 0
                x = 0
            if byte == 0:
                domainParts.append(domainString)
                break
        else:
            state = 1
            expectedLength = byte
        y += 1

    questionType = data[y : y + 2]
    print('domainParts=',domainParts)
    print('questioType=',questionType)
    return (domainParts, questionType)

def getZone(domain):
    global zoneData
    zoneName = '.'.join(domain)
    return zoneData[zoneName]

def getRecs(data):
    domain, questioType = getQuestionDomain(data)
    qt = ''
    if questioType == b'\x00\x01':
        qt = 'a'

    zone = getZone(domain)
    return (zone[qt], qt, domain)

def buildQuestion(domainName, recType):
    qBytes = b''

    for part in domainName:
        length = len(part)
        qBytes += bytes([length])

        for char in part:
            qBytes += ord(char).to_bytes(1, byteorder='big')

    if recType == 'a':
        qBytes += (1).to_bytes(2, byteorder = 'big')

    qBytes += (1).to_bytes(2, byteorder = 'big')

    return qBytes

def rectTobytes(domainName, recType, recttl, recval):
    rBytes = b'\xc0\x0c'

    if recType == 'a':
        rBytes = rBytes + bytes([0]) + bytes([1])

    rBytes = rBytes + bytes([0]) + bytes([1])

    rBytes += int(recttl).to_bytes(4, byteorder= 'big')

    if recType == 'a':
        rBytes = rBytes + bytes([0]) + bytes([4])

        for part in recval.split('.'):
            rBytes += bytes([int(part)])
    return rBytes


def buildResponse(data):
    # transaction ID
    transactionID = data[:2]
    TID = ''
    for byte in transactionID:
        TID += hex(byte)[2:]

    print('TID=',TID)

    # Get the flags
    flags = getFlags(data[2:4])

    print('flags', flags)

    # Question Count
    # binary format of hex number 1
    QDCOUNT = b'\x00\x01'

    # Answer Count
    ANCOUNT = len(getRecs(data[12:])[0]).to_bytes(2, byteorder = 'big')
    print('ANCOUNT= ',ANCOUNT)
    # NameServer Count
    NSCOUNT = (0).to_bytes(2, byteorder = 'big')

    # Additional Count
    ARCOUNT = (0).to_bytes(2, byteorder = 'big')

    dnsHeader = transactionID + flags + QDCOUNT \
    + ANCOUNT + NSCOUNT + ARCOUNT

    dnsBody = b''

    # Get answer for query
    records, recType, domainName = getRecs(data[12:])


    # Get DNS question
    dnsQuestion = buildQuestion(domainName, recType)


    for record in records:
        dnsBody += rectTobytes(domainName, recType, record["ttl"], record["value"])

    return dnsHeader + dnsQuestion + dnsBody


while 1:
    ## When less or equal to 512 is better to use UDP
    data, addr = sock.recvfrom(512)
    response = buildResponse(data)
    sock.sendto(response,addr)
