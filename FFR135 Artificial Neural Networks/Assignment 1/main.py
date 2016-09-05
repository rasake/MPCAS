# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:13:19 2016

@author: Rasmus
"""
import numpy as np
import hopfield as hf


def create_random_pattern(pattern_length):
    temp_lst = [np.sign(2*(np.random.rand()-0.5)) for x in range(pattern_length)] 
    return np.reshape(np.array(temp_lst), [pattern_length, 1])
    
def store_random_patterns(hopfield_network, nbr_of_patterns):
    patterns = [create_random_pattern(hopfield_network._NBR_OF_CELLS) for x in range(nbr_of_patterns)]
    for pattern_i in patterns:
        hopfield_network.store_pattern(pattern_i)
    return patterns

def simulate_on_step_error_prob(pattern_length, nbr_of_patterns):
    hopfield_network = hf.HopfieldNetwork(pattern_length)
    stored_patterns = store_random_patterns(hopfield_network, nbr_of_patterns)
    nbr_of_tests = int(600 / pattern_length)
    temp_patterns = [stored_patterns[np.random.randint(nbr_of_tests)] for x in range(nbr_of_tests)]
    one_step_errors = 0
    for pattern_i in temp_patterns:
        hopfield_network.feed_pattern(pattern_i)
        hopfield_network.update_state()
        print(sum(abs(pattern_i - hopfield_network.neuron_state_vector)))
        one_step_errors += np.sum(abs(pattern_i - hopfield_network.neuron_state_vector))
    print(one_step_errors)
    print(hopfield_network._NBR_OF_CELLS)
    return one_step_errors/ (nbr_of_tests * pattern_length)

    
print(simulate_on_step_error_prob(100,20))

    
# randomly select a few of the stored patterns, feed them to the network one at a time, check succesrate for each after on step
    
    
"""

s = np.array([[-1],[-1]])
W = np.array([[0,1],[0,1]])
u = np.array([[-1],[-1]])


Albert = hf.HopfieldNetwork(2)

Albert.feed_pattern(s)

Albert.store_pattern(u)
Albert.store_pattern(u)

print(Albert.weights)

print(Albert.neuron_state_vector)
print(Albert.update_state())
print(Albert.neuron_state_vector)
"""
