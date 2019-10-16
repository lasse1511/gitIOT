import socket
import sys

s = socket.socket();
s.connect(('192.168.0.102',9998))
f = open ("../Downloads/GDProjectMaterial/unpacked/08730_01.csv", "rb")
l = f.read(1024)
dataToSend = '';
index = 0;
print("This is l",l)
l = str(l)
for i in l:
    try:
        dataToSend = dataToSend +(str(int(i)));
        index = index + 1;
    except ValueError:
        continue;
l = str.encode(dataToSend)
print("This is new l:",l);
while (l):
    s.send(l)
    l = f.read(1024)
s.close()