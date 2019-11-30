def send(fileDirectory):

    import socket
    import sys
    import os
    s = socket.socket()
    s.connect(('192.168.0.102',9997))

    totBits = 0
    x = 1
    dataStr = ""
    for filename in os.listdir(fileDirectory):
        filenametosend=str("FILENAME:"+filename+"DATA:").encode()
        print(filenametosend)
        s.send(filenametosend)
        f = open (fileDirectory+filename, "rb")
        l = f.read(1024)
        while (l):
            data = l
            x = x+1
            totBits = totBits+ len(data)
            s.send(data)
            dataStr+=str(l)
            l = f.read(1024)
    s.close()