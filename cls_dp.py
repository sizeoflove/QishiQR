# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:01:45 2018

@author: rl17174
"""

from abc import ABCMeta, abstractmethod

class DataProc(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def read_data(self): 
        """
        Read in data
        """
        raise NotImplementedError("Should implement read_data(self)")

    @abstractmethod
    def split_data(self): 
        """
        Split data to training & testing
        """
        raise NotImplementedError("Should implement data_split(self)")
        
    @abstractmethod
    def clean_data(self): 
        """
        Read in data
        """
        raise NotImplementedError("Should implement clean_data(self)")