# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:19:57 2016

@author: Rasmus
"""

import numpy as np

def create_random_pattern(pattern_length):
    temp_lst = [np.sign(2*(np.random.rand()-0.5)) for x in range(pattern_length)] 
    return np.reshape(np.array(temp_lst), [pattern_length, 1])
    
def store_random_patterns(hopfield_network, nbr_of_patterns):
    patterns = [create_random_pattern(hopfield_network._NBR_OF_CELLS) for x in range(nbr_of_patterns)]
    for pattern_i in patterns:
        hopfield_network.store_pattern(pattern_i)
    return patterns