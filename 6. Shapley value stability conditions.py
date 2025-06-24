# -*- coding: utf-8 -*-
"""
Created on Tue May 13 12:00:54 2025

Code used to verify Theorem 2, i.e., the sufficient condition to ensure core stability of the Shapley value-based 
payoff allocation


@author: tingbai
"""
  
import numpy as np
from tqdm import tqdm
import itertools

# Parameters
epsilon_f=0.07  # unit: euro per km per FPT follower
#epsilon_e=0.048
tau=300  # unit: km
param = np.linspace(0.005, 0.99, 400)  # Set the variation of \delta=epsilon_e/epsilono_f, which is between 0 and 1

# Function: Obtain all the subsets of a set
def get_all_subsets(input_set):
    subsets=[]
    input_list=list(input_set)
    for r in range(len(input_list)+1):
        subsets.extend(itertools.combinations(input_list, r))
    return subsets

# Initialize dictionaries
Comparison_s={}  # Test, in total 15 trucks
Payoff_Shapley={}
Pro_stability_Shapley={}
P_bound_stability={}# Record the probability of epsilon_e/epsilon_f
Payoff_Shapley_k={}

bound_stability={}
for i in range(14):
    bound_stability[i]=(14-i)/15


for i in range(14):
    Comparison_s[i]=[i+1,14-i] #case 0: [N_e,N_f]
    Pro_stability_Shapley[i]={}
    P_bound_stability[i]={}
    Payoff_Shapley[i]={}
    Payoff_Shapley_k[i]={}

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
    # Loop through parameter values to compute payoffs and probabilities
    for j in param:
        
        # Compute the payoff vector (Shapley value)
        for v in N_set_f.keys():
            N_set[v]=(1-1/N)*epsilon_f*tau
        for v in N_set_e.keys():
            N_set[v]=((1-1/N_e)*epsilon_f*j+(N_f*epsilon_f)/(N*N_e))*tau
                    
        Payoff_Shapley[i][j]=N_set
        
        # 4. Compute the stability probability
        S_subsets=get_all_subsets({i for i in N_set.keys()})
        P_num_Shapley={} # Proposed method
        for s in S_subsets:
            if s:
                if len(s)!=N: # excluding the grand coalition \mathcal{N}
                    if len(s)==1:
                        v_s=0 # there is only one truck, the platoon benefit is 0
                        if v_s>N_set[s[0]]:
                            P_num_Shapley[s]=v_s-N_set[s[0]]
                    else:
                        s_f=[] # The set of FPTs
                        s_e=[] # The set of ETs
                        x_s_sum_Shapley=[]
                        for v in s:
                            if v in N_set_e.keys():
                                s_e.append(v)
                            if v in N_set_f.keys():
                                s_f.append(v)
                            x_s_sum_Shapley.append(N_set[v])
                        if len(s_e)>=1:
                            v_s=(len(s_f)*epsilon_f+(len(s_e)-1)*epsilon_f*j)*tau
                        if len(s_e)==0:
                            v_s=(len(s_f)-1)*epsilon_f*tau
                            
                        if v_s>sum(x_s_sum_Shapley):
                            P_num_Shapley[s]=v_s-sum(x_s_sum_Shapley)
                        
        # Calculate the stability probability
        Pro_Shapley = 1-len(P_num_Shapley.keys())/(len(S_subsets)-2) 
        Pro_stability_Shapley[i][j]=Pro_Shapley
        
    k=bound_stability[i]
    # Compute the payoff vector (Shapley value)
    for v in N_set_f.keys():
        N_set_k[v]=(1-1/N)*epsilon_f*tau
    for v in N_set_e.keys():
        N_set_k[v]=((1-1/N_e)*epsilon_f*k+(N_f*epsilon_f)/(N*N_e))*tau
                
    Payoff_Shapley_k[i][k]=N_set_k
    
    # 4. Compute the stability probability
    S_subsets_k=get_all_subsets({i for i in N_set_k.keys()})
    P_num_Shapley_k={} # Proposed method
    for s in S_subsets_k:
        if s:
            if len(s)!=N: # excluding the grand coalition \mathcal{N}
                if len(s)==1:
                    v_s=0 # there is only one truck, the platoon benefit is 0
                    if v_s>N_set_k[s[0]]:
                        P_num_Shapley_k[s]=v_s-N_set_k[s[0]]
                else:
                    s_f=[] # The set of FPTs
                    s_e=[] # The set of ETs
                    x_s_sum_Shapley_k=[]
                    for v in s:
                        if v in N_set_e.keys():
                            s_e.append(v)
                        if v in N_set_f.keys():
                            s_f.append(v)
                        x_s_sum_Shapley_k.append(N_set_k[v])
                    if len(s_e)>=1:
                        v_s=(len(s_f)*epsilon_f+(len(s_e)-1)*epsilon_f*k)*tau
                    if len(s_e)==0:
                        v_s=(len(s_f)-1)*epsilon_f*tau
                        
                    if v_s>sum(x_s_sum_Shapley):
                        P_num_Shapley[s]=v_s-sum(x_s_sum_Shapley)
                    
    # Calculate the stability probability
    Pro_Shapley_k = 1-len(P_num_Shapley_k.keys())/(len(S_subsets_k)-2) 
    P_bound_stability[i][k]=Pro_Shapley_k
        

# save the data
f=open('Stability_Probability_Shapley_value','w') 
f.write(str(Pro_stability_Shapley))
f.close()

f=open('Probability_Stability_Shapley_value','w') 
f.write(str(P_bound_stability))
f.close()

f=open('Stability_bound_Shapley_value','w') 
f.write(str(bound_stability))
f.close()



    
        