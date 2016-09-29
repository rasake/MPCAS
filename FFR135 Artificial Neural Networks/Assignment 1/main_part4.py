# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:37:48 2016

@author: Rasmus
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool
#import seaborn as sns

from feed_forward_network import MultilayerNetwork



def load_and_normalize(train_path, validation_path):
    df_tr = pd.read_csv(train_path, header = None, delim_whitespace=True, names = ['xi_1', 'xi_2', 'zeta'])
    df_val = pd.read_csv(validation_path, header = None, delim_whitespace=True, names = ['xi_1', 'xi_2', 'zeta'])

    big_df = pd.concat([df_tr, df_val])
    xi_1_mean = big_df.xi_1.mean()
    xi_1_std = big_df.xi_1.std()
    xi_2_mean = big_df.xi_2.mean()
    xi_2_std = big_df.xi_2.std()

    df_tr.xi_1 = (df_tr.xi_1 - xi_1_mean)/xi_1_std
    df_tr.xi_2 = (df_tr.xi_2 - xi_2_mean)/xi_2_std

    df_val.xi_1 = (df_val.xi_1 - xi_1_mean)/xi_1_std
    df_val.xi_2 = (df_val.xi_2 - xi_2_mean)/xi_2_std

    big_df = pd.concat([df_tr, df_val])  

    return df_tr, df_val

def draw_observation(df):
    r_index = np.random.randint(0, len(df)) #low inclusive, high exclusive
    r_series = df.iloc[r_index]
    r_xi1 = r_series.xi_1
    r_xi2 = r_series.xi_2
    r_xi = np.reshape([r_xi1,r_xi2], [2,1])
    r_zeta = np.reshape(r_series.zeta, [1,1])
    
    return r_xi, r_zeta



def classification_error(network, df):
    C = 0
    p = len(df)
    for row in df.iterrows():
        row = row[1]
        xi = np.reshape([row.xi_1,row.xi_2], [2,1])
        zeta = row.zeta
        o = network.feed_forward(xi)[0][0]
        error_i = 1/(2*p) * np.abs(zeta - np.sign(o))
        C += error_i
    return C

        
def train_network(network, learning_rate, df_tr, df_val, nbr_iterations, nbr_errors):
    tr_error = np.zeros(int(nbr_errors))
    val_error = np.zeros(int(nbr_errors))
    for i in range(int(nbr_iterations)):
        xi, zeta = draw_observation(df_tr)
        network.feed_forward(xi)
        network.propogate_back(zeta, learning_rate)
        condition_1 = i % (nbr_iterations//nbr_errors) == 0
        if condition_1 and i//(nbr_iterations//nbr_errors) < nbr_errors:
            tr_error[int(i//(nbr_iterations//nbr_errors))] = classification_error(network, df_tr)
            val_error[int(i//(nbr_iterations//nbr_errors))] = classification_error(network,df_val)

    return tr_error, val_error


def single_trial_a(input_lst):
    [save_folder, df_tr, df_val, trial_id] = input_lst

    nbr_iterations = 2e5
    nbr_errors = 1000
    learning_rate = 0.01
    beta = 0.5
    
    save_path = os.path.join(save_folder, str(trial_id) + '.txt')

    network = MultilayerNetwork([2,1], beta)
    tr_error, val_error = train_network(network, learning_rate, df_tr, df_val, nbr_iterations, nbr_errors)
    
    tmp_dict = {'tr_error': tr_error, 'val_error': val_error}
    df = pd.DataFrame(tmp_dict)
    df.to_csv(save_path)
    
    return min(tr_error), min(val_error)


def main_a():
    meta_save_folder = 'C:\\Users\\Rasmus\\ANN'
    tr_path = 'C:\\Users\\Rasmus\\Desktop\\train_data_2016.txt'
    val_path =  'C:\\Users\\Rasmus\\Desktop\\valid_data_2016.txt'
    nbr_trials = 100 #100 in assngment
       
    if not os.path.isdir(meta_save_folder):
        raise ValueError('Save folder ' + meta_save_folder + ' is not a directory.')
    save_folder = os.path.join(meta_save_folder, 'Assgnm4a')
    os.mkdir(save_folder)

    df_tr, df_val = load_and_normalize(tr_path, val_path)    
    silly_lst = [[save_folder, df_tr, df_val, 'trial_' + str(i)] for i in range(nbr_trials)]   
    pool = Pool(processes=4)     # start 4 worker processes
    results = [x for x in pool.imap_unordered(single_trial_a, silly_lst)]
    pool.close()

    mean_min_tr_error = np.mean([x[0] for x in results])
    mean_min_val_error = np.mean([x[1] for x in results])

    file_path = os.path.join(save_folder, 'Averages.txt')

    with open(file_path, 'w') as output_file:
        output_file.write("Average of minimum training error: " + str(mean_min_tr_error) + "\n")
        output_file.write("Average of minimum validation error: " + str(mean_min_val_error) + "\n")
    
    print("Average of minimum training error: " + str(mean_min_tr_error))
    print("Average of minimum training error: " + str(mean_min_val_error))
    
 
    return results




def single_trial_b(input_lst):
    [save_folder, df_tr, df_val, trial_id, nbr_hidden_layers] = input_lst

    nbr_iterations = 2e5
    nbr_errors = 500
    learning_rate = 0.01
    beta = 0.5
    
    save_path = os.path.join(save_folder, str(trial_id) + '.txt')

    network = MultilayerNetwork([2,nbr_hidden_layers,1], beta) #Try 2,4,6,8,32 neurons in hidden layer
    tr_error, val_error = train_network(network, learning_rate, df_tr, df_val, nbr_iterations, nbr_errors)
    
    tmp_dict = {'tr_error': tr_error, 'val_error': val_error}
    df = pd.DataFrame(tmp_dict)
    df.to_csv(save_path)
    
    return min(tr_error), min(val_error)




def main_b(nbr_hidden_layers):
    meta_save_folder = 'C:\\Users\\Rasmus\\ANN'
    tr_path = 'C:\\Users\\Rasmus\\Desktop\\train_data_2016.txt'
    val_path =  'C:\\Users\\Rasmus\\Desktop\\valid_data_2016.txt'
    nbr_trials = 25 #100 in assngment
       
    if not os.path.isdir(meta_save_folder):
        raise ValueError('Save folder ' + meta_save_folder + ' is not a directory.')
    save_folder = os.path.join(meta_save_folder, 'Assgnm4b_' + str(nbr_hidden_layers) + '_hidden_layers')
    os.mkdir(save_folder)

    df_tr, df_val = load_and_normalize(tr_path, val_path)    
    silly_lst = [[save_folder, df_tr, df_val, 'trial_' + str(i), nbr_hidden_layers] for i in range(nbr_trials)]   
    pool = Pool(processes=3)     # start 4 worker processes
    results = [x for x in pool.imap_unordered(single_trial_b, silly_lst)]
    pool.close()

    mean_min_tr_error = np.mean([x[0] for x in results])
    mean_min_val_error = np.mean([x[1] for x in results])

    file_path = os.path.join(save_folder, 'Averages.txt')

    with open(file_path, 'w') as output_file:
        output_file.write("Average of minimum training error: " + str(mean_min_tr_error) + "\n")
        output_file.write("Average of minimum validation error: " + str(mean_min_val_error) + "\n")
    
    print("Average of minimum training error: " + str(mean_min_tr_error))
    print("Average of validation training error: " + str(mean_min_val_error))
    
 
    return results



def simple_plot():
    meta_save_folder = 'C:\\Users\\Rasmus\\ANN'
    save_folder = os.path.join(meta_save_folder, 'Assgnm4b')
    for i in range(4):
        path_i = os.path.join(save_folder, 'trial_' + str(i) + '.txt')
        df_i = pd.read_csv(path_i)
        plt.plot(df_i.tr_error)
    plt.show()

def separate_df(df):
    xi_1_red = []
    xi_2_red = []
    xi_1_blue = []
    xi_2_blue = []
    for i in range(len(df)):
        xi1 = df.iloc[i].xi_1
        xi2 = df.iloc[i].xi_2
        zeta = df.iloc[i].zeta
        if zeta == -1:
            xi_1_red.append(xi1)
            xi_2_red.append(xi2)
        else:
            xi_1_blue.append(xi1)
            xi_2_blue.append(xi2)
    return [xi_1_red, xi_2_red],[xi_1_blue, xi_2_blue] 

    
def visualize_raw_data():    
    tr_path = 'C:\\Users\\Rasmus\\Desktop\\train_data_2016.txt'
    val_path =  'C:\\Users\\Rasmus\\Desktop\\valid_data_2016.txt'
    df_tr, df_val = load_and_normalize(tr_path, val_path)    
    #sns.set_style('white')
    fig = plt.figure()
    ax = plt.subplot(111)
    [xi_1_red, xi_2_red],[xi_1_blue, xi_2_blue] = separate_df(df_tr)
    plt.plot(xi_1_red, xi_2_red, 'ro', label = "Training points \n with zeta=-1")
    plt.plot(xi_1_blue, xi_2_blue, 'go', label = "Training points \n with zeta=1")
    [xi_1_red, xi_2_red],[xi_1_blue, xi_2_blue] = separate_df(df_val)
    plt.plot(xi_1_red, xi_2_red, 'bo', label = "Validation points \n with zeta=-1")
    plt.plot(xi_1_blue, xi_2_blue, 'co', label = "Validation points \n with zeta=1")    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.96])
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.setp(legend.get_title(),fontsize='15')
    plt.xlabel("xi_1")
    plt.ylabel("xi_2")

    plt.savefig('C:\\Users\\Rasmus\\Desktop\\raw_data_viz', dpi = 400)  

    
if __name__ == '__main__':
#    results = main_b(2)
#    results = main_b(4)    
#    results = main_b()
    visualize_raw_data()
    
