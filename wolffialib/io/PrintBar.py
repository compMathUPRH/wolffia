#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:31:42 2020

@author: jse
"""

import progressbar
#import progressbar.utils as utils
class PrintBar(progressbar.ProgressBar):
    ''' Wrapper for ProgressBar to respond to PyQt progress bar methods.
        To install progressbar module use pip3 install progressbar2
    '''
    def __init__(self, min_value=0, max_value=None, widgets=None,
                 left_justify=True, initial_value=0, poll_interval=None,
                 widget_kwargs=None, #custom_len=utils.len_color,
                 max_error=True, prefix=None, suffix=None, variables=None,
                 min_poll_interval=None, **kwargs):
        super(PrintBar, self).__init__(min_value, max_value, widgets,
                 left_justify, initial_value, poll_interval,
                 widget_kwargs, custom_len,
                 max_error, prefix, suffix, variables,
                 min_poll_interval, **kwargs)
    
    def setLabelText(self, label):
        self.prefix = label
        
    def setRange(self, rmin, rmax):
        self.min_value = rmin
        self.max_value = rmax
        
    def setValue(self, val):
        self.update(val)
        
    def close(self):
        self.finish()
        
