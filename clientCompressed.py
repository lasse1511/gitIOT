def send():

    import socket
    import sys
    import os
    s = socket.socket()
    s.connect(('192.168.0.102',9997))

    totBits = 0
    x = 1
    dataStr = ""
    for filename in os.listdir('compressed'):
        filenametosend=str("FILENAME:"+filename).encode()
        totBits+=len(filenametosend)
        s.send(filenametosend)
        dataStr+=str(filenametosend)
        print(filenametosend)
        f = open ("compressed/"+filename, "rb")
        l = f.read(1024)
        # print('Byte file: ', l)
        # print('Length of file: ', len(l))
        while (l):
            data = l
            print('Sending data ', x, " with length: ", len(data))
            x = x+1
            totBits = totBits+ len(data)
            s.send(data)
            print(data)
            dataStr+=str(l)
            l = f.read(1024)
    print('Closing connection')
    s.close()
    print(dataStr.split("b'FILENAME"))
    print("Total bits send: ", totBits)
    print(len(dataStr))