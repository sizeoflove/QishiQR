# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:46:30 2018

@author: rl17174
"""
from cls_strategy import Strategy
import numpy as np
import pandas as pd
from collections import Counter
from operator import itemgetter
from itertools import tee


class CorpusStrategy(Strategy):
    def __init__(self, init_ts, n):
        """
        Initialize strategy instance. init_ts here is for the intial setup 
        of corpus, which essentially means -- training data. 
        """
        self.init_ts = init_ts
        self.n       = n
        # This corpus may be updated later as data flow in
        self.corpus_dict  = self._get_init_corpus()
    
    def _get_init_corpus(self):
        return self._get_corpus(self._get_symbol(self.init_ts))
    
    def _get_corpus(self, ts_sym):
        """Establish the corpus dictionary.
        Args:
            ts_sym: A string represent symbol and ndarray of symbols
        Returns:
            Dictionary, contains {symbol: counts}.
        """
        corpus_dict = Counter(ts_sym[i:i+self.n] for i in \
                              range(len(ts_sym)-self.n+1))
        return corpus_dict
    
    def _get_symbol(self, ts):
        """Encode information such as up and down into symbols.
        Args:
            ts: pd series, represents mid or last price time series.
        Returns:
            A string represent symbol and ndarray of symbols (optional).
        """
        ret = pd.Series(ts).pct_change().dropna()
        # note: tuning parameter 'm' is hard-coded as '0', '1', '2'
        symbol_arr = np.where(ret==0, '0', np.where(ret<0, '1', '2'))
        ts_sym = ''.join(symbol_arr.tolist())
        return ts_sym  

    def get_signal(self, ts):
        """vectorized calculation for signal"""
        self.signal = pd.Series(index=ts.index, name='Signal')
        ts_sym = self._get_symbol(ts)
        ts_substr = [''.join(s) for s in list(self.window(ts_sym, self.n-1))]
        substr_uniq = set(ts_substr)
        Pr_up = [self.corpus_dict[s+'2'] for s in substr_uniq]
        Pr_down = [self.corpus_dict[s+'1'] for s in substr_uniq]
        prediction = ['2' if u>d else '1' for u, d in zip(Pr_up, Pr_down)]
        prediction_dct = dict(zip(substr_uniq, prediction))
        self.signal.iloc[self.n-1:] = [prediction_dct[s] for s in ts_substr]
#    def get_signal(self, ts):
#        """vectorized calculation for signal"""
#        self.signal = pd.Series(index=ts.index, name='Signal')
#        ts_sym = self._get_symbol(ts)
#        for i, pat in enumerate(self._sliding_window(ts_sym)):
#            self.signal.iloc[i+self.n-1] = self._get_sig_for_pat(pat)
        
#    def _sliding_window(self, syms):
#        """ window length is defaulted to self.n-1"""
#        for i in range(self.n-1, len(syms)+1): yield syms[i-self.n+1:i]
        
    @staticmethod
    def window(iterable, n):
        els = tee(iterable, n)
        for i, el in enumerate(els):
            for _ in range(i):
                next(el, None)
        return zip(*els)
    
#    def _get_sig_for_pat(self, pattern):
#        """Obtain signal based on lastest nth observations and established corpus.
#        Returns:
#            A string represents signal.
#        """        
#        # note: tuning parameter 'm' is hard-coded as '0', '1', '2'
#        symbol_freq = {symbol:self.corpus_dict.get(pattern+symbol, 0)
#                       for symbol in '012'}
#        signal, freq = max(symbol_freq.items(), key=itemgetter(1))
#        return signal
#    
#    def _update_corpus(self, pattern):
#        raise NotImplementedError("Should implement update_corpus()")