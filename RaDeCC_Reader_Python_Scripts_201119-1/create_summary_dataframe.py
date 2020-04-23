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
#    print (set_of_samples_or_sub_samples)
    df_seed = []
    
    for subsample in set_of_samples_or_sub_samples:
        subsample.split('/')
        df_seed.append(subsample.split('/'))
    
    summary_df = pd.DataFrame(df_seed, columns = [sample_variable ,sub_sample_variable])
    
    
    for summary_index, summary_row in summary_df.iterrows():
        row_list = []
        for main_index, main_row in df.iterrows():
            
            if main_row[sample_variable] == summary_row[sample_variable] and main_row[sub_sample_variable] == summary_row[sub_sample_variable]:
#                print (main_row)
                row_list.append(main_row)
    
        sample_df = pd.DataFrame(row_list)
        
    
        print(sample_df[sample_variable],sample_df['sampling_to_read_time_(days)'])
    
    
    
    
    return(summary_df)

#create_summary_dataframe(lvl2_main_df, sample_variable, sub_sample_variable)