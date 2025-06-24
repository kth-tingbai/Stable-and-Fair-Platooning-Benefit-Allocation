# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:10:37 2025

Verify the special case of Theorem 1, i.e., homogeneous truck platooning

Code to compute the stability probability in homogeneous truck platoon 

Given the number of ETs and FPTs, compute the upperbound of the parameter xi in Theorem 1
We consider 15 trucks, where the ETs vary from 1 to 14

Test particular scenario where all trucks are fuel-powered trucks or electric trucks:
       1) Change the values of N
       2) Change the value of xi to check if the platoon keeps stable if xi<=1/N-1

@author: tingbai
"""

import copy
import numpy as np
from tqdm import tqdm
import itertools

# Parameters
epsilon_f=0.07  # unit: dollar
tau=300  # unit: km
param = np.linspace(0.005, 1, 500)  # Set the variation of xi based on the upper bound

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
upbound_our={}  # Record the upper bound of xi in each case
Pro_stability_our={}
P_xi={}

for i in range(14):
    Comparison_s[i]=[i+2] # represent the number of total trucks
    Pro_stability_our[i]={}
    upbound_our[i]={}
    P_xi[i]={}
    Payoff_our[i]={} # record the payoff of each truck 

# Main loop for comparison
for i in tqdm(Comparison_s.keys(), desc="Processing", unit="Comparison", ncols=100):
    N=Comparison_s[i][0]  # the number of trucks in total
    N_set={v: {} for v in range(N)}  # Set of trucks
    
    # 1. Compute the lower bound for xi
    xi_lowbound=1/N
    
    # 2. Compute the upper bound for xi
    xi_upbound=1/(N-1)
    upbound_our[i]=xi_upbound
    
    V_total=(N-1)*epsilon_f*tau
    
    for j in param: # xi
    
        N_set_payoff=copy.deepcopy(N_set)
        # 3. Calculate the payoff for each vehicle
        for v in N_set.keys():
            if v==0:
                # leader
                N_set_payoff[v]=j*V_total
            else:
                N_set_payoff[v]=(1-j)*epsilon_f*tau
        
        Payoff_our[i][j]=N_set_payoff 
        # 4. Compute the stability probability
        S_subsets=get_all_subsets({i for i in N_set.keys()})
        P_num_our={} # Proposed method
        for s in S_subsets:
            if s:
                if len(s)!=N: # excluding the grand coalition \mathcal{N}
                    if len(s)==1:
                        v_s=0 # there is only one truck, the platoon benefit is 0
                        if v_s>N_set_payoff[s[0]]:
                            P_num_our[s]=v_s-N_set_payoff[s[0]]
                    else:
                        x_s_sum_our=[]
                        for v in s:
                            x_s_sum_our.append(N_set_payoff[v])
                        v_s=(len(s)-1)*epsilon_f*tau # The value of the set
                        if v_s>sum(x_s_sum_our):
                            P_num_our[s]=v_s-sum(x_s_sum_our)
                        
                        
        # Calculate the stability probability
        Pro_our = 1-len(P_num_our.keys())/(len(S_subsets)-2) 
        Pro_stability_our[i][j]=Pro_our
        
Pro_stability_save={}
Pro_stability_save[(epsilon_f)]=Pro_stability_our
# save the data
f=open('Probability_homogeneous','w') # the stable probability 
f.write(str(Pro_stability_save))
f.close()

f=open('Upbound_homogeneous','w') # the upperbound of \xi for stability
f.write(str(upbound_our))
f.close()
