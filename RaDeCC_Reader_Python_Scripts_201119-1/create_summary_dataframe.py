#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd
import numpy as np



def create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable):
    
    
    summary_df = log_df
    
    xs224_list = []
    xs223_list = []
    ra228_list = []
    th228_list = []
    ac227_list = []
    error_list = []
    
    for index, row in summary_df.iterrows():
        row_specific_errors = []
        
        row_sample_variable = row[sample_variable]
        row_sub_sample_variable = row[sub_sample_variable]
        
#        print (row_sample_variable, row_sub_sample_variable)
       
        read_number_set = set(lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) &
                                 (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)), 'read_number'])

###########################################################################################################################################
#       224xs calculations      

#####   Read1 - Read3    
        
        if 1 in read_number_set and 3 in read_number_set:
            
            read1_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm224 (dpm/m^3)']
            read3_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==3))
                    , 'vdpm224 (dpm/m^3)']
            
            
            if len(read1_vdpm224)>1 or len(read3_vdpm224)>1:
                row_specific_errors.append('multi_reads_averaged')
                xs224_list.append(np.average(read1_vdpm224)-np.average(read3_vdpm224))
            else:
                xs224_list.append(read1_vdpm224.iloc[0]-read3_vdpm224.iloc[0])
            
#####   Read1 - Read4      
        elif 1 in read_number_set and 4 in read_number_set:
            row_specific_errors.append('(224xs) using read 4 instead of 3')
            read4_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm224 (dpm/m^3)']
            
            if len(read1_vdpm224)>1 or len(read4_vdpm224)>1:
                row_specific_errors.append('(xs224) multi_reads_averaged')
                xs224_list.append(np.average(read1_vdpm224)-np.average(read4_vdpm224))
            else:
                xs224_list.append(read1_vdpm224.iloc[0]-read4_vdpm224.iloc[0])
            
#####   Reads missing             
        else:
            xs224_list.append('(224xs) Required reads not available')
        
###########################################################################################################################################
###########################################################################################################################################
#       223xs calculations      

#####   Read2 - Read4       
        if 2 in read_number_set and 4 in read_number_set:
            
            read2_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==2))
                    , 'vdpm223 (dpm/m^3)']
            read4_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223 (dpm/m^3)']
            
            
            if len(read2_vdpm223)>1 or len(read4_vdpm223)>1:
                row_specific_errors.append('(xs223) multi_reads_averaged')
                xs223_list.append(np.average(read2_vdpm223)-np.average(read4_vdpm223))
            else:
                xs223_list.append(read2_vdpm223.iloc[0]-read4_vdpm223.iloc[0])
        
        
        
        
#####   Read1 - Read4        
        elif 1 in read_number_set and 4 in read_number_set:
#            xs223_list.append('(223xs) using read 1 instead of 2')
            row_specific_errors.append('(223xs) using read 1 instead of 2')
            read1_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm223 (dpm/m^3)']
            read4_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223 (dpm/m^3)']
            
            if len(read1_vdpm223)>1 or len(read4_vdpm223)>1:
                row_specific_errors.append('(xs223) multi_reads_averaged')
                xs223_list.append(np.average(read1_vdpm223)-np.average(read4_vdpm223))
            else:
                xs223_list.append(read1_vdpm223.iloc[0]-read4_vdpm223.iloc[0])

#####   Reads missing                
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
        error_list.append(row_specific_errors)
        
#        print ('\n')
        
    summary_df['224xs'] = xs224_list
    summary_df['223xs'] = xs223_list
    summary_df['228Ra'] = ra228_list
    summary_df['error_list'] = error_list
    
    summary_df.to_csv('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Example_Output_Folder/Dataframes/summary_df.csv')
    
    
    return(summary_df)

#print (create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable))