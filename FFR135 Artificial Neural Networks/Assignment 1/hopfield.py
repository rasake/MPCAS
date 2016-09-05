# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 12:23:28 2016

@author: Rasmus
"""
import numpy as np

class HopfieldNetwork:
    def __init__(self, nbr_of_cells, initial_pattern = None, initial_weights = None):
        """assert(nbr_of_cells >0)
        if initial_pattern == None:
            initial_pattern = ones(nbr_of_cells)
        if initial_weights == None:
            initial_weights= zero_matrix(nbr_of_cells, nbr_of_cells)
        assert(len(initial_pattern) == nbr_of_cells) # size operation correct?
        """
        self.__NBR_OF_CELLS = nbr_of_cells
        self.__neuron_state_vector = initial_pattern
        self.__weights = initial_weights
        self.__updates_since_last_reset = 0

    @property
    def neuron_state_vector(self):
        return self.__neuron_state_vector

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def temperature(self, new_weights):
        """
        if shape(self.__weights) != shape(new_weights):
            raise ValueError("Weight matrix cannot change size")
        """
        self.__weights = new_weights
        
    
    def feed_pattern(self, pattern_vector):
        #TODO assert length
        self.__neuron_state_vector    

        
        
    def store_pattern(self, pattern_vector):
        #TODO assert length
        temp_weights = pattern_vector @ np.transpose(pattern_vector) / self.__NBR_OF_CELLS
        self.__weightsnp.fill_diagonal(temp_weights,0)

    def update_state(self):
        self.neuron_state_vector = self.__weights @ self.__neuron_state_vector