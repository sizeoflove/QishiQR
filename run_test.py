# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:46:25 2018

@author: rl17174
"""

import pprint
from cls_corpus_strat import CorpusStrategy
from cls_dp_spot import DataProcSpot
from cls_eqw_port import EqualWeightPort
from cls_backtest import Backtest
import matplotlib.pyplot as plt

import os

###############################################################################
#######################          Shanghai Test    #############################
###############################################################################
data_dir = "data/"

if(False):
    # Process data
    SHcomp = DataProcSpot(os.path.join(data_dir, '000001.SS.csv'))
    SHcomp.split_data((('1995', '2004'), ('2005', '2013')))
    
    # Create strategy
    strat = CorpusStrategy(SHcomp.train, 6)
    strat.get_signal(SHcomp.test)
    sig = strat.signal
    
    # Portfolio accepts signal and produce position
    port = EqualWeightPort(sig)
    port.get_position()
    position = port.position
    
    # Backtest
    my_bt = Backtest(SHcomp.test[position.index], position)
    stats = my_bt.output_summary_stats(rf=.02)
    
    pprint.pprint(stats)

###############################################################################
#######################          Futures test    ##############################
###############################################################################
if(True):
    import pandas as pd
    file_name = os.path.join(data_dir, 'ag1706_20161115.csv')
    ag1076 = pd.read_csv(file_name, delimiter=',', usecols=[2, 12, 22], \
                         dtype={'AskPrice1':float, 'BidPrice1':float})
    ag1076 = ag1076[(ag1076['AskPrice1']>0) & (ag1076['BidPrice1']>0)]
    
    prices = (ag1076['AskPrice1'] + ag1076['BidPrice1'])/2
    
#    plt.figure()
#    prices.plot()
#    
#    plt.figure()
#    prices[::5].plot()
#    
#    plt.figure()
#    prices[::10].plot()
    
    prices = prices[::20]
    prices = prices[prices.diff()!=0]
#    diff = prices.diff()=='0'
    
    
    prices.index = range(len(prices))
    
    
    cutoff = int(len(prices)/2)
    train = prices.iloc[:cutoff].copy()
    test  = prices.iloc[cutoff:].copy()
    
    # Create strategy
    print("Create Strats")
    print("Train data.")
    strat = CorpusStrategy(train, 6)
    print("Get signal")
    strat.get_signal(test)
    sig = strat.signal
    
    print("Position Sizing")
    # Portfolio accepts signal and produce position
    port = EqualWeightPort(sig)
    port.get_position()
    position = port.position
    
    # Backtest
    print("Backtest")
    my_bt = Backtest(test[position.index], position)
    stats = my_bt.output_summary_stats()
    
    pprint.pprint(stats)
