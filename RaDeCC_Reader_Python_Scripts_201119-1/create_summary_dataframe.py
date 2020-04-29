#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd



def create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable):
    
    
    summary_df = log_df
    
    xs224_list = []
    xs223_list = []
    ra228_list = []
    th228_list = []
    ac227_list = []
    
    for index, row in summary_df.iterrows():
        print (row[sample_variable])
        
#        print (set(np.array(lvl2_main_df[lvl2_main_df[sub_sample_variable]==row[sub_sample_variable]]['Read_Number'])))
        read_number_set = set(lvl2_main_df[lvl2_main_df[sub_sample_variable]==row[sub_sample_variable]]['read_number'])

###########################################################################################################################################
#       224xs calculations      
        
        if 1 in read_number_set and 3 in read_number_set:
            xs224_list.append('224xs is go')
        elif 1 in read_number_set and 4 in read_number_set:
            xs224_list.append('(224xs) using read 4 instead of 3')
        else:
            xs224_list.append('(224xs) Required reads not available')
        
###########################################################################################################################################
###########################################################################################################################################
#       223xs calculations      
        
        if 2 in read_number_set and 4 in read_number_set:
            xs223_list.append('223xs is go')
        elif 1 in read_number_set and 4 in read_number_set:
            xs223_list.append('(223xs) using read 1 instead of 2')
        else:
            xs223_list.append('(223xs) Required reads not available')
        
###########################################################################################################################################
###########################################################################################################################################
#       228Ra calculations      
        
        if 4 in read_number_set and 5 in read_number_set:
            ra228_list.append('228Ra is go')
        
        else:
            ra228_list.append('(228Ra) Required reads not available')
        
###########################################################################################################################################
        print ('\n')
        
    summary_df['224xs'] = xs224_list
    summary_df['223xs'] = xs223_list
    summary_df['228Ra'] = ra228_list
    
    
#    df =  lvl2_main_df
#    set_of_samples_or_sub_samples = list(set(df[sample_variable]+'/'+df[sub_sample_variable]))
##    print (set_of_samples_or_sub_samples)
#    df_seed = []
#    
#    for subsample in set_of_samples_or_sub_samples:
#        subsample.split('/')
#        df_seed.append(subsample.split('/'))
#    
#    summary_df = pd.DataFrame(df_seed, columns = [sample_variable ,sub_sample_variable])
#    
#    
#    for summary_index, summary_row in summary_df.iterrows():
#        row_list = []
#        for main_index, main_row in df.iterrows():
#            
#            if main_row[sample_variable] == summary_row[sample_variable] and main_row[sub_sample_variable] == summary_row[sub_sample_variable]:
##                print (main_row)
#                row_list.append(main_row)
#    
#        sample_df = pd.DataFrame(row_list)
#        
##        print(sample_df.columns)
#        print(sample_df[[sample_variable,sub_sample_variable,'read_number','sampling_to_read_time_(days)']])
        
    
    
    
    
    return(summary_df)

print (create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable))