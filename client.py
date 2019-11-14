def send():

    import socket
    import sys
    s = socket.socket();
    s.connect(('192.168.0.102',9997))
    f = open ("unpacked/08730_01.csv", "rb")
    l = f.read(1024)
    print('Length of file: ', len(l))
    x = 1;
    totBits = 0;
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
        
        print('Sending data ', x, " with length: ", len(data));
        x = x+1;
        totBits = totBits+ len(data);
        s.send(data)
        l = f.read(1024)
    print('Closing connection')
    s.close()
    print("Total bits send: ", totBits)
