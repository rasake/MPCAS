# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:28:36 2017

@author: Rasmus
"""


import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os


def split_data():
    housing_data = pd.read_csv('kc_house_data.csv')
    housing_data = housing_data.dropna()
    msk = np.random.rand(len(housing_data)) < 0.5
    train = housing_data[msk]
    train = train[0:500]
    test = housing_data[~msk]
    test = test[0:5000]
    train.to_csv('kc_house_train.csv', index=False)    
    test.to_csv('kc_house_test.csv', index=False)


def standardize(train_data, test_data):
    st_train = train_data.copy()
    st_test = test_data.copy()
    for column in train_data:
        column_mean = np.mean(train_data[column])
        st_train[column] -= column_mean
        st_test[column] -= column_mean
        column_var = np.var(train_data[column])
        st_train[column] /= column_var
        st_test[column] /= column_var        
    return st_train, st_test

def transform(housing_data, inplace = False):
    if inplace:
        drop_columns_inplace(housing_data, ['id', 'date'])
        housing_data.price = np.log10(housing_data.price)
        housing_data.rename(columns={'price': 'log10(price)'}, inplace = True) 
        housing_data.sqft_living = np.log10(housing_data.sqft_living)
        housing_data.rename(columns={'sqft_living': 'log10(sqft_living)'}, inplace = True)
        housing_data.sqft_lot = np.log10(housing_data.sqft_lot)
        housing_data.rename(columns={'sqft_lot': 'log10(sqft_lot)'}, inplace = True)
        housing_data.sqft_above = np.log10(housing_data.sqft_above)
        housing_data.rename(columns={'sqft_above': 'log10(sqft_above)'}, inplace = True)
        housing_data.sqft_living15 = np.log10(housing_data.sqft_living15)
        housing_data = housing_data.drop('sqft_basement', axis=1)
        housing_data.rename(columns={'sqft_living15': 'log10(sqft_living15)'}, inplace = True)
        housing_data.sqft_lot15 = np.log10(housing_data.sqft_lot15)
        housing_data.rename(columns={'sqft_lot15': 'log10(sqft_lot15)'}, inplace = True)
    else:
        out_data = housing_data.copy()
        transform(out_data, inplace = True)
        return out_data

def hand_picked_transform(housing_data, inplace=False):
    if inplace:
        columns_to_drop = ['id', 'date', 'sqft_lot', 'sqft_above', 
        'sqft_basement', 'sqft_living15', 'sqft_lot15']
        drop_columns_inplace(housing_data, columns_to_drop)
        housing_data.price = np.log10(housing_data.price)
        housing_data.rename(columns={'price': 'log10(price)'}, inplace = True) 
        housing_data.sqft_living = np.log10(housing_data.sqft_living)
        housing_data.rename(columns={'sqft_living': 'log10(sqft_living)'}, inplace = True)
    else:
        out_data = housing_data.copy()
        hand_picked_transform(out_data, inplace = True)
        return out_data

def hand_picked_transform2(housing_data):
    df_out = pd.DataFrame()
    df_out['log10(price)'] = np.log10(housing_data.price)
    df_out['log10(sqft_living)'] = np.log10(housing_data.sqft_living)
    df_out['waterfront'] = housing_data.waterfront
    df_out['lat'] = housing_data.lat
    df_out['zipcode'] = housing_data.zipcode    
    return df_out


def drop_columns_inplace(df, column_names):
    for i_column in column_names:
        df.drop(i_column, axis=1, inplace=True)


def one_hot_encode(df, column_names):
    new_df = df
    for i_column in column_names:
        new_df[i_column] = i_column + ': ' + new_df[i_column].astype(str)
        new_df = pd.concat([new_df, new_df[i_column].str.get_dummies()], axis=1)
        new_df = new_df.drop(column_names, axis=1)
    return new_df

def trim_dataframes(df1, df2):
    column_names1 = list(df1)
    column_names2 = list(df2)
    new_df2 = df2.copy()
    for column in column_names2:
        if column not in column_names1:
            new_df2.drop(column, axis=1, inplace=True)
    for column in column_names1:
        if column not in column_names2:
            new_df2[column] = [0 for x in range(new_df2.shape[0])]
    return new_df2


        
def add_interaction_variables(data, inplace=False):
    if not inplace:
        out_data = data.copy()
        add_interaction_variables(out_data, inplace=True)
        return out_data
    columns = list(data)
    for i_column in columns:
        for j_column in columns:      
            if i_column == j_column:
                continue
            new_column_str = i_column + '*' + j_column
            if new_column_str in list(data):
                continue
            data[new_column_str] = data[i_column] * data[j_column]

def rmsPriceDomain(est, X, y):
    pred_error = 10**y - 10**est.predict(X)
    rms = np.sqrt(np.mean([x*x for x in pred_error]))
    return rms


def rmsLogDomain(est, X, y):
    pred_error = y - est.predict(X)
    rms = np.sqrt(np.mean([x*x for x in pred_error]))
    return rms

def evaluate(data, est, y_label='log10(price)'):
    X = data.drop(y_label, axis=1)
    X = sm.add_constant(X)
    y = data[y_label]
    return rmsLogDomain(est, X, y)

def train_OLS(data):
    X = data.drop('log10(price)', axis=1)
    X = sm.add_constant(X)
    y = data['log10(price)']
    return sm.OLS(y, X.astype(float)).fit()

def train_regularized(data, alpha):
    X = data.drop('log10(price)', axis=1)
    X = sm.add_constant(X)
    y = data['log10(price)']
    return sm.OLS(y, X.astype(float)).fit_regularized(alpha=alpha)

def plot_residuals(est, data, objective_name='log10(price)'):
    # fitted values (need a constant term for intercept)
    model_fitted_y = est.fittedvalues
    plot_lm_1 = plt.figure(1)
    plot_lm_1.set_figheight(8)
    plot_lm_1.set_figwidth(12)
    plot_lm_1.axes[0] = sns.residplot(model_fitted_y, objective_name, data=data, 
                              lowess=True, 
                              scatter_kws={'alpha': 0.5}, 
                              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
    plot_lm_1.axes[0].set_title('Residuals vs Fitted')
    plot_lm_1.axes[0].set_xlabel('Fitted values')
    plot_lm_1.axes[0].set_ylabel('Residuals')
 
def test_encoding():
    train_data = pd.read_csv('kc_house_train.csv')
    test_data = pd.read_csv('kc_house_test.csv')
    
    nbr_zip_codes = len(set(train_data.zipcode))
    print('Nbr of distinct zip codes in training data: ' + str(nbr_zip_codes))
    trans1_train = transform(train_data)
    trans1_test = transform(test_data)
    est = train_OLS(trans1_train)
    plot_residuals(est, trans1_train)
    plt.title('Residual plot using full data and no dummy variables')
    #plt.savefig('full_data_fit.png', dpi = 800)
    #plt.close()
    plt.show()
    pMSE = evaluate(trans1_test, est)**2
    print('Full data, no dummy variables: pMSE=' + str(pMSE))
    
    trans2_train = one_hot_encode(transform(train_data), ['zipcode'])
    trans2_test = one_hot_encode(transform(test_data), ['zipcode'])
    trans2_test = trim_dataframes(trans2_train, trans2_test)
    print(len(list(trans2_train)))
    print(len(list(trans2_test)))
    est = train_OLS(trans2_train)
    plot_residuals(est, trans2_train)
    plt.title('Residual plot using full data and one-hot-encoding for zipcodes')
    #plt.savefig('one_hot_encoding.png', dpi = 800)
    plt.show()
    pMSE = evaluate(trans2_test, est)**2
    print('Full data, one-hot-encoding for zipcodes: pMSE=' + str(pMSE))
    print(est.summary())


def test_interaction_vars():
    
    train_data = transform(pd.read_csv('kc_house_train.csv'))
    test_data = transform(pd.read_csv('kc_house_test.csv'))
    
    print(len(list(test_data)))
    est = train_OLS(train_data)
    tMSE = evaluate(train_data, est)**2
    pMSE = evaluate(test_data, est)**2    
    print('No interaction variables: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    train_zipcodes = train_data.zipcode    
    train_price = train_data['log10(price)']    
    train_data.drop('zipcode', axis = 1, inplace=True)
    train_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(train_data, inplace=True)
    train_data = pd.concat([train_data, train_zipcodes, train_price], axis=1)

    test_zipcodes = test_data.zipcode
    test_price = test_data['log10(price)']
    test_data.drop('zipcode', axis = 1, inplace=True)
    test_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(test_data, inplace=True)
    test_data = pd.concat([test_data, test_zipcodes, test_price], axis=1)
    

    
    print(len(list(test_data)))
    est = train_OLS(train_data)
    plot_residuals(est, train_data)
    plt.title('Residual plot with all interaction variables')
    plt.show()
    
    tMSE = evaluate(train_data, est)**2
    pMSE = evaluate(test_data, est)**2    
    print('Interaction variables: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    train_data = one_hot_encode(train_data, ['zipcode'])
    test_data = one_hot_encode(test_data, ['zipcode'])
    test_data = trim_dataframes(train_data, test_data)

    print(len(list(test_data)))
    est = train_OLS(train_data)
    plot_residuals(est, train_data)
    plt.title('Residual plot with all interaction variables, and all dummy variables')
    plt.show()
    
    tMSE = evaluate(train_data, est)**2
    pMSE = evaluate(test_data, est)**2    
    print('Interaction + dummy variables: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    


def test_ridge():
    train_data = transform(pd.read_csv('kc_house_train.csv'))
    test_data = transform(pd.read_csv('kc_house_test.csv'))
    
    train_zipcodes = train_data.zipcode    
    train_price = train_data['log10(price)']    
    train_data.drop('zipcode', axis = 1, inplace=True)
    train_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(train_data, inplace=True)
    train_data = pd.concat([train_data, train_zipcodes, train_price], axis=1)

    test_zipcodes = test_data.zipcode
    test_price = test_data['log10(price)']
    test_data.drop('zipcode', axis = 1, inplace=True)
    test_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(test_data, inplace=True)
    test_data = pd.concat([test_data, test_zipcodes, test_price], axis=1)
    
    train_data = one_hot_encode(train_data, ['zipcode'])
    test_data = one_hot_encode(test_data, ['zipcode'])
    test_data = trim_dataframes(train_data, test_data)
    
    st_train, st_test = standardize(train_data, test_data)
    
    
    print(len(list(st_train)))
    est = train_regularized(st_train, 0)
    print(est.summary())
    
    plot_residuals(est, st_train)
    plt.title('Residual plot for Ridge')
    plt.show()
    
    tMSE = evaluate(st_train, est)**2
    pMSE = evaluate(st_test, est)**2    
    print('Ridge: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    

def test_lasso():
    train_data = transform(pd.read_csv('kc_house_train.csv'))
    test_data = transform(pd.read_csv('kc_house_test.csv'))
    
    train_zipcodes = train_data.zipcode    
    train_price = train_data['log10(price)']    
    train_data.drop('zipcode', axis = 1, inplace=True)
    train_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(train_data, inplace=True)
    train_data = pd.concat([train_data, train_zipcodes, train_price], axis=1)

    test_zipcodes = test_data.zipcode
    test_price = test_data['log10(price)']
    test_data.drop('zipcode', axis = 1, inplace=True)
    test_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(test_data, inplace=True)
    test_data = pd.concat([test_data, test_zipcodes, test_price], axis=1)
    
    
    train_data = one_hot_encode(train_data, ['zipcode'])
    test_data = one_hot_encode(test_data, ['zipcode'])
    test_data = trim_dataframes(train_data, test_data)
    
    st_train, st_test = standardize(train_data, test_data)
    print(len(list(st_train)))
    est = train_regularized(st_train, 1)
    print(est.summary())
    
    plot_residuals(est, st_train)
    plt.title('Residual plot for Lasso')
    plt.show()
    
    tMSE = evaluate(st_train, est)**2
    pMSE = evaluate(st_test, est)**2    
    print('Lasso: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    print(type(est.params))
    for param_name in est.params.index:
        if est.params[param_name] != 0:
            print(param_name + str(est.params[param_name]))

def test_lasso_handpicked():
    train_data = hand_picked_transform(pd.read_csv('kc_house_train.csv'))
    test_data = hand_picked_transform(pd.read_csv('kc_house_test.csv'))
    
    train_zipcodes = train_data.zipcode    
    train_price = train_data['log10(price)']    
    train_data.drop('zipcode', axis = 1, inplace=True)
    train_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(train_data, inplace=True)
    train_data = pd.concat([train_data, train_zipcodes, train_price], axis=1)

    test_zipcodes = test_data.zipcode
    test_price = test_data['log10(price)']
    test_data.drop('zipcode', axis = 1, inplace=True)
    test_data.drop('log10(price)', axis = 1, inplace=True)
    add_interaction_variables(test_data, inplace=True)
    test_data = pd.concat([test_data, test_zipcodes, test_price], axis=1)
    
    
    train_data = one_hot_encode(train_data, ['zipcode'])
    test_data = one_hot_encode(test_data, ['zipcode'])
    test_data = trim_dataframes(train_data, test_data)
    
    st_train, st_test = standardize(train_data, test_data)
    print(len(list(st_train)))
    est = train_regularized(st_train, 1)
    print(est.summary())
    
    plot_residuals(est, st_train)
    plt.title('Residual plot for Lasso')
    plt.show()
    
    tMSE = evaluate(st_train, est)**2
    pMSE = evaluate(st_test, est)**2    
    print('Lasso: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    print(type(est.params))
    for param_name in est.params.index:
        if est.params[param_name] != 0:
            print(param_name + str(est.params[param_name]))

def test_top_pick_transform():
    train_data = hand_picked_transform2(pd.read_csv('kc_house_train.csv'))
    test_data = hand_picked_transform2(pd.read_csv('kc_house_test.csv'))
    
    train_data = one_hot_encode(train_data, ['zipcode'])
    test_data = one_hot_encode(test_data, ['zipcode'])
    test_data = trim_dataframes(train_data, test_data)
    
    print(len(list(train_data)))
    est = train_OLS(train_data)
    print(est.summary())
    
    plot_residuals(est, train_data)
    plt.title('Residual plot for OLS with feature selected by Lasso')
    plt.show()
    
    tMSE = evaluate(train_data, est)**2
    pMSE = evaluate(test_data, est)**2    
    print('OLS with Lasso best pick: tMSE={:.3e}, pMSE={:.3e}'.format(tMSE, pMSE))
    
    print(type(est.params))
    for param_name in est.params.index:
        if est.params[param_name] != 0:
            print(param_name + str(est.params[param_name]))


def scatter_mort(data):
    col_names = list(data)
    nbr_cols = len(col_names)
    for j in range(nbr_cols):
        x_label = 'mort'
        y_label = col_names[j]
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




def full_search():
    data = pd.read_csv('pollution.txt') 
    data.so = np.sqrt(data.so)
    data.rename(columns={'so': 'sqrt(so)'}, inplace = True) 
    data.educ = 1 / data.educ
    data.rename(columns={'educ': 'inv(educ)'}, inplace = True) 
    
    X = data.drop('mort', axis=1)
    y = data.mort
    
    best_est = None
    best_score = 0
    nbr_vars = len(list(X))
    specifier = '0'+str(nbr_vars)+'b'
    limit = 2**nbr_vars
    configs = [str(format(i, specifier)) for i in range(limit)]
    print('entering the loop')
    nbr_hits = 0
    for i_config in configs:
        print(int(i_config, 2)/limit)
        if int(i_config) == 0:
            continue
        tmp_X = X.copy()
        for j, column_name in enumerate(tmp_X):
            if not int(i_config[j]):
                tmp_X.drop(column_name, axis=1, inplace=True)
        tmp_X = sm.add_constant(tmp_X)
        est = sm.OLS(y, tmp_X.astype(float)).fit()
        score = 1/est.bic
        if score > best_score:
            print('===================================')
            print("found new best estimator")
            print('BIC=' + str(score/1))
            print('===============================')
            nbr_hits += 1
            best_est = est
            best_score = score
    print(best_est.summary())
    best_est.save('best_pollution_est_BIC.pickle')
    print(nbr_hits)
    

def evaluate_best_polution():
    data = pd.read_csv('pollution.txt') 
    data.so = np.sqrt(data.so)
    data.rename(columns={'so': 'sqrt(so)'}, inplace = True) 
    data.educ = 1 / data.educ
    data.rename(columns={'educ': 'inv(educ)'}, inplace = True)
    mort = data.mort

    est = sm.regression.linear_model.RegressionResults.load('best_pollution_est_AIC.pickle')
    data = sm.add_constant(data)
    X = pd.DataFrame() 
    for param_name in est.params.index:
        X[param_name] = data[param_name]
    
    data = pd.concat([X, mort], axis=1)
    plot_residuals(est, data, 'mort')
    plt.title('Residual plot for Lasso')
    plt.show()
    print(est.summary())



def lasso_pollution():
    data = pd.read_csv('pollution.txt') 
    data.so = np.sqrt(data.so)
    data.rename(columns={'so': 'sqrt(so)'}, inplace = True) 
    data.educ = 1 / data.educ
    data.rename(columns={'educ': 'inv(educ)'}, inplace = True) 

    mort = data.mort
    X = data.drop('mort', axis = 1)
    #add_interaction_variables(X, inplace=True)
    X, _ = standardize(X, X)
    st_data = pd.concat([X, mort], axis=1)
    X = sm.add_constant(X)
    est = sm.OLS(mort, X.astype(float)).fit_regularized(1)
    print(est.summary())
    
    plot_residuals(est, st_data, 'mort')
    plt.title('Residual plot for Lasso')
    plt.show()
    
    tMSE = evaluate(st_data, est, 'mort')**2 
    print('Lasso: tMSE={:.3e}'.format(tMSE))
    
    print(type(est.params))
    for param_name in est.params.index:
        if est.params[param_name] != 0:
            print(param_name + str(est.params[param_name]))

    plt.hist(mort)
    print(np.std(mort))


#full_search()
#evaluate_best_polution()
#lasso_pollution()

#test_top_pick_transform()
#test_lasso_handpicked()  
#test_interaction_vars()
 
#test_ridge()

test_encoding()