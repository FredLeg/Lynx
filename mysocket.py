#! C:\python34\python

import socket

fp = open('mysockets_hosts.txt')
i=0
for line in fp:
    host = line.strip()
    i += 1
    print("{} Host: {}  IP: {}".format(i, host, socket.gethostbyname(host))) # socket.gethostbyname(host)
print("TheEnd")
