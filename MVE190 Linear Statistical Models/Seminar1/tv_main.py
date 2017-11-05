# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:32:36 2017

@author: Rasmus
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
import regutil


def drop_nans(x,y):
    x = x[np.logical_not(np.isnan(x))]
    y = y[np.logical_not(np.isnan(x))]
    x = x[np.logical_not(np.isnan(y))]
    y = y[np.logical_not(np.isnan(y))]
    return (x,y)

def main():
    tv_data = pandas.read_csv('TV.dat', sep='\t')
    # print column headers and number of observations
    print('TV data loaded, {} observations, with the following categories:'.format(len(tv_data)))
    col_names = list(tv_data)
    print(col_names)
    

    save_folder = os.path.join('figs', 'Dr_vs_TV')
    try:
        os.mkdir(save_folder)
    except FileExistsError:
        pass
    x =  tv_data['ppDr']
    y = tv_data['ppTV']
    x, y = drop_nans(x,y)
    x_label = 'People per Doctor'
    y_label = 'People per TV'
    # without tranformation
    regutil.make_plots(x, y, x_label, y_label, save_folder)

    # log10 transform
    x_trans = np.log10(x)
    x_trans_label = 'Log10 of ' + x_label
    y_trans = np.log10(y)
    y_trans_label = 'Log10 of' + y_label
    regutil.make_plots(x_trans, y_trans, x_trans_label, y_trans_label, save_folder)
    
    # inverse transform
    x_trans = 1/x
    x_trans_label = 'Doctors per capita'
    y_trans = 1/y
    y_trans_label = 'TVs per capita'
    regutil.make_plots(x_trans, y_trans, x_trans_label, y_trans_label, save_folder)
    
    # inverse transform
    x_trans = np.sqrt(1/x)
    x_trans_label = 'Square Root of Doctors per capita'
    y_trans = np.sqrt(1/y)
    y_trans_label = 'Square Root of TVs per capita'
    regutil.make_plots(x_trans, y_trans, x_trans_label, y_trans_label, save_folder)
if __name__ == "__main__":
    main()