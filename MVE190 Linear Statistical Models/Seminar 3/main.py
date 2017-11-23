# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:26:46 2017

@author: Rasmus
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
import statsmodels.api as sm
np.random.seed(1337)


def scatter_all(data, y_label = 'y'):
    col_names = list(data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        x_label = col_names[j]
        x = data[x_label]
        y = data[y_label]
        try:
            plt.scatter(x, y)
        except:
            print('Could not scatter {} against {}'.format(y_label, x_label))
        else:
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.savefig(os.path.join('scatterplots', x_label + '_vs_' + y_label + '.png'))
        plt.close()

def rms(y, yhat):
    error = y - yhat
    rms = np.sqrt(np.mean([e*e for e in error]))
    return rms

def RSS(y, yhat):
    error = y - yhat
    return sum([e*e for e in error])

def TSS(y):
    average_y = np.mean(y)
    return sum((y-average_y)**2)

def r_squared(y, yhat):
    tss = TSS(y)
    rss = RSS(y, yhat)
    return (tss-rss)/tss


def split_data(data, title=''):
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    train.to_csv(title + 'train.csv', index=False)    
    test.to_csv(title + 'test.csv', index=False)

def generate_x(nbr_samples):
    x1 = np.random.rand(nbr_samples)*10
    x2 = np.random.rand(nbr_samples)*5
    x3 = np.random.rand(nbr_samples)*100      
    x4 = np.random.rand(nbr_samples)*(3-0.1)+0.1
    return (x1, x2, x3, x4)
 
def generate_data(nbr_samples):
    (x1, x2, x3, x4) = generate_x(nbr_samples)
    y = 25 + x1 + 5*np.sqrt(x2) + 2.5*np.log(x3) + 1/x4
    e = np.random.normal(0, 3, nbr_samples)
    y = y+e
    df = pandas.DataFrame({'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4, 'y': y})
    return df

def MSE(est, x, y):
    yhat = est.predict(x)
    return rms(y, yhat)**2

def resid_plot(est, data):
     # not sure this is working correctly....
     x = data.drop('y', axis=1)
     y = data.y
     yhat = est.predict(x)
     e_tilde = (y-yhat)/np.sqrt(1-est.get_influence().hat_matrix_diag)
     plt.scatter(y, e_tilde)
     plt.xlabel('y')
     plt.ylabel('Standardized Residuals')

def resid_hist(est, data):    
     x = data.drop('y', axis=1)
     y = data.y
     yhat = est.predict(x)
     plt.hist(y-yhat)
     print(len(y))
     plt.xlabel('Residual')
     plt.ylabel('Frequency')


def transform_data_all_log(data):
    data.x1 = np.log(data.x1)
    data.rename(columns={'x1': 'log(x1)'}, inplace = True)
    data.x2 = np.log(data.x2)
    data.rename(columns={'x2': 'log(x2)'}, inplace = True)
    data.x3 = np.log(data.x3)    
    data.rename(columns={'x3': 'log(x3)'}, inplace = True)
    data.x4 = np.log(data.x4) # 1/data.x4
    data.rename(columns={'x4': 'log(x4)'}, inplace = True)  
    return data


def transform_data_all_sqrt(data):
    data.x1 = np.sqrt(data.x1)
    data.rename(columns={'x1': 'sqrt(x1)'}, inplace = True)
    data.x2 = np.sqrt(data.x2)
    data.rename(columns={'x2': 'sqrt(x2)'}, inplace = True)
    data.x3 = np.sqrt(data.x3)    
    data.rename(columns={'x3': 'sqrt(x3)'}, inplace = True)
    data.x4 = np.sqrt(data.x4)
    data.rename(columns={'x4': 'sqrt(x4)'}, inplace = True)  
    return data


def transform_data(data):
    data.x2 = np.sqrt(data.x2)
    data.rename(columns={'x2': 'sqrt(x2)'}, inplace = True)
    data.x3 = np.sqrt(data.x3)    
    data.rename(columns={'x3': 'sqrt(x3)'}, inplace = True)
    data.x4 = 1/data.x4
    data.rename(columns={'x4': 'x4^-1'}, inplace = True)
    return data

def train_model(data):
    x = data.drop('y', axis=1)
    y = data.y
    est = sm.OLS(y, x).fit()
    return(est)

def evaluate_model(data):
    print(data.head())
    x = data.drop('y', axis=1)
    y = data.y
    return MSE(est, x, y)
    
    
if __name__ == "__main__":
    data = generate_data(1000)
    data = sm.add_constant(data)
    scatter_all(data)
    data = transform_data(data)
    scatter_all(data)
    split_data(data)

    train_data = pandas.read_csv('train.csv')
    est = train_model(train_data)
    tMSE = evaluate_model(train_data)
    print(tMSE)
    plt.title('Residual plot, train data, tMSE=' + str(tMSE))
    #plt.show()

    test_data = pandas.read_csv('test.csv')
    pMSE = evaluate_model(test_data)
    resid_hist(est, test_data)
    plt.title('Histogram of test set residuals, pMSE=%.2f' % pMSE)
    plt.savefig('tmp.png', dpi=800)
    print(pMSE)
    