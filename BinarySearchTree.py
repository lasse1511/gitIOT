#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:17 2019

@author: rv
"""

import numpy as np

class Base():
    def __init__(self, input_array):
        self.array = input_array
        self.usage = 1

    def __lt__(self, other):
        diff = (self.array ^ other.array).argmax()
        return self.array[diff]<other.array[diff]
        
    def __gt__(self, other):
        diff = (self.array ^ other.array).argmax()
        return self.array[diff]>other.array[diff]
    
    def __repr__(self):
        return "{}, {}".format(self.array, self.usage)
    
    
class BinarySearchTree():
    def __init__(self):
        self.root = None
        self.nextID = 1
        
    def insert(self, data):
        if self.root is None:
            self.root = BSTNode(Base(data), 0)
            return 0
        else:
            assigned_id = self.root.insert(Base(data), self.nextID)
            if assigned_id == self.nextID:
                self.nextID += 1
            return assigned_id
    
    def serialize(self):
        bases, order = self.root.serialize()
        return bases[np.argsort(order)]
    
    def usage(self):
        bases, order = self.root.serialize()
        usages = self.root.get_usages()
        return np.array(usages)[np.argsort(order)]
    
class BSTNode():
    def __init__(self, data, ID):
        self.left = None
        self.right = None
        self.data = data
        self.ID = ID
        
    # Insert method to create nodes
    def insert(self, data, newID):
        """
        Insert method to creat new nodes.
        
        Returns:
        --------
        True if new element was inserted.
        False if element already existed.
        """
        if data < self.data:
            if self.left is None:
                self.left = BSTNode(data, newID)
                return self.left.ID
            else:
                return self.left.insert(data, newID)
        elif data > self.data:
            if self.right is None:
                self.right = BSTNode(data, newID)
                return self.right.ID
            else:
                return self.right.insert(data, newID)
        else: 
            # Then we must be equal to!
            self.data.usage += 1
            return self.ID
            
    def serialize(self):
        """
        Serializes the BST.
        """
        if self.left:
            l, l_id = self.left.serialize()
        else: 
            l = np.zeros((0, self.data.array.size))
            l_id = []
        d = self.data.array[np.newaxis,:]
        d_id = [self.ID]
        if self.right:
            r, r_id = (self.right.serialize())
        else: 
            r = np.zeros((0, self.data.array.size))
            r_id = []
        return np.vstack((l,d,r)), l_id+d_id+r_id
    
    def get_usages(self):
        """
        Extracts how many times each node (base) is used.
        """
        if self.left:
            l_usage = self.left.get_usages()
        else:
            l_usage = []
        my_usage = [self.data.usage]
        if self.right:
            r_usage = self.right.get_usages()
        else:
            r_usage = []
        return l_usage+my_usage+r_usage
        
    
if __name__ == '__main__':
    base1 = np.array([0,0,0])
    base2 = np.array([1,1,1])
    base3 = np.array([0,1,0])
    
    BST = BinarySearchTree()
    BST.insert(base3)
    BST.insert(base2)
    BST.insert(base2)
    BST.insert(base2)
    BST.insert(base1)
    BST.insert(base1)
    serialized = BST.serialize()
    usages = BST.usage()
    
    print(serialized)
    print(usages)