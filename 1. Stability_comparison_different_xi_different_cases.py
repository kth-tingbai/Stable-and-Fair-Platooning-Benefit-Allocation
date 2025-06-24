# -*- coding: utf-8 -*-
"""
Created on Tue May 6 17:06:32 2025

The code is used to validate the stable payoff allocation approach proposed in Theorem 1.

(Code to compute the stable payoff vector for any platoon formed by electric and fuel-powered trucks)

1. Given the number of ETs and FPTs, compute the upper bound of the parameter xi in Theorem 1
2. We consider 15 trucks, where the ETs vary from 1 to 14
   Test different scenarios:
     1) Change the values of epsilon_e and epsilon_f
     2) Change the value of xi to check if the platoon keeps stable
    
@author: tingbai
"""


import copy
import numpy as np
from tqdm import tqdm
import itertools

# Parameters
epsilon_f=0.07  # unit: dollar per km 
epsilon_e=0.048
tau=300  # unit: km
param = np.linspace(0.005, 0.15, 300)  # Set the variation of xi based on the upper bound

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
lowbound_our={}  # Record the lower bound of xi in each case
Pro_stability_our={}
P_xi={}

for i in range(14):
    Comparison_s[i]=[i+1,14-i]
    Pro_stability_our[i]={}
    upbound_our[i]={}
    lowbound_our[i]={}
    P_xi[i]={}
    Payoff_our[i]={}

# Main loop for comparison
for i in tqdm(Comparison_s.keys(), desc="Processing", unit="Comparison", ncols=100):
    N_e=Comparison_s[i][0]  # Number of electric trucks
    N_f=Comparison_s[i][1]  # Number of fuel-powered trucks
    N=N_f+N_e  # Set total number of vehicles
    N_set_f={v: {} for v in range(N_f)}  # Set of fuel-powered trucks
    N_set_e={v: {} for v in range(N_f, N_f+N_e)}  # Set of electric trucks
    N_set={**N_set_f, **N_set_e}  # Combine the sets of both vehicle types

    # 1. Compute the lower bound for xi
    if N_e!=0:
        xi_lowbound=epsilon_e/(epsilon_f*N_f+epsilon_e*N_e)
    else:
        xi_lowbound=1/(N_e+N_f)
    lowbound_our[i]=xi_lowbound
        

    # 2. Compute the upper bound for xi
    if N_e != 0:
        xi_upbound=epsilon_e/(epsilon_e*(N_e-1)+epsilon_f*N_f)
    else:
        xi_upbound=epsilon_f/(epsilon_f*(N_f-1)+epsilon_e*N_e)

    upbound_our[i]=xi_upbound

    # Loop through parameter values to compute payoffs and probabilities
    for j in param:
        # 3. Compute the payoff vector (our method)
        if N_e!=0:
            V_total=(epsilon_f*N_f+epsilon_e*(N_e-1))*tau
        else:
            V_total=epsilon_f*(N-1)*tau

        N_set_payoff=copy.deepcopy(N_set)
        
        # Calculate the payoff for each vehicle
        for v in N_set.keys():
            if N_e!=0:  # Leader is an electric truck
                if v==list(N_set_e.keys())[0]:
                    N_set_payoff[v]=j*V_total
                else:
                    if v in N_set_e.keys():
                        N_set_payoff[v]=(1-j)*epsilon_e*tau
                    if v in N_set_f.keys():
                        N_set_payoff[v]=(1-j)*epsilon_f*tau
            else:  # Leader is a fuel-powered truck
                if v==list(N_set_f.keys())[0]:
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
                        s_f=[] # The set of FPTs
                        s_e=[] # The set of ETs
                        x_s_sum_our=[]
                        for v in s:
                            if v in N_set_f.keys():
                                s_f.append(v)
                            if v in N_set_e.keys():
                                s_e.append(v)
                            x_s_sum_our.append(N_set_payoff[v])
                        if len(s_e)>=1:
                            v_s=(len(s_f)*epsilon_f+(len(s_e)-1)*epsilon_e)*tau
                        if len(s_e)==0:
                            v_s=(len(s_f)-1)*epsilon_f*tau
                            
                        if v_s>sum(x_s_sum_our):
                            P_num_our[s]=v_s-sum(x_s_sum_our)
                        
        # Calculate the stability probability
        Pro_our = 1-len(P_num_our.keys())/(len(S_subsets)-2) 
        Pro_stability_our[i][j]=Pro_our
        
Pro_stability_save={}
Pro_stability_save[(epsilon_f,epsilon_e)]=Pro_stability_our
# save the data
f=open('Probability_in_different_parameters_Case1','w') # the stable probability 
f.write(str(Pro_stability_save))
f.close()

f=open('Upbound_parameters_Case1','w') # the upperbound of \xi for stability
f.write(str(upbound_our))
f.close()


