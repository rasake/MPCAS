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



def split_data():
    housing_data = pandas.read_csv('kc_house_data.csv')
    housing_data = housing_data.dropna()
    msk = np.random.rand(len(housing_data)) < 0.5
    train = housing_data[msk]
    train = train[0:250]
    test = housing_data[~msk]
    test = test[0:250]
    train.to_csv('kc_house_train.csv', index=False)    
    test.to_csv('kc_house_test.csv', index=False)
    

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



def basic_OLS(housing_data):
    X = housing_data[['grade', 'sqft_living']]
    y = housing_data['price']

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
    
    # plot hyperplane
    surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

    # set axis labels
    ax.set_xlabel('sqft_living')
    ax.set_ylabel('grade')
    ax.set_zlabel('price')
    plt.show()



def backwards_selection(data, target_name, save_folder):
    n = len(data)
    X = data.drop(target_name, axis=1)
    X = sm.add_constant(X)
    y = data[target_name]
    
    est_best = None
    
    
    for i in range(len(list(X))-1):
        
        save_path = os.path.join(save_folder,  'fit_' + str(len(list(X))-1) + '_variables.pickle')    
        RSS_simple = np.Inf;
        i_worst_predictor = None
        
        # Do the full fit
        est = sm.OLS(y, X.astype(float)).fit()
        est.save(save_path)
        RSS_complex = sum([x*x for x in est.resid])
        degrees_of_freedom = n-len(list(X))
        
        # Find out which one is worse
        for j_predictor in list(X):
            if j_predictor == 'const':
                continue
            
            jX = X.drop(j_predictor, axis=1)
            j_est = sm.OLS(y, jX.astype(float)).fit()
            j_RSS = sum([x*x for x in j_est.resid])

            
            if j_RSS < RSS_simple:
                RSS_simple = j_RSS
                i_worst_predictor = j_predictor

        F_obs = (RSS_simple-RSS_complex)/RSS_complex*(degrees_of_freedom)
        alpha = 0.05
        F_theo =  stats.f.ppf(1-alpha, 1, degrees_of_freedom)
        
        if F_obs <= F_theo:
            best_est = est
            
        print('Dropping ' + i_worst_predictor)
        X = X.drop(i_worst_predictor, axis=1)

    print('\n')
    print('Best predictors:')
    print(best_est.pvalues.index.drop('const').tolist())
    return best_est
        
        
    
def train_backwards():
    housing_data = pandas.read_csv('kc_house_train.csv')
    
    housing_data = housing_data.drop('date', axis=1)
    housing_data = housing_data.drop('id', axis=1)    
    # Transformations
    housing_data.price = np.log10(housing_data.price)
    housing_data.sqft_living = np.log10(housing_data.sqft_living)
    housing_data.sqft_lot = np.log10(housing_data.sqft_lot)
    housing_data.sqft_above = np.log10(housing_data.sqft_above)
    housing_data.sqft_living15 = np.log10(housing_data.sqft_living15)
    housing_data.sqft_lot15 = np.log10(housing_data.sqft_lot15)


    
    # print column headers and number of observations
    print('Housing data loaded, {} observations, with the following categories:'.format(len(housing_data)))
    col_names = list(housing_data)
    print(col_names)
    
    
    est = backwards_selection(housing_data, 'price', 'fits')
    print(est.summary())

def fit_expert_guess():
    housing_data = pandas.read_csv('kc_house_train.csv')

    # Transformations
    housing_data.price = np.log10(housing_data.price)
    housing_data.sqft_living = np.log10(housing_data.sqft_living)

    X = housing_data[['bathrooms', 'sqft_living', 'grade', 'view']]
    X = sm.add_constant(X)
    y = housing_data['price']
    
    est = sm.OLS(y, X.astype(float)).fit()
    est.save('expert_guess.pickle')
    print(est.summary())
    

def rms(est, X, y):
    pred_error = 10**y - 10**est.predict(X)
    rms = np.sqrt(np.mean([x*x for x in pred_error]))
    return rms
    
def evaluate_expert_guess():
    
    test_data = pandas.read_csv('kc_house_test.csv')
    # Transformations
    test_data.price = np.log10(test_data.price)
    test_data.sqft_living = np.log10(test_data.sqft_living)

    X = test_data[['bathrooms', 'sqft_living', 'grade', 'view']]
    X = sm.add_constant(X)
    y = test_data['price']
    est = sm.regression.linear_model.RegressionResults.load('expert_guess.pickle')
    print(np.mean(10**y))
    return rms(est, X, y)
    
def evaluate_backwards():
    
    data = pandas.read_csv('kc_house_test.csv')
    data = data.drop('date', axis=1)
    data = data.drop('id', axis=1)    
    # Transformations
    data.price = np.log10(data.price)
    data.sqft_living = np.log10(data.sqft_living)
    data.sqft_lot = np.log10(data.sqft_lot)
    data.sqft_above = np.log10(data.sqft_above)
    data.sqft_living15 = np.log10(data.sqft_living15)
    data.sqft_lot15 = np.log10(data.sqft_lot15)
    
    
    results = pandas.DataFrame(columns=['nbr_predictors', 'rms', 'predictors'])
    for filename in os.listdir('fits'):
        file_path = os.path.join('fits', filename)
        est = sm.regression.linear_model.RegressionResults.load(file_path)
        predictors = est.pvalues.index.drop('const').tolist()    
        X = data[predictors]
        X = sm.add_constant(X)
        y = data['price']
        results = results.append({'rms': rms(est, X, y), 'predictors': predictors,
                        'nbr_predictors': len(predictors)}, ignore_index = True)

    results.sort_values('nbr_predictors', axis=0, inplace = True)
    results = results.reset_index(drop=True)
    print(results)
    plt.plot(results.nbr_predictors, results.rms)
    plt.show()
    return -1#


def main():
    train_backwards()
    print(evaluate_backwards())
    print(evaluate_expert_guess())
    
if __name__ == "__main__":
    main()
    