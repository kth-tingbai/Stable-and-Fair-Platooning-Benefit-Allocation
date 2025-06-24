# -*- coding: utf-8 -*-
"""
Created on Fri May 16 11:48:21 2025

Code used to compute the mean relative deviation of x from the Shapley value-based payoff phi to verify Theorem 3

@author: tingbai
"""

import copy
import numpy as np
from tqdm import tqdm
import itertools

# Parameters
epsilon_f=0.72  # unit: dollar
epsilon_e=0.048
tau=300  # unit: km
param = np.linspace(0.005, 0.99, 500)  # Set the variation of \delta=epsilon_e/epsilono_f, which is between 0 and 1

# Function: Obtain all the subsets of a set
def get_all_subsets(input_set):
    subsets=[]
    input_list=list(input_set)
    for r in range(len(input_list)+1):
        subsets.extend(itertools.combinations(input_list, r))
    return subsets

# Initialize dictionaries
Comparison_s={}  # Test, in total 15 trucks
Payoff_our={}
Payoff_bound={}
Payoff_Shapley={}
D_r={}# Record the relative deviation

bound_min={} # record the minimum bound

for i in range(14):
    Comparison_s[i]=[i+1,14-i] #case 0: [N_e,N_f]
    Payoff_Shapley[i]={}
    Payoff_our[i]={}
    Payoff_bound[i]={}
    bound_min[i]={}
    D_r[i]={}
    

# Main loop for comparison
for i in tqdm(Comparison_s.keys(), desc="Processing", unit="Comparison", ncols=100):
    N_e=Comparison_s[i][0]  # Number of electric trucks
    N_f=Comparison_s[i][1]  # Number of fuel-powered trucks
    N=N_e+N_f  # Set total number of vehicles
    N_set_e={v: {} for v in range(N_e)}  # Set of ETs
    N_set_f={v: {} for v in range(N_e, N_e+N_f)}  # Set of FPTs
    N_set={**N_set_e, **N_set_f}  # Combine the sets of both vehicle types
    N_set_k={**N_set_e, **N_set_f}  # Combine the sets of both vehicle types
    
    # 2. Compute the upper bound for xi
    xi_up=epsilon_e/(epsilon_e*(N_e-1)+epsilon_f*N_f)


    # Compute the payoff vector (Shapley value)
    for v in N_set_f.keys():
        N_set[v]=(1-1/N)*epsilon_f*tau
    for v in N_set_e.keys():
        N_set[v]=((1-1/N_e)*epsilon_e+(N_f*epsilon_f)/(N*N_e))*tau
                
    Payoff_Shapley[i]=N_set
    
    

    # Loop through parameter values to compute payoffs and mean relative deviation
    for j in param: # i.e., loop \xi
        
        # Compute the payoff vector (Our method)
        if N_e!=0:
            V_total=(epsilon_f*N_f+epsilon_e*(N_e-1))*tau
        else:
            V_total=epsilon_f*(N-1)*tau

        N_set_payoff=copy.deepcopy(N_set)
        N_set_min=copy.deepcopy(N_set)
        
        # Calculate the payoff for each vehicle
        for v in N_set.keys():
            if N_e!=0:  # Leader is an electric truck
                if v==list(N_set_e.keys())[0]:
                    N_set_payoff[v]=j*V_total
                    N_set_min[v]=xi_up*V_total
                else:
                    if v in N_set_e.keys():
                        N_set_payoff[v]=(1-j)*epsilon_e*tau
                        N_set_min[v]=(1-xi_up)*epsilon_e*tau
                    if v in N_set_f.keys():
                        N_set_payoff[v]=(1-j)*epsilon_f*tau
                        N_set_min[v]=(1-j)*epsilon_f*tau
            else:  # Leader is a fuel-powered truck
                if v==list(N_set_f.keys())[0]:
                    N_set_payoff[v]=j*V_total
                    N_set_min[v]=xi_up*V_total
                else:
                    N_set_payoff[v]=(1-j)*epsilon_f*tau
                    N_set_min[v]=(1-xi_up)*epsilon_f*tau
                    
        Payoff_our[i][j]=N_set_payoff
        Payoff_bound[i][xi_up]=N_set_min
        
        
        # 4. Compute the mean relative deviation
        D_r_j=[]
        D_r_min=[]
        for v in Payoff_Shapley[i].keys():
            phi_v=Payoff_Shapley[i][v]
            x_v=Payoff_our[i][j][v]
            x_v_min=Payoff_bound[i][xi_up][v]
            D_r_j.append(abs(phi_v-x_v)/phi_v)
            D_r_min.append(abs(phi_v-x_v_min)/phi_v)
        D_r[i][j]=D_r_j
        bound_min[i][xi_up]=D_r_min
        

# save the data
f=open('Mean_relative_deviation','w') # the mean relative deviation of different \xi
f.write(str(D_r))
f.close()

f=open('Minimum_D','w') # the stable probability 
f.write(str(bound_min))
f.close()
