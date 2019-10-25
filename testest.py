# f = open ("unpacked/08730_01.csv", "rb")
f = open ("compressed/params.gd.npy", "rb")

l = f.read()
print(l)
i = 0;
while(l):
    i = i+1
    l = f.readline()
print(i)