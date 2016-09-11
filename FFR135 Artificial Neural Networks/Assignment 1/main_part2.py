# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 06:31:13 2016

@author: Rasmus
"""
import numpy as np
import matplotlib.pyplot as plt
import datetime


import hopfield as hf
import patterns_part2 as pp2

def distort_pattern(pattern, fraction_of_bits_to_distort):
    pattern = np.copy(pattern)
    tot_nbr_bits = len(pattern)
    indeces_to_distort = []
    while (len(indeces_to_distort) < fraction_of_bits_to_distort * tot_nbr_bits):
        random_index = np.random.randint(0,tot_nbr_bits)
        if random_index not in indeces_to_distort:
            indeces_to_distort.append(random_index)
    distorted_pattern = pattern
    for index in indeces_to_distort:
        
        distorted_pattern[index] = (-1 * pattern[index])
    return distorted_pattern

def store_original_patterns(hopfield_network):
    hopfield_network.store_pattern(pp2.PATTERN_ZERO)
    hopfield_network.store_pattern(pp2.PATTERN_ONE)
    hopfield_network.store_pattern(pp2.PATTERN_TWO)
    hopfield_network.store_pattern(pp2.PATTERN_THREE)
    hopfield_network.store_pattern(pp2.PATTERN_FOUR)


def test_pattern(original_pattern, q):
    ann = hf.HopfieldNetwork(len(original_pattern))
    store_original_patterns(ann)
    distorted_pattern = distort_pattern(original_pattern, q)
    ann.feed_pattern(distorted_pattern)
    ann.run_until_convergence(synchronous=False)
    success = np.array_equal(original_pattern, ann.neuron_state_vector) #or np.array_equal(-original_pattern, ann.neuron_state_vector) 
#    success = np.array_equal(pp2.SPURIOUS_THREE, ann.neuron_state_vector)
    incorrect_bits = int(sum(abs(original_pattern-ann.neuron_state_vector))/2)
    #print(ann._updates_since_last_reset)
    return success, incorrect_bits

def simulate_successrate(original_pattern, q):
    nbr_of_trials = 1000
    successes = 0
    for i in range(nbr_of_trials):
        successes += test_pattern(original_pattern, q)[0]
    return successes / nbr_of_trials

def simulate_curve(original_pattern):
    M = 100
    q_lst = []
    prob_lst = []
    for i in range(M+1):
        q_i = 1/M * i
        prob_i = simulate_successrate(original_pattern, q_i)
        q_lst.append(q_i)
        prob_lst.append(prob_i)
    return q_lst, prob_lst
 


   
def simulate_and_save():
    path = r"C:\Users\Rasmus\Documents\simulation_results.txt"
    now = datetime.datetime.now()
    with open(path, 'a') as the_file:
        the_file.write("Simulation results " + str(now) + "\n")
        for pattern in pp2.ALL_PATTERNS:
            q_lst, prob_lst = simulate_curve(pattern)
            q_str_lst = [str(x) for x in q_lst]
            p_str_lst = [str(x) for x in prob_lst]
            the_file.write("\t".join(q_str_lst) + "\n")
            the_file.write("\t".join(p_str_lst) + "\n")
        


def plot_from_file():
        path = r"C:\Users\Rasmus\Documents\simulation_results1.txt"
        with open(path, 'r') as the_file:
            content = the_file.readlines()
            print(content)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.hold(True)
        for i in range(0,5):
            q_lst = content[2*i+1].split("\t")
            prob_lst = content[2*(i+1)].split("\t")
            ax.plot(q_lst, prob_lst)
        legend = ["Pattern Zero", "Pattern One", "Pattern Two", "Pattern Three", "Pattern Four"]
        plt.legend(legend)
        plt.title("Recognising distorted patterns")
        plt.xlabel("Fractions of bits flipped")
        plt.ylabel("Probability of recognising pattern")
        plt.show()
        
        

def plot_sim(pattern, ax):
        q_lst, prob_list = simulate_curve(pattern)
        print("\n")
        print(prob_list)
        ax.plot(q_lst,prob_list)

        
def main():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.hold()
    for pattern in pp2.ALL_PATTERNS:
        plot_sim(pattern, ax)
    legend = ["Pattern Zero", "Pattern One", "Pattern Two", "Pattern Three", "Pattern Four"]
    plt.legend(legend)
    plt.title("Recognising distorted patterns")
    plt.xlabel("Fractions of bits flipped")
    plt.ylabel("Probability of recognising pattern")
    plt.show()
    

simulate_and_save()
plot_from_file()
