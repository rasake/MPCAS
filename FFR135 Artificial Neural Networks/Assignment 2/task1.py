# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:43:19 2016

@author: Rasmus
"""
import numpy as np
from numpy.random import rand
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns

import kohonen

def rand_tri():
    x = rand()
    y = rand()
    inside_triangle = (x<0.5 and y<x*sqrt(3)) or (x>0.5 and y<(1-x)*sqrt(3))
    if inside_triangle:
        return np.reshape([x,y], [2,1])
    else:
        return rand_tri()

        

def main():
    nbr_neurons = 100
    t_max_order_phase = 1000
    t_max_conv_phase = 50000
    start_sigma = 5
    start_eta = 0.1
    conv_sigma = 0.9
    conv_eta = 0.01
    tau = 200
    save_path = r'C:\Users\Rasmus\Desktop\assgn21_.png'

    weight_matrix = np.random.rand(nbr_neurons,2)
    positions = [x for x in range(nbr_neurons)]
    input_distr = [rand_tri() for i in range(1000)]
    triangle_x = [0, 0.5, 1, 0]
    triangle_y = [0, sqrt(3)/2, 0, 0 ]
    
    plt.axis([-0.1, 1.1, -0.1, 1.1])
    #plot outline of triangle
    plt.plot(triangle_x,triangle_y)

    
    #ordering phase
    for t in range(t_max_order_phase):
        tmp = np.exp(-t/tau)
        sigma = start_sigma*tmp
        eta = start_eta*tmp
        sample = input_distr[np.random.randint(1000)]
        kohonen.update_weight_matrix(weight_matrix, positions, sample, sigma, eta)
    plt.plot(weight_matrix[:,0], weight_matrix[:,1], 'ro')
        
    
    #convergence phase; same but with fixed eta, sigma
    sigma = conv_sigma
    eta = conv_eta


    #converging phase
    for t in range(t_max_conv_phase):
        sample = input_distr[np.random.randint(1000)]
        kohonen.update_weight_matrix(weight_matrix, positions, sample, sigma, eta)    
    #plot new weight_matrix
    plt.plot(weight_matrix[:,0], weight_matrix[:,1], 'go')
    
    legend1 = 'Outline of sampled input distribution'
    legend2 = 'Weights after ordering phase'
    legend3 = 'Weights after convergence phase'
    plt.legend([legend1, legend2, legend3], frameon=True)
    plt.savefig(save_path, dpi = 800)



if __name__ == '__main__':
    main()