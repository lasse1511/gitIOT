from socket import *
import sys
import csv

server = socket(AF_INET,SOCK_STREAM)
ipadresse= gethostbyname(gethostname());
print (ipadresse);
server.bind(('',9998))
print (server);
server.listen(3);

while True:
    conn, addr = server.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    data = conn.recv(2048)
    print('Server received', repr(data))
    myFile = open('csvdata.csv', 'w')
    strdata=str(data);
    strdata=strdata.replace('b','');
    strdata=strdata.replace('\'','');
    with myFile:
       writer = csv.writer(myFile)
       myBitLenght=8;
       
       while myBitLenght < len(strdata):
           oneRow=strdata[0:myBitLenght];
           strdata=strdata.replace(strdata[0:myBitLenght],'');
           writer.writerow(oneRow);
    
    

server.close();

