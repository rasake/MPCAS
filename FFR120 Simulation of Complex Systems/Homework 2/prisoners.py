# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:01:21 2016

@author: Rasmus
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def print_settings(reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off):
    print("Game settings:")
    print("reward_pay_off = " + str(reward_pay_off))
    print("temptation_pay_off = " + str(temptation_pay_off))
    print("sucker_pay_off = " + str(sucker_pay_off))
    print("punishment_pay_off = " + str(punishment_pay_off))

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
    



def run_cellular_automaton(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, p_mut, board_size = 32, plot = True):
    
    strategy_matrix = PeriodicMatrix(np.floor(np.random.rand(board_size, board_size)*(nbr_rounds+1)))
    if plot:
        sns.heatmap(strategy_matrix, vmin = 0, vmax = nbr_rounds)
        plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\ca_0.png", dpi = 400)
        plt.close()
    
    strategy_time_evolution = np.zeros([nbr_time_steps, nbr_rounds+1])
    for k in range(nbr_rounds+1):
        strategy_time_evolution[0,k] = np.sum(strategy_matrix == k)/board_size**2    
    for t in range(1,nbr_time_steps):
        pay_off_matrix = evaluate_strategies(strategy_matrix,nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
        strategy_matrix = update_strategies(strategy_matrix, pay_off_matrix, nbr_rounds, p_mut)
        if plot:
            sns.heatmap(strategy_matrix, vmin = 0, vmax = nbr_rounds)
            plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\ca_" + str(t) + ".png", dpi = 400)
            plt.close()

        for k in range(nbr_rounds+1):
            strategy_time_evolution[t,k] = np.sum(strategy_matrix == k)/board_size**2

    return strategy_time_evolution, strategy_matrix

def plot_time_evolution(strategy_time_evolution, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str = ""):    
    title_str = "Strategy time evolution for: R= " + str(reward_pay_off) 
    title_str += ", T=" + str(temptation_pay_off) + ", S=" + str(sucker_pay_off)
    title_str += ", P=" + str(punishment_pay_off)
    legend_strings = []
    sns.set_style('white')
    sns.set_palette(sns.color_palette("RdBu", n_colors=nbr_rounds+1))
    for k in range(nbr_rounds+1):
        plt.plot(strategy_time_evolution[:,k])
        legend_strings.append("S_" + str(k))
    plt.legend(legend_strings)
    plt.title(title_str)
    plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\time_evo" + file_id_str + ".png", dpi = 400)


def final_strategy_distribution(strategy_time_evolution, nbr_rounds, hindsight):
    distribution = []
    for k in range(nbr_rounds+1):
        time_average = np.mean(strategy_time_evolution[-hindsight:,k])
        distribution.append(time_average)
    return distribution

def find_regime(strategy_distribution):
    if strategy_distribution[0] + strategy_distribution[1] > 0.7:
        return 1
    if strategy_distribution[-1] + strategy_distribution[-2] > 0.7:
        return 2
    else:
        return 3


def explore_tp_space(nbr_time_steps, nbr_interior_points, hindsight):
    
    nbr_rounds = 7
    reward_pay_off = 1
    sucker_pay_off = 0
    p_mut = 1/32**2
    
    regime_map = np.zeros([nbr_interior_points, nbr_interior_points])
    temptation_pay_offs = np.linspace(1,2,nbr_interior_points)
    punishment_pay_offs = np.linspace(0,1,nbr_interior_points)
    for i, temptation_i in enumerate(temptation_pay_offs):
        for j, punishment_j in enumerate(punishment_pay_offs):
            strategy_time_evolution, strategy_matrix = run_cellular_automaton(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_i, sucker_pay_off, punishment_j, p_mut, plot=False)
            strategy_dist = final_strategy_distribution(strategy_time_evolution, nbr_rounds, hindsight)
            regime = find_regime(strategy_dist)
            regime_map[i][j] = regime       
            
    return temptation_pay_offs, punishment_pay_offs, regime_map


def generate_single_run_graphs(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, p_mut = 1/32**2, file_id_str = ""):
    
    strategy_time_evolution, strategy_matrix = run_cellular_automaton(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, p_mut, plot=False)
    sns.heatmap(strategy_matrix, vmin = 0, vmax = nbr_rounds)
    plt.savefig("C:\\Users\\Rasmus\\Documents\Cellular Automata\\ca_final" + file_id_str + ".png", dpi = 400)
    plt.show()
    plt.close()
    
    plot_time_evolution(strategy_time_evolution, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str)
    
def demonstrate_basic_model(nbr_time_steps, nbr_rounds):
    reward_pay_off = 1
    temptation_pay_off = 1.5
    sucker_pay_off = 0
    punishment_pay_off = 0.5
    id_str = "_basic_model_" + str(nbr_time_steps) + "_steps_"
    
    print_settings(reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
    
    generate_single_run_graphs(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str = id_str)

def demonstrate_regime1(nbr_time_steps, nbr_rounds):
    reward_pay_off = 1
    temptation_pay_off = 1.5
    sucker_pay_off = 0
    punishment_pay_off = 0.8
    id_str = "_regime1"
    
    print_settings(reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
    
    generate_single_run_graphs(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str = id_str)

def demonstrate_regime2(nbr_time_steps, nbr_rounds):
    reward_pay_off = 1
    temptation_pay_off = 1.5
    sucker_pay_off = 0
    punishment_pay_off = 0.1
    id_str = "_regime2"
    
    print_settings(reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)
    
    generate_single_run_graphs(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str = id_str)

def demonstrate_regime3(nbr_time_steps, nbr_rounds):
    reward_pay_off = 1
    temptation_pay_off = 1.5
    sucker_pay_off = 0
    punishment_pay_off = 0.5
    id_str = "_regime3"
    
    print_settings(reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off)

    generate_single_run_graphs(nbr_time_steps, nbr_rounds, reward_pay_off, temptation_pay_off, sucker_pay_off, punishment_pay_off, file_id_str = id_str)


def generate_regime_graph():
    nbr_time_steps = 10
    nbr_interior_points = 3
    hindsight = 2
    temptation_pay_offs, punishment_pay_offs, regime_map = explore_tp_space(nbr_time_steps, nbr_interior_points, hindsight)
    map_filpped = np.flipud(regime_map)
    punishments_reversed = punishment_pay_offs[::-1]
    sns.heatmap(map_filpped, xticklabels=temptation_pay_offs, yticklabels=punishments_reversed)
    plt.show()
