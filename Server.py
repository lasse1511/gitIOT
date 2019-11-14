from socket import *
import sys
import csv


timesdatasend = 0;
filename="";

server = socket(AF_INET,SOCK_STREAM)
ipadresse= gethostbyname(gethostname());
print (ipadresse);
server.bind(('',9997))
print (server);
server.listen(10);
conn, addr = server.accept()     # Establish connection with client.
print ('Got connection from', addr)
data = str("").encode()
while True:
    try:
        rdata = conn.recv(1024)
        if not rdata: break
        data+=rdata;

        print('Server received', repr(rdata))
        timesdatasend = timesdatasend+1;
        print("Client send this many times ",timesdatasend);
    except Exception:
        print("Something broke")
    finally:
        server.close();
#if type(rdata)==str and title=false:
#data=str(data)
data = data.split(b'FILENAME:')
print("Dette er vores array af filnavne:" , data)
print("Deete har jeg modtager", data)
print("Længden af data", len(data))
print("Længden af data str", len(str(data).encode()))
data=data.replace("\'b\'","")
print(len(data.split("b")))
data=data.split("FILENAME")
print("Længden af data-array", len(data))
for x in data:
    if (x[0]==':'):
        index = x.split("\\")
        filename=index[0]
        filename=filename[1:]
        
        data_to_save = str(x[len(filename)+1:]).encode()
        #print(filename, data_to_save)
        myFile = open(filename, 'wb')
        myFile.write(data_to_save)
        myFile.close()
        print(data_to_save)
        print(len(x))
        print(filename," fylder ", len(data_to_save)," bits nu")
    



