import clientCompressed as c;
import os
from GDFileCompressorBST import FileCompressor
import GDFileCompressorBST as gd
import time 

directory = "unpacked/"
compressedDirectory = "compressed/"

f = FileCompressor()
f.__init__()
f.initialize_from_parameters(29,19)

start = time.time()
for filename in os.listdir(directory):
    size = 0
    file = open (directory + filename)
    f.CompressFile(file)
    # c.send(compressedDirectory)
    # os.remove()
    # for file in os.listdir(compressedDirectory):
        # size += os.path.getsize('./' + compressedDirectory + file)
    # print(size + " bytes")
end = time.time()
print("Time elapsed: ", end - start)

# for file in os.listdir(compressedDirectory):
#     if ("08730" in file):
#         f.ExtractFile(compressedDirectory+file)
#         n = file.split(".")
#         unpacked_file = n[0] + "." + n[1]
#         print(gd.AssertFileEquality(directory+unpacked_file, compressedDirectory+file+".out"))




# c.send("compressed");
