# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:12:59 2016

@author: Rasmus
"""
#TODO use seaborn and tsplot or violin plot

import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool
import pandas as pd

import hopfield as hf
import pattern_utilities


def steady_state_order_parameter(network, pattern, beta, t_max):
    max_iterations = int(t_max)
    nbr_points_included = int(np.floor(t_max/100))
    m_list = np.zeros(nbr_points_included).tolist()
    for i in range(max_iterations):
        network.update_state(synchronous = False, stochastic = True, beta = beta)
        m_i = (np.transpose(network.neuron_state_vector) @ pattern  / len(pattern) )[0][0]
        index = int(i - max_iterations + nbr_points_included)
        if index >= 0:            
            m_list[index] = m_i
    return np.mean(m_list)


        
# function for  m1  for one datapoint
def steady_state_order_random_patterns(nbr_of_neurons, nbr_of_patterns, beta, t_max):
    network = hf.HopfieldNetwork(nbr_of_neurons)
    stored_patterns = pattern_utilities.store_random_patterns(network, nbr_of_patterns)
    pattern_one = stored_patterns[0]
    network.feed_pattern(pattern_one)
    m1 = steady_state_order_parameter(network, pattern_one, beta, t_max)
    return m1
        
        
def order_wrapper(input_lst):
    [nbr_of_neurons, nbr_of_patterns, beta, t_max] = input_lst
    return steady_state_order_random_patterns(nbr_of_neurons, nbr_of_patterns, beta, t_max)
        

def simulate_order_parameter(nbr_of_neurons, nbr_of_patterns, beta, nbr_of_data_points, t_max):
    silly_lst = [[nbr_of_neurons, nbr_of_patterns, beta, t_max] for i in range(nbr_of_data_points)]   
    pool = Pool(processes=4)     # start 4 worker processes
    results =   [x for x in pool.imap_unordered(order_wrapper, silly_lst)]
    pool.close()
    return results
    
   
def make_curve(beta, path = None):
    nbr_of_neurons = 25
    
    p_lst = [11,30]
    m1_means = np.zeros(len(p_lst))
    m1_upper = np.zeros(len(p_lst))
    m1_lower = np.zeros(len(p_lst))
    alphas = np.zeros(len(p_lst))
    
    for index, p in enumerate(p_lst):
 
        results = simulate_order_parameter(nbr_of_neurons, p, beta, 10, 1e4)
        mean = np.mean(results)
        std = np.std(results)
 
        alphas[index] = p/nbr_of_neurons 
        m1_means[index] = mean
        m1_upper[index] = mean + std
        m1_lower[index] = mean - std
    
    dic = {"Alpha": alphas, "Average_m1": m1_means, "Upper": m1_upper, "Lower": m1_lower, "p":p_lst}
    df = pd.DataFrame(dic)
    if path != None:
        df.to_csv(path)
    return df
    

def plot_results(df, save_path, df_path = None):
    if df_path != None:
        df = pd.read_csv(df_path)    
    plt.plot(df.Alpha,df.Average_m1)
    plt.fill_between(df.Alpha, df.Lower,df.Upper, alpha = '0.5')
    plt.xlabel('Alpha')
    plt.ylabel('m1')
    plt.legend(['Average m1, with shading showing the spread'])
    plt.title("Simulation results for the Steady-State Order Parameter")
    plt.savefig(save_path, dpi = 800)
    
def multiplot(df_lst, save_path):
    legend = []
    for df in df_lst:
        plt.plot(df.Alpha,df.Average_m1)
        legend.append(str(df.p.iloc[-1]) + " patterns")
    plt.legend(legend)
    plt.xlabel('Alpha')
    plt.ylabel('m1')
    plt.title("Simulation results for the Steady-State Order Parameter")
    plt.show()
    #plt.savefig(save_path, dpi = 800)

def plot_from_files():
    df50 = pd.read_csv(r'C:\Users\Rasmus\p50.txt')
    df100 = pd.read_csv(r'C:\Users\Rasmus\p100.txt')
    df250 = pd.read_csv(r'C:\Users\Rasmus\p250.txt')
    df500 = pd.read_csv(r'C:\Users\Rasmus\p500.txt')
    df_lst = [df50, df100, df250, df500]
    multiplot(df_lst, r'C:\Users\Rasmus\multiplot.png')
    
if __name__ == '__main__':
    #save_path = r'C:\Users\Rasmus\Documents\plotb.png'
    #df_path = r'C:\Users\Rasmus\Documents\assgn1_3a.txt'
    #df = make_curve(2, df_path)
    #plot_results(df, save_path)
    plot_from_files()
