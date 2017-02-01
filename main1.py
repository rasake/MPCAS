# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:23:33 2017

@author: Rasmus
"""
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

def run_model_wrapper(args_lst):
    model = args_lst[0]
    N0 = args_lst[1]
    nbr_iterations = args_lst[2]
    return run_model(model, N0, nbr_iterations)

def run_model(model, N0, nbr_iterations):
    N_lst = np.zeros((1,nbr_iterations)).flatten().tolist()
    N=N0
    for i in range(nbr_iterations):
        N_lst[i] = N
        N = model(N)
    N_lst.append(N)
    return N_lst

def model1(N_i):
    K = 1000
    r = 0.1
    b = 1

    return (r+1)*N_i/(1+(N_i/K)**b)
    
def model1_lin_b(N_i):
    r = 0.1
    derivative = r+1
    return N_i*derivative


def model1_lin_c(N_i):
    r = 0.1
    b = 1
    derivative = 1-r*b/(r+1)
    #derivative = r+1
    return 100+(N_i-100)*derivative    
    

def mainb():   
    N0_lst = [1,2,3,10]
    nbr_iterations = 100
    
    args_lst = [[model1,x,nbr_iterations] for x in N0_lst]
    args_lst_lin = [[model1_lin_b,x,nbr_iterations] for x in N0_lst]

    pool = multiprocessing.Pool(processes=4)
    data = pool.map(run_model_wrapper, args_lst)
    data_lin = pool.map(run_model_wrapper, args_lst_lin)
    
    legends = []    
    plt.figure(figsize = (8,4.5))
    for i, N0 in enumerate(N0_lst):
        p = plt.loglog(data[i])
        plt.loglog(data_lin[i], color=p[0].get_color(), linestyle = 'dashed')
        legends.append('Exact dynamics with N0='+str(N0))
        legends.append('Linearized dynamics with N0='+str(N0))
    plt.xlabel('t')
    plt.ylabel('N')
    plt.legend(legends,loc='center left',bbox_to_anchor=(1, 0.5),
          fancybox=True, shadow=True, ncol=1)  
    plt.title('Effect of linearization around unstable steady state N*=0')
    plt.savefig('plot1b.png', dpi=800)

def mainc():   
    N0_lst = [90,95,97,80]
    nbr_iterations = 100
    
    args_lst = [[model1,x,nbr_iterations] for x in N0_lst]
    args_lst_lin = [[model1_lin_c,x,nbr_iterations] for x in N0_lst]

    pool = multiprocessing.Pool(processes=4)
    data = pool.map(run_model_wrapper, args_lst)
    data_lin = pool.map(run_model_wrapper, args_lst_lin)
    
    legends = []
    plt.figure(figsize = (8,4.5))
    for i, N0 in enumerate(N0_lst):
        p = plt.plot(data[i])
        plt.plot(data_lin[i], color=p[0].get_color(), linestyle = 'dashed')
        legends.append('Exact dynamics with N0='+str(N0))
        legends.append('Linearized dynamics with N0='+str(N0))
    plt.xlabel('t')
    plt.ylabel('N')
    plt.legend(legends)
    plt.title('Effect of linearization around stable steady state N*=100')
    plt.savefig('plot1c.png', dpi=800)

if __name__ == "__main__": 
    mainb()
    mainc()