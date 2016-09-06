# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:13:19 2016

@author: Rasmus
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import hopfield as hf


def create_random_pattern(pattern_length):
    temp_lst = [np.sign(2*(np.random.rand()-0.5)) for x in range(pattern_length)] 
    return np.reshape(np.array(temp_lst), [pattern_length, 1])
    
def store_random_patterns(hopfield_network, nbr_of_patterns):
    patterns = [create_random_pattern(hopfield_network._NBR_OF_CELLS) for x in range(nbr_of_patterns)]
    for pattern_i in patterns:
        hopfield_network.store_pattern(pattern_i)
    return patterns

def simulate_one_step_error_prob(pattern_length, nbr_of_patterns):
    hopfield_network = hf.HopfieldNetwork(pattern_length)
    stored_patterns = store_random_patterns(hopfield_network, nbr_of_patterns)
    one_step_errors = 0
    for pattern_i in stored_patterns:
        hopfield_network.feed_pattern(pattern_i)
        hopfield_network.update_state()
        one_step_errors += np.sum(abs(pattern_i - hopfield_network.neuron_state_vector)) / 2 # Dvision by two since bits are either 1 or -1 so the difference is 2 or -2 if a bit flips
    return one_step_errors/ (len(stored_patterns) * hopfield_network._NBR_OF_CELLS)


def simulate_prob_curve():
    N = [100, 200]
    P = [10, 20, 30, 40, 50, 75, 100, 150, 200]
    P_over_N = np.zeros(len(N)*len(P))
    probabilities = np.zeros(len(N)*len(P))
    for i, N_i in enumerate(N):
        for j, P_i in enumerate(P):
            P_over_N[i+j] = P_i / N_i
            probabilities[i+j] = simulate_one_step_error_prob(N_i,P_i)
    return (P_over_N, probabilities)

def make_prob_comp_plot():
    x = np.linspace(0.001,1)
    analytical_prob = [0.5*(1-math.erf(math.sqrt(1/x_i/2))) for x_i in x]
    simulated_curve = simulate_prob_curve()
    plt.plot(simulated_curve[0], simulated_curve[1], 'rx')
    plt.plot(x, analytical_prob)    
    plt.show()
    

make_prob_comp_plot()
    
