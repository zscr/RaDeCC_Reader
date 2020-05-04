#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd
import numpy as np
import copy



def create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable):
    
    half_life223 = 11.43 #days
    half_life224 = 3.65 #days
    ra223_lambda_days = (np.log(2)/(half_life223))
    ra224_lambda_days = (np.log(2)/(half_life224))
    
    summary_df = copy.deepcopy(log_df)
    
    xs224_list = []
    xs223_list = []
    ra228_list = []
    th228_list = []
    th228_err_list = []
    ac227_list = []
    ac227_err_list = []
    fraction_decayed_224_list = []
    fraction_decayed_223_list = []
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
            read1_vdpm224_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm224_err (dpm/m^3)']
            read1_days_since_sampling = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'sampling_to_read_time_(days)']
            
            
            read3_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==3))
                    , 'vdpm224 (dpm/m^3)']
            read3_vdpm224_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==3))
                    , 'vdpm224_err (dpm/m^3)']


            if len(read1_vdpm224)>1 and len(read3_vdpm224)<1:
                row_specific_errors.append('(224xs) multiple_1st_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs224_t0_list = []
                for i in range(len(read1_vdpm224)):
                    fraction_decayed_since_sampling = np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs224_t0_list.append((read1_vdpm224.iloc[i]-read3_vdpm224.iloc[0])/fraction_decayed_since_sampling)
                xs224_list.append(np.average(sample_xs224_t0_list))
                th228_list.append(read3_vdpm224.iloc[0])
                th228_err_list.append(read3_vdpm224_err.iloc[0])
                
            if len(read1_vdpm224)<1 and len(read3_vdpm224)>1:
                row_specific_errors.append('(224xs, 228Th) multiple_3rd_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[0]))
                xs224_list.append((read1_vdpm224.iloc[0]-np.average(read3_vdpm224))/fraction_decayed_224_list[-1])
                th228_list.append(np.average(read3_vdpm224))
                th228_err_list.append(np.average(read3_vdpm224_err))
                
                
            if len(read1_vdpm224)>1 and len(read3_vdpm224)>1:
                row_specific_errors.append('(224xs, 228Th) multiple_1st_and_3rd_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs224_t0_list = []
                for i in range(len(read1_vdpm224)):
                    fraction_decayed_since_sampling = np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs224_t0_list.append((read1_vdpm224.iloc[i]-np.average(read3_vdpm224))/fraction_decayed_since_sampling)
                xs224_list.append(np.average(sample_xs224_t0_list))
                th228_list.append(np.average(read3_vdpm224))
                th228_err_list.append(np.average(read3_vdpm224_err))
                
            else:
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[0]))
                xs224_list.append((read1_vdpm224.iloc[0]-read3_vdpm224.iloc[0])/fraction_decayed_224_list[-1])
                th228_list.append(read3_vdpm224.iloc[0])
                th228_err_list.append(read3_vdpm224_err.iloc[0])
                
            
                
#####   Read1 - Read4      
        elif 1 in read_number_set and 4 in read_number_set:
            row_specific_errors.append('(224xs, 228Th) using read 4 instead of 3')
            
            read1_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm224 (dpm/m^3)']
            read1_vdpm224_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm224_err (dpm/m^3)']
            read1_days_since_sampling = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'sampling_to_read_time_(days)']
            
            read4_vdpm224 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm224 (dpm/m^3)']
            read4_vdpm224_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm224_err (dpm/m^3)']
            
            if len(read1_vdpm224)>1 and len(read4_vdpm224)<1:
                row_specific_errors.append('(224xs) multiple_1st_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs224_t0_list = []
                for i in range(len(read1_vdpm224)):
                    fraction_decayed_since_sampling = np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs224_t0_list.append((read1_vdpm224.iloc[i]-read4_vdpm224.iloc[0])/fraction_decayed_since_sampling)
                xs224_list.append(np.average(sample_xs224_t0_list))
                th228_list.append(read4_vdpm224.iloc[0])
                th228_err_list.append(read4_vdpm224.iloc[0])
                
            if len(read1_vdpm224)<1 and len(read4_vdpm224)>1:
                row_specific_errors.append('(224xs, 228Th) multiple_4th_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[0]))
                xs224_list.append((read1_vdpm224.iloc[0]-np.average(read4_vdpm224))/fraction_decayed_224_list[-1])
                th228_list.append(np.average(read4_vdpm224))
                th228_err_list.append(np.average(read4_vdpm224_err))
                
            if len(read1_vdpm224)>1 and len(read4_vdpm224)>1:
                row_specific_errors.append('(224xs, 228Th) multiple_1st_and_4th_reads_averaged')
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs224_t0_list = []
                for i in range(len(read1_vdpm224)):
                    fraction_decayed_since_sampling = np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs224_t0_list.append((read1_vdpm224.iloc[i]-np.average(read4_vdpm224))/fraction_decayed_since_sampling)
                xs224_list.append(np.average(sample_xs224_t0_list))
                th228_list.append(np.average(read4_vdpm224))
                th228_err_list.append(np.average(read4_vdpm224_err))
                
            else:
                fraction_decayed_224_list.append(np.exp(-ra224_lambda_days*read1_days_since_sampling.iloc[0]))
                xs224_list.append((read1_vdpm224.iloc[0]-read4_vdpm224.iloc[0])/fraction_decayed_224_list[-1])
                th228_list.append(read4_vdpm224.iloc[0])
                th228_err_list.append(read4_vdpm224_err.iloc[0])
#####   Reads missing             
        else:
            row_specific_errors.append('(224xs, 228Th) Required reads not available')
            xs224_list.append(-999)
            th228_list.append(-999)
            th228_err_list.append(-999)
            fraction_decayed_224_list.append(-999)
            
        
###########################################################################################################################################
###########################################################################################################################################
#       223xs calculations      

#####   Read2 - Read4       
        if 2 in read_number_set and 4 in read_number_set:
            
            read2_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==2))
                    , 'vdpm223 (dpm/m^3)']
            read2_vdpm223_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==2))
                    , 'vdpm223_err (dpm/m^3)']
            read2_days_since_sampling = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==2))
                    , 'sampling_to_read_time_(days)']
            
            read4_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223 (dpm/m^3)']
            read4_vdpm223_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223_err (dpm/m^3)']
            
            if len(read2_vdpm223)>1 and len(read4_vdpm223)<1:
                row_specific_errors.append('(223xs) multiple_2nd_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read2_days_since_sampling)))
                sample_xs223_t0_list = []
                for i in range(len(read2_vdpm223)):
                    fraction_decayed_since_sampling = np.exp(-ra223_lambda_days*read2_days_since_sampling.iloc[i])
                    sample_xs223_t0_list.append((read2_vdpm223.iloc[i]-read4_vdpm223.iloc[0])/fraction_decayed_since_sampling)
                xs223_list.append(np.average(sample_xs223_t0_list))
                ac227_list.append(read4_vdpm223.iloc[0])
                ac227_err_list.append(read4_vdpm223.iloc[0])
                
            if len(read2_vdpm223)<1 and len(read4_vdpm223)>1:
                row_specific_errors.append('(223xs, 227Ac) multiple_4th_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read2_days_since_sampling.iloc[0]))
                xs223_list.append((read2_vdpm223.iloc[0]-np.average(read4_vdpm223))/fraction_decayed_223_list[-1])
                ac227_list.append(np.average(read4_vdpm223))
                ac227_err_list.append(np.average(read4_vdpm223_err))
                
            if len(read2_vdpm223)>1 and len(read4_vdpm223)>1:
                row_specific_errors.append('(223xs, 227Ac) multiple_2nd_and_4th_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read2_days_since_sampling)))
                sample_xs223_t0_list = []
                for i in range(len(read2_vdpm223)):
                    fraction_decayed_since_sampling = np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs223_t0_list.append((read2_vdpm223.iloc[i]-np.average(read4_vdpm223))/fraction_decayed_since_sampling)
                xs223_list.append(np.average(sample_xs223_t0_list))
                ac227_list.append(np.average(read4_vdpm223))
                ac227_err_list.append(np.average(read4_vdpm223_err))
                
            else:
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read2_days_since_sampling.iloc[0]))
                xs223_list.append((read2_vdpm223.iloc[0]-read4_vdpm223.iloc[0])/fraction_decayed_223_list[-1])
                ac227_list.append(read4_vdpm223.iloc[0])
                ac227_err_list.append(read4_vdpm223_err.iloc[0])
                
                
                
                
                
                
#                
#                
#            if len(read2_vdpm223)<1 and len(read4_vdpm223)>1:
#                row_specific_errors.append('(xs223, 227Ac) multiple_4th_reads_averaged')
#                xs223_list.append(read2_vdpm223.iloc[0]-np.average(read4_vdpm223))
#                ac227_list.append(np.average(read4_vdpm223))
#                ac227_err_list.append(np.average(read4_vdpm223_err))
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read2_days_since_sampling.iloc[0]))
#                
#            if len(read2_vdpm223)>1 and len(read4_vdpm223)<1:
#                row_specific_errors.append('(xs223) multiple_2nd_reads_averaged')
#                xs223_list.append(np.average(read2_vdpm223)-read4_vdpm223.iloc[0])
#                ac227_list.append(read4_vdpm223.iloc[0])
#                ac227_err_list.append(read4_vdpm223_err.iloc[0])
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
#                
#            if len(read2_vdpm223)>1 and len(read4_vdpm223)>1:
#                row_specific_errors.append('(xs223, 227Ac) multiple_2nd_and_4th_reads_averaged')
#                xs223_list.append(np.average(read2_vdpm223)-np.average(read4_vdpm223))
#                ac227_list.append(np.average(read4_vdpm223))
#                ac227_err_list.append(np.average(read4_vdpm223_err))
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
#                
#            else:
#                xs223_list.append(read2_vdpm223.iloc[0]-read4_vdpm223.iloc[0])
#                ac227_list.append(read4_vdpm223.iloc[0])
#                ac227_err_list.append(read4_vdpm223_err.iloc[0])
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read2_days_since_sampling.iloc[0]))
#        
#        
        
#####   Read1 - Read4        
        elif 1 in read_number_set and 4 in read_number_set:
#            xs223_list.append('(223xs) using read 1 instead of 2')
            row_specific_errors.append('(223xs) using read 1 instead of 2')
            
            read1_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm223 (dpm/m^3)']
            read1_vdpm223_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'vdpm223_err (dpm/m^3)']
            read1_days_since_sampling = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==1))
                    , 'sampling_to_read_time_(days)']
            
            read4_vdpm223 = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223 (dpm/m^3)']
            read4_vdpm223_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm223_err (dpm/m^3)']
            
            if len(read1_vdpm223)>1 and len(read4_vdpm223)<1:
                row_specific_errors.append('(223xs) multiple_1st_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs223_t0_list = []
                for i in range(len(read1_vdpm223)):
                    fraction_decayed_since_sampling = np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs223_t0_list.append((read1_vdpm223.iloc[i]-read4_vdpm223.iloc[0])/fraction_decayed_since_sampling)
                xs223_list.append(np.average(sample_xs223_t0_list))
                ac227_list.append(read4_vdpm223.iloc[0])
                ac227_err_list.append(read4_vdpm223.iloc[0])
                
            if len(read1_vdpm223)<1 and len(read4_vdpm223)>1:
                row_specific_errors.append('(223xs, 227Ac) multiple_4th_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[0]))
                xs223_list.append((read1_vdpm223.iloc[0]-np.average(read4_vdpm223))/fraction_decayed_223_list[-1])
                ac227_list.append(np.average(read4_vdpm223))
                ac227_err_list.append(np.average(read4_vdpm223_err))
                
            if len(read1_vdpm223)>1 and len(read4_vdpm223)>1:
                row_specific_errors.append('(223xs, 227Ac) multiple_1st_and_4th_reads_averaged')
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
                sample_xs223_t0_list = []
                for i in range(len(read1_vdpm223)):
                    fraction_decayed_since_sampling = np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[i])
                    sample_xs223_t0_list.append((read1_vdpm223.iloc[i]-np.average(read4_vdpm223))/fraction_decayed_since_sampling)
                xs223_list.append(np.average(sample_xs223_t0_list))
                ac227_list.append(np.average(read4_vdpm223))
                ac227_err_list.append(np.average(read4_vdpm223_err))
                
            else:
                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[0]))
                xs223_list.append((read1_vdpm223.iloc[0]-read4_vdpm223.iloc[0])/fraction_decayed_223_list[-1])
                ac227_list.append(read4_vdpm223.iloc[0])
                ac227_err_list.append(read4_vdpm223_err.iloc[0])
                
#                
#                
#
#            if len(read1_vdpm223)<1 and len(read4_vdpm223)>1:
#                row_specific_errors.append('(xs223, 227Ac) multiple_4th_reads_averaged')
#                xs223_list.append(read1_vdpm223.iloc[0]-np.average(read4_vdpm223))
#                ac227_list.append(np.average(read4_vdpm223))
#                ac227_err_list.append(np.average(read4_vdpm223_err))
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[0]))
#                
#            if len(read1_vdpm223)>1 and len(read4_vdpm223)<1:
#                row_specific_errors.append('(xs223) multiple_1st_reads_averaged')
#                xs223_list.append(np.average(read1_vdpm223)-read4_vdpm223.iloc[0])
#                ac227_list.append(read4_vdpm223.iloc[0])
#                ac227_err_list.append(read4_vdpm223_err.iloc[0])
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
#                
#            if len(read1_vdpm223)>1 and len(read4_vdpm223)>1:
#                row_specific_errors.append('(xs223, 227Ac) multiple_1st_and_4th_reads_averaged')
#                xs223_list.append(np.average(read1_vdpm223)-np.average(read4_vdpm223))
#                ac227_list.append(np.average(read4_vdpm223))
#                ac227_err_list.append(np.average(read4_vdpm223_err))
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*np.average(read1_days_since_sampling)))
#                
#            else:
#                xs223_list.append(read1_vdpm223.iloc[0]-read4_vdpm223.iloc[0])
#                ac227_list.append(read4_vdpm223.iloc[0])
#                ac227_err_list.append(read4_vdpm223_err.iloc[0])
#                fraction_decayed_223_list.append(np.exp(-ra223_lambda_days*read1_days_since_sampling.iloc[0]))

#####   Reads missing                
        else:
            row_specific_errors.append('(223xs,227Ac) Required reads not available')
            ac227_list.append(-999)
            ac227_err_list.append(-999)
            xs223_list.append(-999)
            fraction_decayed_223_list.append(-999)
        
###########################################################################################################################################
###########################################################################################################################################
#       228Ra calculations    (under construction)  
        
        if 4 in read_number_set and 5 in read_number_set:
            ra228_list.append('228Ra is go')
        
        else:
            ra228_list.append('(228Ra) Required reads not available')
        
###########################################################################################################################################
        error_list.append(row_specific_errors)
        
    summary_df['224xs_t0'] = xs224_list
    summary_df['Fraction_of_original_224_remaining'] = fraction_decayed_224_list
#    summary_df['224xs_t0'] = summary_df['224xs']/summary_df['Fraction_of_original_224_remaining']
    summary_df['228Th'] = th228_list
    summary_df['228Th_err'] = th228_err_list
    summary_df['223xs_t0'] = xs223_list
    summary_df['Fraction_of_original_223_remaining'] = fraction_decayed_223_list
#    summary_df['223xs_t0'] = summary_df['223xs']/summary_df['Fraction_of_original_223_remaining']
    summary_df['227Ac'] = ac227_list
    summary_df['227Ac_err'] = ac227_err_list
    summary_df['228Ra'] = ra228_list
    summary_df['error_list'] = error_list
    
    cols = list(log_df.columns) + ['224xs_t0',	'Fraction_of_original_224_remaining', '228Th',	 '228Th_err', 
                                   '223xs_t0', 'Fraction_of_original_223_remaining', '227Ac',	'227Ac_err', 
                                   '228Ra', 'error_list' ]
    summary_df = summary_df[cols]
    
    summary_df.to_csv('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Example_Output_Folder/Dataframes/summary_df_testing.csv')
    
    
    return(summary_df)

print (create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable))