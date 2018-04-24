# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 19:12:54 2018

@author: rl17174
"""

from cls_portfolio import Portfolio

class EqualWeightPort(Portfolio):
    def __init__(self, signal):
        self.sig = signal
        
    def get_position(self):
        self.position = self.sig.dropna().copy()
        self.position = self.position.apply(lambda x: 1 if x == '2' else -1)
        self.position.name = 'position'