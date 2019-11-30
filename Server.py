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
conn, addr = server.accept() # Establish connection with client.
print ('Got connection from', addr)
data = str("").encode()
while True:
    try:  
        rdata = conn.recv(1024)
        if not rdata: 
            break
        data+=rdata;
        print('Server received', repr(rdata))
        timesdatasend = timesdatasend+1;
        print("Client send this many times ",timesdatasend);
    except Exception:
        print("Something broke")
    finally:
        server.close();

data = data.split(b'FILENAME:')
for i in range(1,len(data)):
    filename, data_to_save = data[i].split(b'DATA:')
    filename = filename.decode('utf-8')
    myFile = open("compressed/"+filename, 'wb')
    myFile.write(data_to_save)
    myFile.close()
    print(filename," fylder ", len(data_to_save)," bytes nu")
