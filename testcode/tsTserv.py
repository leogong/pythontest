from _socket import SOCK_STREAM
from _socket import AF_INET
from socket import socket
from time import ctime

__author__ = 'leo'

# blank means any host can connect
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
#max connections
tcpSerSock.listen(5)

while True:
    print 'Waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send('[%s] %s' % (ctime(), data))

    tcpCliSock.close()
tcpSerSock.close()




