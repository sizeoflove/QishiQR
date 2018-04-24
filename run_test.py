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

###############################################################################
#######################          Shanghai Test    #############################
###############################################################################

if(True):
    # Process data
    SHcomp = DataProcSpot(r'000001.SS.csv')
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
    ag1076 = pd.read_csv('chain_data.csv', delimiter=',', usecols=[3, 13, 23])
    prices = (ag1076['AskPrice1'] + ag1076['BidPrice1'])/2
    cutoff = int(len(ag1076)/2)
    train = prices.iloc[:cutoff]
    test  = prices.iloc[cutoff:]
    
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
