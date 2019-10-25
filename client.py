import socket
import sys

s = socket.socket();
s.connect(('192.168.0.102',9998))
f = open ("../../Downloads/GDProjectMaterial/unpacked/08730_01.csv", "rb")
l = f.read(1024)
x = 1;
while (l):
    dataToSend = '';
    index = 0;
    #print("This is l",l)
    data = str(l)
    for i in data:
        try:
            dataToSend = dataToSend +(str(int(i)));
            index = index + 1;
        except ValueError:
            continue;
    data = str.encode(dataToSend)
    #print("This is new l:",data);
    
    print('Sending data ', x);
    x = x+1;
    s.send(data)
    l = f.read(1024)
s.close()