#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd
import numpy as np
import copy
from xs_calculator import xs_calculator



def create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable):
    
    half_life223 = 11.43 #days
    half_life224 = 3.65 #days
    ra223_lambda_days = (np.log(2)/(half_life223))
    ra224_lambda_days = (np.log(2)/(half_life224))
    
    summary_df = copy.deepcopy(log_df)
    
    xs224_list = []
    xs224_err_list = []
    xs223_list = []
    xs223_err_list = []
    xs224_t0_list = []
    xs223_t0_list = []
    ra228_list = []
    th228_list = []
    th228_err_list = []
    ac227_list = []
    ac227_err_list = []
    fraction_decayed_224_list = []
    fraction_decayed_223_list = []
    error_list = []
    
    
#   Index list for xs_calculator ##################################################################################################################
    xs = 0
    xs_err = 1
    fraction_decayed = 2
    xs_t0 = 3
    parent_activity = 4
    parent_activity_err = 5
    row_errors = 6
    
    error_flag = -999
    
    for index, row in summary_df.iterrows():
        row_specific_errors = []
        
        row_sample_variable = row[sample_variable]
        row_sub_sample_variable = row[sub_sample_variable]
        
#        print (row_sample_variable, row_sub_sample_variable)
       
        read_number_set = set(lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) &
                                 (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)), 'read_number'])

###########################################################################################################################################
#       224xs calculations      
###########################################################################################################################################
    
#####   Read1 - Read3    ##################################################################################################################
        
        if 1 in read_number_set and 3 in read_number_set:
            
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-224', isotope_column_string = 'vdpm224 (dpm/m^3)', isotope_column_string_err = 'vdpm224_err (dpm/m^3)', 
                   isotope_lambda_days = ra224_lambda_days, 
                   read_a = 1, read_b = 3, 
                   read_number_set = read_number_set)
            
            xs224_list.append(xs_calc_results[xs])
            xs224_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_224_list.append(xs_calc_results[fraction_decayed])
            xs224_t0_list.append(xs_calc_results[xs_t0])
            th228_list.append(xs_calc_results[parent_activity])
            th228_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])

                
#####   Read1 - Read4    ##################################################################################################################  
        elif 1 in read_number_set and 4 in read_number_set:
            row_specific_errors.append('(224xs, 228Th) using read 4 instead of 3')
            
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-224', isotope_column_string = 'vdpm224 (dpm/m^3)', isotope_column_string_err = 'vdpm224_err (dpm/m^3)', 
                   isotope_lambda_days = ra224_lambda_days, 
                   read_a = 1, read_b = 4, 
                   read_number_set = read_number_set)
           
            xs224_list.append(xs_calc_results[xs])
            xs224_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_224_list.append(xs_calc_results[fraction_decayed])
            xs224_t0_list.append(xs_calc_results[xs_t0])
            th228_list.append(xs_calc_results[parent_activity])
            th228_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])

#####   Reads missing      ##################################################################################################################       
        else:
            row_specific_errors.append('(224xs, 228Th) Required reads not available')
            xs224_list.append(error_flag)
            xs224_err_list.append(error_flag)
            xs224_t0_list.append(error_flag)
            th228_list.append(error_flag)
            th228_err_list.append(error_flag)
            fraction_decayed_224_list.append(error_flag)
            
        

###########################################################################################################################################
#       223xs calculations      
###########################################################################################################################################

#####   Read2 - Read4   ##################################################################################################################    
        if 2 in read_number_set and 4 in read_number_set:
            
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-223', isotope_column_string = 'vdpm223 (dpm/m^3)', isotope_column_string_err = 'vdpm223_err (dpm/m^3)', 
                   isotope_lambda_days = ra223_lambda_days, 
                   read_a = 2, read_b = 4, 
                   read_number_set = read_number_set)
            
            xs223_list.append(xs_calc_results[xs])
            xs223_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_223_list.append(xs_calc_results[fraction_decayed])
            xs223_t0_list.append(xs_calc_results[xs_t0])
            ac227_list.append(xs_calc_results[parent_activity])
            ac227_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])
            

        
#####   Read1 - Read4      #################################################################################################################
        elif 1 in read_number_set and 4 in read_number_set:
#            xs223_t0_list.append('(223xs) using read 1 instead of 2')
            row_specific_errors.append('(223xs) using read 1 instead of 2')
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-223', isotope_column_string = 'vdpm223 (dpm/m^3)', isotope_column_string_err = 'vdpm223_err (dpm/m^3)', 
                   isotope_lambda_days = ra223_lambda_days, 
                   read_a = 1, read_b = 4, 
                   read_number_set = read_number_set)
            
            xs223_list.append(xs_calc_results[xs])
            xs223_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_223_list.append(xs_calc_results[fraction_decayed])
            xs223_t0_list.append(xs_calc_results[xs_t0])
            ac227_list.append(xs_calc_results[parent_activity])
            ac227_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])
            


#####   Reads missing       ##################################################################################################################         
        else:
            row_specific_errors.append('(223xs,227Ac) Required reads not available')
            ac227_list.append(error_flag)
            ac227_err_list.append(error_flag)
            xs223_list.append(error_flag)
            xs223_err_list.append(error_flag)
            xs223_t0_list.append(error_flag)
            fraction_decayed_223_list.append(error_flag)
        

###########################################################################################################################################
#       228Ra calculations    (under construction)  
###########################################################################################################################################
        
        if 4 in read_number_set and 5 in read_number_set:
            ra228_list.append('228Ra is go')
        
        else:
            ra228_list.append('(228Ra) Required reads not available')
        
###########################################################################################################################################
        error_list.append(row_specific_errors)
    
    
    
    
    summary_df['224xs'] = xs224_list    
    summary_df['224xs_err'] = xs224_err_list    
    summary_df['224xs_t0'] = xs224_t0_list
    summary_df['Fraction_of_original_224_remaining'] = fraction_decayed_224_list
    summary_df['228Th'] = th228_list
    summary_df['228Th_err'] = th228_err_list
    summary_df['223xs'] = xs223_list    
    summary_df['223xs_t0'] = xs223_t0_list
    summary_df['Fraction_of_original_223_remaining'] = fraction_decayed_223_list
#    summary_df['223xs_t0'] = summary_df['223xs']/summary_df['Fraction_of_original_223_remaining']
    summary_df['227Ac'] = ac227_list
    summary_df['227Ac_err'] = ac227_err_list
    summary_df['228Ra'] = ra228_list
    summary_df['error_list'] = error_list
    
    cols = list(log_df.columns) + ['224xs','224xs_err', '224xs_t0',	'Fraction_of_original_224_remaining', '228Th',	 '228Th_err', 
                                   '223xs','223xs_t0', 'Fraction_of_original_223_remaining', '227Ac',	'227Ac_err', 
                                   '228Ra', 'error_list' ]
    summary_df = summary_df[cols]
    
    summary_df.to_csv('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Example_Output_Folder/Dataframes/summary_df_testing.csv')
    
    
    return(summary_df)

print (create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable))