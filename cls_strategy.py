# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:39:33 2018

@author: rl17174
"""

from abc import ABCMeta, abstractmethod

class Strategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_signal(self): 
        """
        Provides the mechanisms to calculate the list of signals.
        """
        raise NotImplementedError("Should implement calculate_signals()")
        
        
        
