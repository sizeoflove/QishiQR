# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:25:09 2018

@author: rl17174
"""

import os
import pandas as pd
from collections import defaultdict
from operator import itemgetter

class FutureContracts(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.chain_data()
         
    def chain_data(self):
        """Put data together.
        Args:
            main_contracts: list of lists or ndarray, with dim(-1, 2).
            data_dir: data directory.
        Returns:
            DataFrame: chained data.
        """
        self._get_main_contracts()
        
        df_all = (pd.read_csv(os.path.join(self.data_dir, '{}_{}.csv'.format(mc, date))) 
                  for date, mc in self.main_contracts)
        self.df_data = pd.concat(df_all, ignore_index=True)
    
    def _get_acc_volume(self, file):
        """Read the last line of a specific file and get its accumulative volume.
        Args:
            file: commodity future data file.
        Returns:
            A float number represents AccVolume in the last line of data file.
        """  
        with open(file, 'rb') as f:
            f.seek(-2, os.SEEK_END)     
            while f.read(1) != b'\n':   
                if f.seek(-2, os.SEEK_CUR) == 0:
                    return None
            return float(f.readline().decode().split(',')[8])
    
    
    def _get_main_contracts(self):
        """Get the main contract for each date.
        Args:
            data_dir: data directory.
        Returns:
            List of lists, each sublist is in the format of [date, main contract].
        """
        vol_all = defaultdict(list)
        # for each date, collect all the contracts and their AccVolume
        # note: 1) empty file; 2) one-line file
        for filename in os.listdir(self.data_dir):
            file = os.path.join(self.data_dir, filename)
            if not filename.startswith('.') and os.stat(file).st_size != 0:
                accum_vol = self._get_acc_volume(file)
                if accum_vol != None:
                    contract, date = filename.split('.')[0].split('_')
                    vol_all[date].append((contract, accum_vol))
        # get the main contract for each date
        mc = [[d, max(vols, key=itemgetter(1))[0]] for d, vols in vol_all.items()]            
        self.main_contracts = sorted(mc, key=itemgetter(0))
    