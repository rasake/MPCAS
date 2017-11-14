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
import statsmodels.api as sm


from mpl_toolkits.mplot3d import Axes3D


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



def tmp(housing_data):
    X = housing_data[['grade', 'sqft_living']]
    y = housing_data['price']

    ## fit a OLS model with intercept on TV and Radio
    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()
    
    print(est.summary())
    
    ## Create the 3d plot -- skip reading this
    # TV/Radio grid for 3d plot
    xx1, xx2 = np.meshgrid(np.linspace(X.grade.min(), X.grade.max(), 100), 
                           np.linspace(X.sqft_living.min(), X.sqft_living.max(), 100))
    # plot the hyperplane by evaluating the parameters on the grid
    Z = est.params[0] + est.params[1] * xx1 + est.params[2] * xx2
    
    # create matplotlib 3d axes
    fig = plt.figure(figsize=(12, 8))
    ax = Axes3D(fig, azim=-115, elev=15)
    ax.scatter(X.grade, X.sqft_living, y)
    
    print(X.sqft_living.max())
    # plot hyperplane
    surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

    # set axis labels
    ax.set_xlabel('sqft_living')
    ax.set_ylabel('grade')
    ax.set_zlabel('price')
    plt.show()

def main():
    housing_data = pandas.read_csv('kc_house_data.csv')
    housing_data = housing_data[['price', 'bedrooms',
    'bathrooms', 'sqft_living', 'floors', 'waterfront', 
    'view', 'condition', 'grade', 'sqft_above',
    'yr_built', 'yr_renovated']]
    housing_data.price = np.log10(housing_data.price)
    
    msk = np.random.rand(len(housing_data)) < 0.5
    train = housing_data[msk]
    train = train[0:250]
    test = housing_data[~msk]
    test = test[0:250]
    
    # print column headers and number of observations
    print('Housing data loaded, {} observations, with the following categories:'.format(len(housing_data)))
    col_names = list(housing_data)
    print(col_names)
    tmp(train)
    
    
if __name__ == "__main__":
    main()
    