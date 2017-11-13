# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 10:13:25 2017

@author: Rasmus
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

def make_regplot(x,y, x_label, y_label, save_folder):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax = sns.regplot(x,y, ci=False)
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    textstr = '$\mathrm{intercept} = %.3f$\n$\mathrm{slope}=%.2f$\n$\mathrm{r2}=%.2f$'%(intercept, slope, r_value**2)
    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(os.path.join(save_folder, x_label + '_vs_'
        + y_label + '.png'), dpi=700)
    plt.close()
    return (slope, intercept)


def make_error_plots(x, y, e, x_label, y_label, save_folder):
    plt.scatter(x,e)
    plt.xlabel(x_label)
    plt.ylabel('Residual')
    plt.savefig(os.path.join(save_folder, 'Xerrorplot_' + x_label + '_vs_'
        + y_label + '.png'), dpi = 700)
    plt.close()    

    plt.scatter(y,e)
    plt.xlabel(y_label)
    plt.ylabel('Residual')
    plt.savefig(os.path.join(save_folder, 'Yerrorplot_' + x_label + '_vs_'
        + y_label + '.png'), dpi = 700)
    plt.close()

def make_plots(x, y, x_label, y_label, save_folder):
    slope, intercept = make_regplot(x, y, x_label, y_label, save_folder)    
    yhat = [slope*xi + intercept for xi in x]
    e = yhat-y  
    make_error_plots(x, y, e, x_label, y_label, save_folder)
 