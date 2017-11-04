# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:13:18 2017

@author: Rasmus
"""
import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats



def scatter_price(housing_data):
    col_names = list(housing_data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        x_label = 'price'
        y_label = col_names[j]
        x = housing_data[x_label]
        y = housing_data[y_label]
        try:
            plt.scatter(x, y)
            
        except:
            print('Could not scatter {} against {}'.format(y_label, x_label))
        else:
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.savefig(os.path.join('housing_scatterplots', x_label + '_vs_' + y_label + '.png'))
        plt.close()

def analyze_basement(housing_data):
    x_label = 'sqft_basement'
    y_label = 'price'
    x = housing_data[x_label]
    y = housing_data[y_label]
    plt.scatter(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(os.path.join('figs', x_label + '_vs_' + y_label + '.png'))
    plt.close()
    
    #clean
    tmp = housing_data[housing_data.sqft_basement != 0]
    print(len(tmp))
    x = tmp[x_label]
    y = tmp[y_label]
    # transform
    x = np.log(x)
    y = np.log(y)
    #plt.scatter(x,y)
    sns.jointplot(x,y,kind='kde')
    plt.xlabel('Logarithm of ' + x_label)    
    plt.ylabel('Logarithm of ' + y_label)    
    plt.savefig(os.path.join('figs', 'log_'+ x_label + '_vs_log_' + y_label + '.png'), dpi=700)
    plt.close()



def make_regplot(x,y, x_label, y_label, save_folder):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax = sns.regplot(x,y)
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
        

def set_up(housing_data, x_label, y_label):
    save_folder = os.path.join('figs', x_label)
    try:
        os.mkdir(save_folder)
    except FileExistsError:
        pass
    return housing_data[x_label], housing_data[y_label], save_folder
    

def analyze_grade(housing_data):
    x_label = 'grade'
    y_label = 'price'
    (x, y, save_folder) = set_up(housing_data, x_label, y_label)

    # without tranformation
    make_plots(x, y, x_label, y_label, save_folder)

    # transform
    y = np.log(y)
    y_label = 'Log(' + y_label + ')'
    make_plots(x, y, x_label, y_label, save_folder)

                                                                                                                                                                                                                                                                                                                                                                                                                                            

def analyze_living(housing_data):
    x_label = 'sqft_living'
    y_label = 'price'
    (x, y, save_folder) = set_up(housing_data, x_label, y_label)

    # without tranformation
    make_plots(x, y, x_label, y_label, save_folder)

    # transform    
    x = np.log(x)
    y = np.log(y)
    x_label = 'Log(' + x_label + ')'
    y_label = 'Log(' + y_label + ')'
    make_plots(x, y, x_label, y_label, save_folder)
    
def analyze_bathrooms(housing_data):
    x_label = 'bathrooms'
    y_label = 'price'
    (x, y, save_folder) = set_up(housing_data, x_label, y_label)

    # without tranformation
    make_plots(x, y, x_label, y_label, save_folder)

    # transform
    y = np.log(y)
    y_label = 'Log(' + y_label + ')'
    make_plots(x, y, x_label, y_label, save_folder)


def main():
    housing_data = pandas.read_csv('kc_house_data.csv')
    # print column headers and number of observations
    print('Housing data loaded, {} observations, with the following categories:'.format(len(housing_data)))
    col_names = list(housing_data)
    print(col_names)
    analyze_bathrooms(housing_data)
    analyze_living(housing_data)
    analyze_grade(housing_data)

if __name__ == "__main__":
    main()
    