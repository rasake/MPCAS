# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:13:19 2016

@author: Rasmus
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import hopfield as hf
import pattern_utilities


def test_stored_patterns(hopfield_network, stored_patterns):
    one_step_errors = 0
    for pattern_i in stored_patterns:
        hopfield_network.feed_pattern(pattern_i)
        hopfield_network.update_state()
        one_step_errors += np.sum(abs(pattern_i - hopfield_network.neuron_state_vector)) / 2 # Dvision by two since bits are either 1 or -1 so the difference is 2 or -2 if a bit flips
    return one_step_errors/ (len(stored_patterns) * hopfield_network._NBR_OF_CELLS)

def simulate_one_step_error_prob(pattern_length, nbr_of_patterns):
    nbr_of_cycles = int(max(1, 1000000/(pattern_length*nbr_of_patterns)))
    prob_list = np.zeros(nbr_of_cycles)
    for i in range(nbr_of_cycles):
        hopfield_network = hf.HopfieldNetwork(pattern_length)
        stored_patterns = pattern_utilities.store_random_patterns(hopfield_network, nbr_of_patterns)
        prob_list[i] = test_stored_patterns(hopfield_network, stored_patterns)  
    return np.mean(prob_list)

def simulate_prob_curve():
    N = [100, 200]
    P = [10, 20, 30, 40, 50, 75, 100, 150, 200]
    P_over_N = np.zeros(len(N)*len(P))
    probabilities = np.zeros(len(N)*len(P))
    k = 0;
    for N_i in N:
        for P_i in P:
            P_over_N[k] = P_i / N_i
            probabilities[k] = simulate_one_step_error_prob(N_i,P_i)
            k += 1
    return (P_over_N, probabilities)

def make_prob_comp_plot():
    x = np.linspace(0.001,2.5)
    analytical_prob = [0.5*(1-math.erf(math.sqrt(1/x_i/2))) for x_i in x]
    simulated_curve = simulate_prob_curve()
    plt.plot(simulated_curve[0], simulated_curve[1], 'rx')
    plt.plot(x, analytical_prob)    
    plt.show()

make_prob_comp_plot()
    
