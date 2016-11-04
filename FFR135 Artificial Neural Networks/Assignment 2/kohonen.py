# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:51:42 2016

@author: Rasmus
"""
import numpy as np
from numpy.linalg import norm

def neighbourhood_function(positions, winning_neuron_index, sigma):
    win_pos = positions[winning_neuron_index]
    return [np.exp(- norm(pos_i-win_pos)**2/(2*sigma**2) ) for pos_i in positions]

def fold_neurons(nbr_neurons, nbr_folds):
    if nbr_folds == 0:
        raise ValueError('There has to be at least one fold')
    return [np.array([index//nbr_folds, index%nbr_folds]) for index in range(nbr_neurons)]

def find_winning_neuron(weight_matrix, pattern):
    nbr_neurons, input_dim = np.shape(weight_matrix)
    euclidian_dist = [norm(weight_matrix[i,:]-np.reshape(pattern, [input_dim])) for i in range(nbr_neurons)]
    return np.argmin(euclidian_dist)


def update_weight_matrix(weight_matrix, positions, sample, sigma, eta):
     #Updates weight matrix IN PLACE (!)
     nbr_neurons, input_dim = np.shape(weight_matrix)
     winning_neuron = find_winning_neuron(weight_matrix, sample)
     proximity_factors = neighbourhood_function(positions, winning_neuron, sigma)
     delta_w = [proximity_factors[i]*(np.reshape(sample, [input_dim]) - weight_matrix[i,:]) for i in range(nbr_neurons)]
     weight_matrix += eta * np.reshape(delta_w, [nbr_neurons, input_dim])