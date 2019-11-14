from socket import *
import sys
import csv


timesdatasend = 0;

server = socket(AF_INET,SOCK_STREAM)
ipadresse= gethostbyname(gethostname());
print (ipadresse);
server.bind(('',9997))
print (server);
server.listen(3);
conn, addr = server.accept()     # Establish connection with client.
print ('Got connection from', addr)
while True:
    try:
        rdata = conn.recv(1024)
        if not rdata: break
        if timesdatasend == 0:
            data=rdata;
        else:
            data+=rdata;
        
        print('Server received', repr(rdata))
        timesdatasend = timesdatasend+1;
        print("Client send this many times ",timesdatasend);
    except Exception:
        print("Something broke")
    finally:
        server.close();
        
        
myFile = open('csvdata.csv', 'w')
print(len(data))
strdata=str(data);
#strdata=strdata.replace('b','');
#strdata=strdata.replace('\'','');
with myFile:
    writer = csv.writer(myFile)
    myBitLenght=12;
    while myBitLenght < len(strdata):
        oneRow=strdata[0:myBitLenght];
        strdata=strdata.replace(strdata[0:myBitLenght],'');
        writer.writerow(oneRow);

