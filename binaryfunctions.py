#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 09:31:29 2019

@author: rv
"""

import numpy as np

def _fix_sign(x):
    if x[0] == '-':
        x = '1' + x[1:]
    return x

def float_to_int_16(x):
    """
    Convert a float to 16-bit integer
    """
    return np.float16(x).view(np.int16)

def float_to_int_32(x):
    """
    Convert a float to 32-bit integer
    """
    return np.float32(x).view(np.int32)

def float_to_int_64(x):
    """
    Convert a float to 64-bit integer
    """
    return np.float64(x).view(np.int64)

def float_to_int(x, prec=64):
    """
    Convert a float to integer with precision prec
    """
    if prec == 16: return float_to_int_16(x)
    elif prec == 32: return float_to_int_32(x)
    elif prec == 64: return float_to_int_64(x)
    else: raise ValueError

def int_to_binary(x, n=64):
    """
    Convert an integer to an n-bit binary number
    """
    return format(x, 'b').zfill(n)

def float_to_binary(x, n=64):
    """
    Convert a float to an n-bit binary number
    """
    return _fix_sign(int_to_binary(float_to_int(x, n), n))

def row_to_binary(row):
    """
    Convert each float in a pandas.dataframe column to binary representation.
    """
    binaryrow = ''
    for item, val in row.iteritems():
        binaryrow += float_to_binary(val)
    return binaryrow

def binary_string_to_gf_elements(b, m_gf):
    """
    Convert a binary string to elements of the field GF(2**m_gf).
    """
    if m_gf == 1:
        return np.fromiter(map(int, b), int)
    else:
        assert(len(b)%m_gf == 0)
        res = np.zeros(len(b)//m_gf)
        for i in range(len(b)//m_gf):
            res[i] = int(b[i*m_gf:(i+1)*m_gf], 2)
        return res.astype(int)
    
def binary_strings_to_gf_array(data, m_gf):
    data_out = []
    for val in data:
        data_out.append(binary_string_to_gf_elements(val, m_gf))
    return np.array(data_out,dtype=int)
    
def array_to_gf_array(data, m_gf = 1, floatprec = 64):
    """
    Convert an array of floats to their representation in GF(2**m_gf). 
    
    Parameters
    ----------
    data : array
        Data to convert
    m_gf : int, default 1
        Galois field to convert data to
    floatprec : int
        Number of bits for float representation
    """
    data_binary = []
    for val in data:
        data_binary.append(binary_string_to_gf_elements(float_to_binary(val, floatprec), m_gf))
    return np.array(data_binary,dtype=int)

def gf_array_to_binary(data, m_gf):
    data_binary = []
    for val in data:
        data_binary.append(''.join([int_to_binary(element, n=m_gf)  for element in val]))
    return data_binary
        
    
def interleave(data, num_to_move=8, move_when=24, floatprec = 32):
    assert num_to_move + move_when == floatprec
    assert num_to_move % 2 == 0
    move_number = num_to_move // 2
    data_gf = array_to_gf_array(data, m_gf=2, floatprec = floatprec)
    data_gf = data_gf.ravel()
    
    moves_start = np.arange(move_when//2, len(data_gf), floatprec//2)
        
    to_move = np.zeros_like(data_gf)
    for i in moves_start:
        to_move[i:i+move_number] = 1
    to_move = np.where(to_move == 1)[0]    
    to_stay = [i for i in np.arange(len(data_gf)) if i not in to_move]
        
    data_new = np.hstack((data_gf[to_stay], data_gf[to_move]))
    return gf_array_to_binary(data_new.reshape(len(data), -1), 2)

def array_to_gf_array_interleave(data, num_to_move, move_when, m_gf, floatprec=32):
    return binary_strings_to_gf_array(interleave(data, num_to_move, move_when, floatprec), m_gf)

def intarray_to_binary(data, resolution):
    return binary_strings_to_gf_array([int_to_binary(v,resolution) for v in data],1)

def binary_to_int(binarray):
    out = 0
    for bit in binarray: 
        out = (out << 1) | bit
    return out

if __name__ == '__main__':
    """
    Example on how to transform data
    """
#    print(array_to_gf_array_interleave([1.0001,1.0002], 8, 24 , m_gf=1, floatprec=32))
    print(array_to_gf_array([1.0001,1.0002], 1, floatprec=32))