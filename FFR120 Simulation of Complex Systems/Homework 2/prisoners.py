# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:01:21 2016

@author: Rasmus
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import cv2
import os


def maxelements(seq): # @John Machin
    ''' Return list of position(s) of largest element '''
    if not seq: return []
    max_val = seq[0] if seq[0] >= seq[-1] else seq[-1]
    max_indices = []
    for i, val in enumerate(seq):
        if val < max_val: continue
        if val == max_val:
            max_indices.append(i)
        else:
            max_val = val
            max_indices = [i]
    return max_indices


class PeriodicMatrix(np.matrix):
     def __getitem__(self, index):
         nbr_rows, nbr_columns = self.shape
         try:
             row_index, column_index = index
         except TypeError:
             row_index = index % nbr_rows
             return super().__getitem__(row_index)
         else:
             row_index = row_index % nbr_rows
             column_index = column_index % nbr_columns
             return super().__getitem__((row_index, column_index))

     def __setitem__(self, index, value):
         nbr_rows, nbr_columns = self.shape
         try:
             row_index, column_index = index
         except TypeError:
             row_index = index % nbr_rows
             return super().__setitem__(row_index, value)
         else:
             row_index = row_index % nbr_rows
             column_index = column_index % nbr_columns
             return super().__setitem__((row_index, column_index), value)
                  

class Player(object):
    
    def __init__(self, patience = 0):
        self.patience = patience
        self.rounds_played = 0
        self.betrayed = False
    
    def reset(self):
        self.rounds_played
        self.betrayed = False

    @property
    def action(self):
        if self.betrayed or (self.rounds_played >= self.patience):
            self.rounds_played += 1
            return "defect"
        else:
            self.rounds_played += 1
            return "cooperate"
            
 

def play_game(patience1, patience2, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off):       
    player1_pay_off = 0
    player2_pay_off = 0
    player1 = Player(patience1)
    player2 = Player(patience2)
    for k in range(nbr_rounds):
        action1 = player1.action
        action2 = player2.action
        if action1 == 'cooperate' and action2 == 'cooperate':
            #print("Full cooperation")
            player1_pay_off += reward_pay_off
            player2_pay_off += reward_pay_off
        elif action1 == 'cooperate' and action2 == 'defect':
            #print("ply1: coop., ply2: defect")            
            player1_pay_off += sucker_pay_off
            player2_pay_off += temptation_pay_off
            player1.betrayed = True
        elif action1 == 'defect' and action2 == 'cooperate':
            #print("ply1: defect, ply2: coop.")
            player1_pay_off += temptation_pay_off
            player2_pay_off += sucker_pay_off
            player2.betrayed = True
        elif action1 == 'defect' and action2 == 'defect':
            #print("full defection")
            player1_pay_off += punishment_pay_off
            player2_pay_off += punishment_pay_off             
    return player1_pay_off, player2_pay_off
    



def evaluate_strategies(strategy_matrix, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off):
    nbr_rows, nbr_columns = strategy_matrix.shape
    payoff_matrix = strategy_matrix*0
    for i in range(nbr_rows):
        for j in range(nbr_columns):
            payoff_matrix[i,j] += play_game(strategy_matrix[i,j], strategy_matrix[i-1,j], nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)[0]
            payoff_matrix[i,j] += play_game(strategy_matrix[i,j], strategy_matrix[i+1,j], nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)[0]
            payoff_matrix[i,j] += play_game(strategy_matrix[i,j], strategy_matrix[i,j-1], nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)[0]
            payoff_matrix[i,j] += play_game(strategy_matrix[i,j], strategy_matrix[i,j+1], nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)[0]
    return payoff_matrix

def update_strategies(strategy_matrix, pay_off_matrix, nbr_rounds, p_mut):
    nbr_rows, nbr_columns = strategy_matrix.shape
    new_strategy_matrix = PeriodicMatrix(np.copy(strategy_matrix))
    for i in range(nbr_rows):
        for j in range(nbr_columns):
            if np.random.rand() > p_mut:
                scores = [pay_off_matrix[i,j], pay_off_matrix[i-1,j], pay_off_matrix[i+1,j], pay_off_matrix[i,j-1], pay_off_matrix[i,j+1]]
                strategies = [strategy_matrix[i,j], strategy_matrix[i-1,j], strategy_matrix[i+1,j], strategy_matrix[i,j-1], strategy_matrix[i,j+1]]
                winners = maxelements(scores)
                #print(scores)
                winner = winners[np.random.randint(len(winners))]
                #print(winner)
                new_strategy_matrix[i,j] = strategies[winner]
            else:
                new_strategy_matrix[i,j] = np.random.randint(nbr_rounds+1)

    return new_strategy_matrix
    



def run_cellular_automaton(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, p_mut, board_size = 32):
    
    strategy_matrix = PeriodicMatrix(np.floor(np.random.rand(board_size, board_size)*(nbr_rounds+1)))
    
    strategy_time_evolution = np.zeros([nbr_time_steps, nbr_rounds+1])
    for k in range(nbr_rounds+1):
        strategy_time_evolution[0,k] = np.sum(strategy_matrix == k)/board_size**2    
    for t in range(1,nbr_time_steps):
        pay_off_matrix = evaluate_strategies(strategy_matrix,nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
        strategy_matrix = update_strategies(strategy_matrix, pay_off_matrix, nbr_rounds, p_mut)
        sns.heatmap(strategy_matrix, vmin = 0, vmax = nbr_rounds)
        plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\ca_" + str(t) + ".png", dpi = 400)
        plt.close()

        for k in range(nbr_rounds+1):
            strategy_time_evolution[t,k] = np.sum(strategy_matrix == k)/board_size**2


    legend_strings = []
    for k in range(nbr_rounds+1):
        plt.plot(strategy_time_evolution[:,k])
        legend_strings.append("S_" + str(k))
    plt.legend(legend_strings)
        
        

def main():
    
    nbr_time_steps = 100
    nbr_rounds = 6
    reward_pay_off = 1
    temptation_pay_off = 1.5
    sucker_pay_off = 0
    punishment_pay_off = 0.5
    p_mut = 1/32**2

    run_cellular_automaton(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, p_mut)
    
    #strategy_matrix = PeriodicMatrix(np.round(np.random.rand(32,32)*nbr_rounds))
    #pay_off_matrix = evaluate_strategies(strategy_matrix,nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
    #update_strategies(strategy_matrix, pay_off_matrix, nbr_rounds, p_mut)
    
    #sns.heatmap(strategy_matrix)
    #plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\ca.png", dpi = 400)
    
    """

    vvw           =   cv2.VideoWriter('mymovie.avi',cv2.VideoWriter_fourcc('X','V','I','D'),24,(640,480))
    frameslist    =   os.listdir("C:\\Users\\Rasmus\\Documents\Cellular Automata\\")
    howmanyframes =   len(frameslist)
    print('Frames count: '+str(howmanyframes)) #just for debugging

    for i in range(0,howmanyframes):
        print(i)
        theframe = cv2.imread('.\\frames\\'+frameslist[i])
        vvw.write(theframe)    
        """
    
if __name__ == "__main__": main()

# structure

# 1. For each cell j, play against surronding cell, calculate total payoff for cell j
# 2. For each cell, update strategies according to payoffs in surrounding cells
