# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:13:19 2016

@author: Rasmus
"""
import numpy as np
import hopfield as hf

s = np.array([[-1],[1]])
W = np.array([[0,1],[0,1]])

Albert = hf.HopfieldNetwork(2,s,W)

print(Albert.neuron_state_vector)

print(Albert.update_state())

print(Albert.neuron_state_vector)

print(Albert.update_state())

print(Albert.neuron_state_vector)
