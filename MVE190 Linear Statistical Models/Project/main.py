# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:47:18 2017

@author: Rasmus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import calendar
import statsmodels.api as sm
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import graphviz

def split_data(data):
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    return (train, test)


def R2(y, y_pred):
    pred_error = y - y_pred
    RSS = sum(pred_error**2)
    SST = sum((y-np.mean(y))**2)
    return (SST-RSS)/SST


def scatter_area(data):
    col_names = list(data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        x_label = col_names[j]
        y_label = 'area'
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


def hist_all(data, folder = 'histograms', create_folder = False):
    if create_folder:    
        os.makedirs(folder, exist_ok=True)
    col_names = list(data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        j_label = col_names[j]
        try:
            plt.hist(data[j_label])
        except:
            print('Could not histogram {} '.format(j_label))
        else:
            plt.xlabel(j_label)
            plt.ylabel('Frequency')
            plt.savefig(os.path.join(folder, j_label + '.png'))
        plt.close()

def hist_division(data, cut_off=0):
    mask = (data.area <= cut_off)
    low_data = data[mask]
    high_data = data [~mask]
    #hist_all(low_data, 'low_hists', create_folder=True)
    #hist_all(high_data, 'high_hists', create_folder=True)
    col_names = list(data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        j_label = col_names[j]
        try:
            sns.distplot(low_data[j_label], hist=(j_label!='area' and j_label!='rain'))
        except:
            print('Could not histogram {} for low range'.format(j_label))
        try:
            sns.distplot(high_data[j_label], hist=(j_label!='area' and j_label!='rain'))
        except:
            print('Could not histogram {} '.format(j_label))
        else:
            plt.xlabel(j_label)
            plt.ylabel('Frequency')
            tmp = ['Data points with area less than or equal to ' + str(cut_off),
                   'Data points with area larger than ' + str(cut_off)]
            plt.legend(tmp)
            plt.savefig(os.path.join('hist_div', j_label + '.png'))
        plt.close()

def hist_division_rain_area(data, cut_off=0):
    mask = (data.area <= cut_off)
    low_data = data[mask]
    high_data = data [~mask]
    
    plt.hist(low_data['rain'], alpha = 0.5)
    plt.hist(high_data['rain'], alpha = 0.5)
    plt.xlabel('rain')
    plt.ylabel('Frequency')
    tmp = ['Data points with area less than or equal to ' + str(cut_off),
           'Data points with area larger than ' + str(cut_off)]
    plt.legend(tmp)
    plt.savefig(os.path.join('hist_div', 'rain.png'))
    plt.close()
    
    plt.hist(low_data['area'], alpha = 0.5)
    plt.hist(high_data['area'], alpha = 0.5)
    plt.xlabel('area')
    plt.ylabel('Frequency')
    tmp = ['Data points with area less than or equal to ' + str(cut_off),
           'Data points with area larger than ' + str(cut_off)]
    plt.legend(tmp)
    plt.savefig(os.path.join('hist_div', 'area.png'))
    plt.close()

data = pd.read_csv('forestfires.csv')
data.area = np.log10(data.area+1)
m_abbrevations = [x.lower() for x in calendar.month_abbr]
data.month = [m_abbrevations.index(x) for x in data.month]        
d_abbrevations = [x.lower() for x in calendar.day_abbr]
data.day = [d_abbrevations.index(x) for x in data.day]

#hist_division(data, cut_off=0.1)
#hist_division_rain_area(data, cut_off=0.1)

train, test = split_data(data )
X = train.drop('area', axis=1)
X = sm.add_constant(X)
y = train['area']
X_test = test.drop('area', axis=1)
X_test = sm.add_constant(X_test)
y_test = test['area']



est = sm.OLS(y, X.astype(float)).fit()
print(est.summary())

print('=======================\n\n')

print('Linear Regression')
y_pred = est.predict(X)
print(R2(y, y_pred))
y_pred_test = est.predict(X_test)
print(R2(y_test, y_pred_test))

print('Decision tree (not pruned)')
clf = tree.DecisionTreeRegressor(min_samples_split = 2)
clf = clf.fit(X,y)
y_pred = clf.predict(X)
print(R2(y, y_pred))
y_pred_test = clf.predict(X_test)
print(R2(y_test, y_pred_test))

dotfile = open("my_reg_tree.dot", 'w')
tree.export_graphviz(clf, out_file = dotfile, feature_names = X.columns)
dotfile.close()

print('Random Tree')
clf = RandomForestRegressor(max_features = None)
clf = clf.fit(X,y)
y_pred_train = clf.predict(X)
print(R2(y, y_pred_train))
y_pred_test = clf.predict(X_test)
print(R2(y_test, y_pred_test))

