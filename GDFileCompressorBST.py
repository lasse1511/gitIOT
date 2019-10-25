#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:54:01 2019

@author: rv
"""

import os
import pandas as pd
import numpy as np
import scipy.stats as ss

import binaryfunctions as bf
from EliasGammaCoding import EliasGammaEncode, EliasGammaDecode
import BinarySearchTree as BST

class FileCompressor():
    def __init__(self, outfolder='/compressed/', correlation_method = np.max):
        self.reordering = None
        self.cwd = os.getcwd()
        if outfolder[0] != '/': outfolder = '/' + outfolder
        self.outfolder = self.cwd + outfolder
        self.corrmethod = correlation_method
        try: 
            os.makedirs(self.outfolder)
        except:
            pass    
        
    def initialize_from_file(self, file):
        """
        Not implemented at this moment.
        """
        pass
    
    def initialize_from_parameters(self, k, l):
        self.k = k
        self.l = l
        self.n = k+l
        self.bases = BST.BinarySearchTree()
    
    def _estimate_entropy(self, data):
        """
        Estimates entropy of a data set.
        """
        uniques, counts = np.unique(data, axis=0, return_counts=True)
        return ss.entropy(counts/uniques.shape[0], base=2)
    
    def _estimate_reordering(self, data):
        """
        Estimates reordering using correlation of columns in data.
        """
        filedf = pd.DataFrame(data)
        corrs = filedf.corr()
        var_corr = self.corrmethod(np.abs(corrs)-np.eye(len(corrs)), axis=0)
        return np.argsort(np.array(var_corr))[::-1]
       
    def _bits_for_base_repr(self, largest_idx):
        """
        Calculates the number of bits required to represent all bases
        """
        return np.ceil(np.log2(1+largest_idx)).astype(int)
    
    def compress(self, filedata):
        """
        Compresses a particular array.
        """
        if type(self.reordering) == type(None):
            ### Determine how to reorder the data acoording to Mutual Information,
            ### if we don't already know.
            self.reordering = self._estimate_reordering(filedata)
            
        ### Reorder the data according to correlation
        data = filedata[:,self.reordering]
        
        ### Split the data
        file_bases = data[:,:self.k]
        file_deviations = data[:,self.k:]
        file_base_idx = np.zeros(file_bases.shape[0], dtype=int)
        
        ### Deduplicate the bases
        for i, base in enumerate(file_bases):
            file_base_idx[i]  = self.bases.insert(base)
        
        ### Represent base idx's as binary
        base_idx_repr_len = self._bits_for_base_repr(max(file_base_idx))
        file_base_idx_ = bf.intarray_to_binary(file_base_idx, base_idx_repr_len)

        ### Interleave bases and deviations for storage.
        gd_data = np.hstack((file_base_idx_, file_deviations))
        gd_data = gd_data.ravel()
 
        ### Add base_repr_length to stored file, using EliasGamma code:
        if base_idx_repr_len == 0:
            return gd_data
        gd_data = np.hstack((EliasGammaEncode(base_idx_repr_len), gd_data))
        return gd_data
    
    def CompressFile(self, file, deltas = False):
        """
        Performs the full operation required to compress a file.
        """
        try:
            filedata = np.genfromtxt(file, delimiter=',')
        except:
            filedata = np.load(file)
            
        if filedata.size%self.n:
            filedata = np.hstack((filedata.ravel(), np.zeros(self.n - filedata.size%self.n)))
        filedata = filedata.astype(int).reshape(-1, self.n)
        if deltas:
            n_s = 12
            c = self.n//n_s
            ### ONE APPROACH: Deltas from first sample
            """
            first_sample = filedata[:,0:n_s]
            for i in range(1, c):
                i_delta = first_sample ^ filedata[:,i*n_s:(i+1)*n_s]
                filedata[:,i*n_s:(i+1)*n_s] = i_delta
            """
            ### OTHER APPROACH: Cumulative deltas
            """
            order = np.arange(1, c)[::-1]
            for i in order:
                previous = filedata[:,(i-1)*n_s:(i)*n_s]
                i_delta = previous ^ filedata[:,i*n_s:(i+1)*n_s]
                filedata[:,i*n_s:(i+1)*n_s] = i_delta
            """
        out = self.compress(filedata)
        print("Outfolder: ", self.outfolder)
        np.save(self.outfolder+"params.gd", np.hstack((np.array([self.k, self.l]), self.reordering)))
        np.save(self.outfolder+"bases.gd", np.packbits(self.bases.serialize().astype(int)))
        np.save(self.outfolder+"usage.gd", self.bases.usage())
        np.save(self.outfolder+"compressedfile"+".gd", np.packbits(out))
        
    def CompressFolder(self, folder):
        """
        Compresses all files in a folder.
        """
        files = os.listdir(folder)
        files.sort()
        for file in files:
            C.CompressFile(folder+file)
        
    def _extract_base_repr_length(self, filedata):
        """
        Decodes how long the base representations are in a given compression,
        and removes the Elias-Gamma coding in the first 2floor(log2(x)) +1 bits
        """
        length = EliasGammaDecode(filedata)
        filedata = filedata[int(2*np.floor(np.log2(length))) + 1:]
        return length, filedata

    def extract(self, filedata):
        """
        Performs the full decompression operation.
        """
        length, filedata = self._extract_base_repr_length(filedata)
        real_data_len = len(filedata)-len(filedata)%(length+self.l)
        filedata = filedata[:real_data_len]
#        filedata = filedata[:-(filedata.shape[0]%8)]
        filedata = filedata.reshape(-1, length+self.l)

        ### Decode bases
        coded_bases = filedata[:, :length]
        base_idx = [bf.binary_to_int(coded_base) for coded_base in coded_bases]
        decoded_bases = self.bases[base_idx]
        
        ### Combine with deviations
        deviations = filedata[:, length:]
        data = np.hstack((decoded_bases, deviations))

        ### Rearrange to standard configuration
        redo_ordering = [0]*(C.k+C.l)
        for i, j in enumerate(C.reordering):
            redo_ordering[j] = i
        data = data[:, redo_ordering]

        return data
    
    def ExtractFile(self, file):
        """
        Performs the full operation required to decompress a file.
        """
        bases = np.unpackbits(np.load(self.outfolder+'bases.gd.npy'))
        bases = bases[:len(bases)-len(bases)%self.k]
        self.bases = bases.reshape(-1, self.k)
        filedata = np.unpackbits(np.load(file))

        out = self.extract(filedata)
        np.savetxt(file+".out", out, delimiter=",", fmt='%d')

def AssertFileEquality(fileA, fileB):
    """
    Checks that two files contain the same data.
    """
    dataA = np.genfromtxt(fileA, delimiter=',').astype(int)
    dataB = np.genfromtxt(fileB, delimiter=',').astype(int)
    dataA = dataA.reshape(1,-1).ravel()
    dataB = dataB.reshape(1,-1).ravel()
    assert(np.alltrue(np.equal(dataA, dataB)))
    
if __name__ == '__main__':
    cwd = os.getcwd()
    infolder = cwd + '/unpacked/'
    outfolder = 'compressed/'
    C = FileCompressor(outfolder)
    
    bits_per_sample = 12
    num_concat = 4
    l = 10
    C.initialize_from_parameters(k = bits_per_sample*num_concat - l, l = l)
    
    ### Compress an entire folder at once
    C.CompressFolder(infolder)
#    
    ### Or compress files individually
    C.CompressFile(infolder+'08730_01.csv')
    C.CompressFile(infolder+'08730_03.csv')
    C.CompressFile(infolder+'08730_02.csv')
    
    ### Extract the output files
    C.ExtractFile(outfolder+'08730_01.csv.gd.npy')
    C.ExtractFile(outfolder+'08730_02.csv.gd.npy')
    C.ExtractFile(outfolder+'08730_03.csv.gd.npy')
    
    AssertFileEquality(infolder+'08730_01.csv', outfolder+'08730_01.csv.gd.npy.out')
    AssertFileEquality(infolder+'08730_02.csv', outfolder+'08730_02.csv.gd.npy.out')
    AssertFileEquality(infolder+'08730_03.csv', outfolder+'08730_03.csv.gd.npy.out')
    
    print("Test passed - extracted files equal the input!")