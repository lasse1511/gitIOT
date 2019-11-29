import clientCompressed as c;
import os
from GDFileCompressorBST import FileCompressor


directory = "unpacked/"
(os.listdir(directory)[0])


f = FileCompressor();
f.__init__()
f.initialize_from_parameters(29,19)

for filename in os.listdir(directory):
    size = 0
    file = open (directory + filename)
    f.CompressFile(file)
    files = os.listdir("compressed/")
    for file in files:
        size += os.path.getsize('./compressed/' + file)
    print(size )






# c.send();
