# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 12:23:28 2016

@author: Rasmus
"""
import numpy as np

class HopfieldNetwork:
    def __init__(self, nbr_of_cells, initial_pattern = None, initial_weights = None):
        if initial_pattern is None:
            initial_pattern = np.ones([nbr_of_cells, 1])
        if initial_weights is None:
            initial_weights = np.ones([nbr_of_cells, nbr_of_cells])
        self._NBR_OF_CELLS = nbr_of_cells
        self.neuron_state_vector = initial_pattern
        self.weights = initial_weights
        self._updates_since_last_reset = 0

    @property
    def neuron_state_vector(self):
        return self._neuron_state_vector

    @neuron_state_vector.setter
    def neuron_state_vector(self, pattern_vector):
        if len(pattern_vector) != self._NBR_OF_CELLS:
            raise ValueError("Size of Neural Network cannot change")
        self._neuron_state_vector = pattern_vector

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights):
        if np.shape(new_weights) != (self._NBR_OF_CELLS, self._NBR_OF_CELLS):
            raise ValueError("Weight matrix cannot change size")
        self._weights = np.copy(new_weights)                

    
    def feed_pattern(self, pattern_vector):
        self.neuron_state_vector = pattern_vector

               
    def store_pattern(self, pattern_vector):
        if len(pattern_vector) != self._NBR_OF_CELLS:
            raise ValueError("Pattern length must match number of neurons")
        temp_weights = pattern_vector @ np.transpose(pattern_vector) / self._NBR_OF_CELLS
        np.fill_diagonal(temp_weights,0)       
        self._weights += temp_weights

    def update_state(self):
        new_state = np.sign(self._weights @ self._neuron_state_vector)
        is_done = np.array_equal(self.neuron_state_vector, new_state)
        self.neuron_state_vector = np.copy(new_state)
        self._updates_since_last_reset +=1
        return is_done