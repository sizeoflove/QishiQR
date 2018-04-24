# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:07:10 2018

@author: rl17174
"""

from cls_dp import DataProc
import pandas as pd

class DataProcSpot(DataProc):
    def __init__(self, file_name, p_str = 'Adj Close'):
        self.file_name = file_name
        self.p_str     = p_str
        self._read_data()
        self._clean_data()
        
    def split_data(self, cutoff_date): 
        self.train = self.data[cutoff_date[0][0]:cutoff_date[0][1]][self.p_str].copy()
        self.test  = self.data[cutoff_date[1][0]:cutoff_date[1][1]][self.p_str].copy()
    
    def _read_data(self): 
        self.data = pd.read_csv(self.file_name, index_col = [0], parse_dates=[0], 
                   na_values=['null'])
        
    def _clean_data(self): 
        self.data = self.data.sort_index().dropna(subset=[self.p_str])
        self.data = self.data[self.data[self.p_str].shift()!=self.data[self.p_str]]
