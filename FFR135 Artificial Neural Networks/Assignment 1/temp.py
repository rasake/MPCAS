# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 06:31:13 2016

@author: Rasmus
"""
import numpy as np
import hopfield as hf



ann = hf.HopfieldNetwork(4)
pattern_lst = [1, 1, -1, 1]
pattern = np.reshape(np.array(pattern_lst), [4, 1])
ann.store_pattern(pattern)
ann.set_neuron(1,-1)

print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))
ann.update_state(synchronous=False)
print (np.transpose(ann.neuron_state_vector))#print_pattern(four_pattern)
