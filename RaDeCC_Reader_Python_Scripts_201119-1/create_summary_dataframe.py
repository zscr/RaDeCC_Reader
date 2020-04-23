#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd



def create_summary_dataframe(lvl2_main_df, sample_variable, sub_sample_variable):
    
    df =  lvl2_main_df
    set_of_samples_or_sub_samples = list(set(df[sample_variable]+'/'+df[sub_sample_variable]))
    print (set_of_samples_or_sub_samples)
    df_seed = []
    
    for subsample in set_of_samples_or_sub_samples:
        subsample.split('/')
        df_seed.append(subsample.split('/'))
    
    summary_df = pd.DataFrame(df_seed, columns = [sample_variable ,sub_sample_variable])
    
    
    
    
    return(summary_df)

print (create_summary_dataframe(lvl2_main_df, sample_variable, sub_sample_variable))