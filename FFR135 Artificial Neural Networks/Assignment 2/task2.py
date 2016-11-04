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

def load_wine_data():
    path = r'C:\Users\Rasmus\Documents\GitHub\MPCAS\FFR135 Artificial Neural Networks\Assignment 2\wine_data.txt'
    my_data = np.genfromtxt(path, delimiter=',')
    wine_data = np.reshape(my_data[:,1:], [len(my_data),13])
    for i in range(13): #normalization
        mean = np.mean(wine_data[:,i])
        std = np.std(wine_data[:,i])
        wine_data[:,i] = (wine_data[:,i]-mean) / std
    wine_class = my_data[:,0]
    return wine_data, wine_class

def main():
    nbr_neurons = 400
    nbr_folds = 20
    t_max_order_phase = 1000
    t_max_conv_phase = 20000
    start_sigma = 30
    start_eta = 0.1
    conv_sigma = 0.9
    conv_eta = 0.01
    tau = 300
    save_path = r'C:\Users\Rasmus\Desktop\assgn22.png'
    backup_path = r'C:\Users\Rasmus\Desktop\assgn22.txt'

    wine_data, wine_class = load_wine_data()
    weight_matrix = np.random.rand(nbr_neurons,13)
    nbr_wines = len(wine_data)
    positions = kohonen.fold_neurons(nbr_neurons,nbr_folds)
    
    #ordering phase
    for t in range(t_max_order_phase):
        tmp = np.exp(-t/tau)
        sigma = start_sigma*tmp
        eta = start_eta*tmp
        sample = wine_data[np.random.randint(nbr_wines)]
        kohonen.update_weight_matrix(weight_matrix, positions, sample, sigma, eta)
        
    
    #convergence phase; same but with fixed eta, sigma
    sigma = conv_sigma
    eta = conv_eta
    #converging phase
    for t in range(t_max_conv_phase):
        sample = wine_data[np.random.randint(nbr_wines)]
        kohonen.update_weight_matrix(weight_matrix, positions, sample, sigma, eta)
        
    np.savetxt(backup_path, weight_matrix, delimiter=",")

    winning_neurons = [kohonen.find_winning_neuron(weight_matrix, pattern) for pattern in wine_data]

    class1 = []
    class2 = []
    class3 = []
    for i,neuron in enumerate(winning_neurons):
        if wine_class[i] == 1:
            class1.append(positions[neuron])
        elif wine_class[i] == 2:
            class2.append(positions[neuron])
        elif wine_class[i] == 3:
            class3.append(positions[neuron])
        else:
            pass
    class1 = np.reshape(class1, [len(class1),2])
    class2 = np.reshape(class2, [len(class2),2])
    class3 = np.reshape(class3, [len(class3),2])
    
    plt.plot(class1[:,0], class1[:,1], 'co', opacity=0.3)
    plt.plot(class2[:,0], class2[:,1], 'go')
    plt.plot(class3[:,0], class3[:,1], 'ro')
    plt.axis([0, 25, 0, 25])

    #    class1_x = [positions[neuron][0] for i,neuron in enumerate(winning_neurons) if wine_class[i]==1 ]
#    class1_y = [positions[neuron][1] for i,neuron in enumerate(winning_neurons) if wine_class[i]==1 ]
#    class2_x = [positions[neuron][0] for i,neuron in enumerate(winning_neurons) if wine_class[i]==2 ]
#    class2_y = [positions[neuron][1] for i,neuron in enumerate(winning_neurons) if wine_class[i]==2 ]
#    class3_x = [positions[neuron][0] for i,neuron in enumerate(winning_neurons) if wine_class[i]==3 ]
#    class3_y = [positions[neuron][1] for i,neuron in enumerate(winning_neurons) if wine_class[i]==3 ]
#
#    plt.plot(class1_x,class1_y, 'go')
#    plt.plot(class2_x,class2_y, 'co')
#    plt.plot(class3_x,class3_y, 'ro')
    
    plt.legend(['Wine class 1', 'Wine class 2', 'Wine class 3'], frameon=True)
    plt.axis([0, 25, 0, 25])
    plt.savefig(save_path, dpi=800)
    
    
if __name__ == '__main__':
    win = main()