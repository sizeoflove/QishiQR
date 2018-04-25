# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:31:45 2018

@author: rl17174
"""
import numpy as np
import pandas as pd

class Backtest(object):
    
    def __init__(self, prices, positions):
        self.prices       = prices 
        self.positions    = positions
        self.pnl          = None
        self.equity_curve = None
        
    def output_summary_stats(self, rf=.0, periods=252):
        """
        Creates a list of summary statistics for the portfolio such
        as Sharpe Ratio and drawdown information.
        """
        self.pnl = self._calc_pnl(self.prices, self.positions)
        self.equity_curve = self._build_equity_curve(self.pnl)
        self.equity_curve.plot()
        
        total_return = self.equity_curve.iloc[-1]
        sharpe_ratio = self._calc_sharpe_ratio(self.pnl, rf, periods)
        max_dd = -self._calc_max_drawdown(self.equity_curve)
        dd_duration = self._calc_max_drawdown_duration(self.equity_curve)
        winning_rate = self._winning_rate(self.prices, self.positions)

        stats = [("Total Return", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
                 ("Sharpe Ratio", "%0.4f" % sharpe_ratio),
                 ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
                 ("Drawdown Duration", "%d" % dd_duration), 
                 ("Winning Rate", "%0.2f%%" % (winning_rate * 100.0))]
        return stats    

    def _build_equity_curve(self, pnl):
        """Build equity curve.
        """
        return (pnl+1).cumprod()
    
    def _calc_pnl(self, prices, positions):
        """
        Calculates strategy pnl based on prices series and positions. 
        """
        pnl = prices.pct_change().multiply(positions.shift(1))
        pnl.iloc[0] = 0
        return pnl
    
    def _winning_rate(self, prices, positions):
        ud = prices.diff()
        ud[ud>0] = 1
        ud[ud<0] = -1
        return len(ud[ud==positions.shift(1)])/(len(ud)-1)
    
#    def _calc_max_drawdown_duration(self, equity_curve):
#        duration = pd.Series(index=equity_curve.index, name = 'Duration')
#        roll_max = np.maximum.accumulate(equity_curve)
#        for i, (dd, rm) in enumerate(zip(equity_curve, roll_max)):
#                duration.iloc[i] = 0 if dd == rm else duration.iloc[i-1] + 1
#        return duration.max()
    
    def _calc_max_drawdown_duration(self, equity_curve):
        roll_max = np.maximum.accumulate(equity_curve)
        duration = equity_curve-roll_max
        duration.index = range(len(duration))
        idx = np.where(duration==.0)
        return np.diff(idx).max()-1
              
    def _calc_max_drawdown(self, pnl):
        """
        Calculates the max drawdown of a price series. If you want the
        actual drawdown series, please use to_drawdown_series.
        """
        return (pnl / pnl.expanding(min_periods=1).max()).min() - 1
    
#    def _to_drawdown_series(self, pnl):
#        """
#        Calculates the drawdown series.
#    
#        This returns a series representing a drawdown.
#        When the price is at all time highs, the drawdown
#        is 0. However, when prices are below high water marks,
#        the drawdown series = current / hwm - 1
#    
#        The max drawdown can be obtained by simply calling .min()
#        on the result (since the drawdown series is negative)
#    
#        Method ignores all gaps of NaN's in the price series.
#    
#        Args:
#            * prices (Series or DataFrame): Series of prices.
#    
#        """
#        # make a copy so that we don't modify original data
#        drawdown = pnl.copy()
#    
#        # Fill NaN's with previous values
#        drawdown = drawdown.fillna(method='ffill')
#    
#        # Ignore problems with NaN's in the beginning
#        drawdown[np.isnan(drawdown)] = -np.Inf
#    
#        # Rolling maximum
#        roll_max = np.maximum.accumulate(drawdown)
#        drawdown = drawdown / roll_max - 1.
#        return drawdown
          
    def _calc_sharpe_ratio(self, returns, rf=.0, periods=252):
        """
        Create the Sharpe ratio for the returns. 
        """
        excess_rets = returns - rf/periods
        return np.sqrt(periods)*np.mean(excess_rets)/np.std(excess_rets)
    
#    def _to_excess_returns(self, returns, rf, nperiods=None):
#        """
#        Given a series of returns, it will return the excess returns over rf.
#    
#        Args:
#            * returns (Series, DataFrame): Returns
#            * rf (float, Series): Risk-Free rate(s) expressed in annualized term or return series
#            * nperiods (int): Optional. If provided, will convert rf to different
#                frequency using deannualize only if rf is a float
#        Returns:
#            * excess_returns (Series, DataFrame): Returns - rf
#    
#        """
#        if type(rf) is float and nperiods is not None:
#            _rf = self._deannualize(rf, nperiods)
#        else:
#            _rf = rf
#        return returns - _rf
#    
#    def _deannualize(self, returns, nperiods):
#        """
#        Convert return expressed in annual terms on a different basis.
#    
#        Args:
#            * returns (float, Series, DataFrame): Return(s)
#            * nperiods (int): Target basis, typically 252 for daily, 12 for
#                monthly, etc.
#    
#        """
#        return np.power(1 + returns, 1. / nperiods) - 1.