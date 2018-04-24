# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 19:11:30 2018

@author: rl17174
"""

from abc import ABCMeta, abstractmethod

class Portfolio(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_position(self, signal):
        raise NotImplementedError("Should implement get_position()")