
# # import os
# # import pandas as pd
# # import numpy as np
# # import scipy.stats as ss

# from GDFileCompressorBST import FileCompressor

# file = open ("unpacked/08730_01.csv", "rb")

# f = FileCompressor();
# f.__init__()
# f.initialize_from_parameters(10,5)
# print(f.CompressFile(file))
import numpy as np

# f = np.load("compressed/params.gd.npy")


f = open("compressed/bases.gd.npy", "rb")
l = f.read(1024)
print(l)
f1 = open("compressed/bases1.gd.npy", "wb")
f1.write(l)
