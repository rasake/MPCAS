# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:12:59 2016

@author: Rasmus
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from multiprocessing import Pool


import hopfield as hf
import pattern_utilities


def steady_state_order(network, pattern, beta, t_max):
    tmp = np.transpose(network.neuron_state_vector) @ pattern / len(pattern)
    print("tmp = " +str(tmp))
    for i in range(t_max):
        network.update_state(synchronous = False, stochastic = True, beta = beta)
        tmp += np.transpose(network.neuron_state_vector) @ pattern  / len(pattern)
    print("Called function steady_state_order, tmp/t_max = " + str(tmp/t_max))
    return (tmp/t_max)[0][0]
        
# fuunction for  m1  for one datapoint
def steady_state_order_random_patterns(nbr_of_patterns, nbr_of_neurons, beta, t_max):
    network = hf.HopfieldNetwork(nbr_of_neurons)
    stored_patterns = pattern_utilities.store_random_patterns(network, nbr_of_patterns)
    pattern_one = stored_patterns[0]
    network.feed_pattern(pattern_one)
    m1 = steady_state_order(network, pattern_one, beta, t_max)
    print("m1 = " + str(m1))
    return m1
        
        
def order_wrapper(input_lst):
    [nbr_of_patterns, nbr_of_neurons, beta, t_max] = input_lst
    return steady_state_order_random_patterns(nbr_of_patterns, nbr_of_neurons, beta, t_max)
        

def simulate_order_parameter(nbr_of_neurons, nbr_of_patterns, beta, nbr_of_data_points, t_max):
    silly_lst = [[nbr_of_patterns, nbr_of_neurons, beta, t_max] for i in range(nbr_of_data_points)]   
    pool = Pool(processes=4)              # start 4 worker processes
    for m1_i in pool.imap_unordered(order_wrapper, silly_lst):
            print(m1_i)
    
    
    
    
    
#   
#def simulate_and_save():
#    path = r"C:\Users\Rasmus\Documents\simulation_results_temp.txt"
#    now = datetime.datetime.now()
#    with open(path, 'a') as the_file:
#        the_file.write("Simulation results " + str(now) + "\n")
#        for pattern in pp2.ALL_PATTERNS:
#            q_lst, prob_lst = simulate_curve(pattern)
#            q_str_lst = [str(x) for x in q_lst]
#            p_str_lst = [str(x) for x in prob_lst]
#            the_file.write("\t".join(q_str_lst) + "\n")
#            the_file.write("\t".join(p_str_lst) + "\n")
#            


def f(x):
    return x*x

if __name__ == '__main__':
    simulate_order_parameter(100,20,10,10, 2000)