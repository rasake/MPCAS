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
            initial_weights = np.zeros([nbr_of_cells, nbr_of_cells])
        self._NBR_OF_CELLS = nbr_of_cells
        self.neuron_state_vector = initial_pattern
        self.weights = initial_weights
        self._updates_since_last_reset = 0
        self._pseudo_stable_bits = np.ones([nbr_of_cells, 1])

    @property
    def neuron_state_vector(self):
        return np.copy(self._neuron_state_vector)

    @neuron_state_vector.setter
    def neuron_state_vector(self, pattern_vector):
        if len(pattern_vector) != self._NBR_OF_CELLS:
            raise ValueError("Size of Neural Network cannot change")
        self._neuron_state_vector = np.copy(pattern_vector)


    def set_neuron(self,index, value):
        if (value != 1 and value != -1):
            message = ("Cannot set neuron " + str(index) + " to " + str(value)
                        + ", neuron states must be either +1 or -1.")
            raise ValueError(message)
        if index < 0:
            raise ValueError("Index must be positive")
        if (index > self._NBR_OF_CELLS - 1):
            message = ("Cannot set neuron, index " + str(index) + " out of bounds "
                        + "for Hopfield Network with size " + str(self._NBR_OF_CELLS)  )
            raise IndexError(message)
        self._neuron_state_vector[index] = value
            
    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights):
        if np.shape(new_weights) != (self._NBR_OF_CELLS, self._NBR_OF_CELLS):
            raise ValueError("Weight matrix cannot change size")
        self._weights = np.copy(new_weights)   

    
    def feed_pattern(self, pattern_vector):
        self.neuron_state_vector = np.copy(pattern_vector)
        self._updates_since_last_reset = 0

               
    def store_pattern(self, pattern_vector):
        if len(pattern_vector) != self._NBR_OF_CELLS:
            raise ValueError("Pattern length must match number of neurons")
        temp_weights = pattern_vector @ np.transpose(pattern_vector) / self._NBR_OF_CELLS
        np.fill_diagonal(temp_weights,0)       
        self.weights += temp_weights


    def update_state(self, synchronous = True):
        if synchronous: #Synchronous updating, all bits updated at once in parallell
            new_state = np.sign(self._weights @ self._neuron_state_vector)
            is_done = np.array_equal(self.neuron_state_vector, new_state)
            self.neuron_state_vector = new_state
        else: #Asynchronous updating, only one bit will change
            r = np.random.randint(0, self._NBR_OF_CELLS) #Start inclusive, stop exclusive
            new_neuron_value = np.sign( self.weights[r] @ self.neuron_state_vector )
            is_flipped = (new_neuron_value != self.neuron_state_vector[r])
            if is_flipped:
                self._pseudo_stable_bits = 0 * self._pseudo_stable_bits
            else:
                self._pseudo_stable_bits[r] = 1
            is_done = np.all()
            self.set_neuron(r, new_neuron_value)           
        self._updates_since_last_reset +=1
        return is_done
