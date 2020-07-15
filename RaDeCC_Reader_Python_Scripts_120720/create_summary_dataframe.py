#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:59:11 2020

@author: seanselzer
"""

import pandas as pd
import numpy as np
import copy
import time
from pathlib import Path
from xs_calculator import xs_calculator



def create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable, output_directory, linear_data_type):
    
    half_life223 = 11.43 #days
    half_life224 = 3.65 #days
    half_life_th228 = 1.9*365 #days
    half_life_ra228 = 5.7*365 #days

    ra223_lambda_days = (np.log(2)/(half_life223))
    ra224_lambda_days = (np.log(2)/(half_life224))
    th228_lambda_days = (np.log(2)/(half_life_th228))
    ra228_lambda_days = (np.log(2)/(half_life_ra228))
    
    summary_df = copy.deepcopy(log_df)
    if linear_data_type == True:
        None_list = ['None' for i in range (len( summary_df))]
        summary_df['subsample_dummy_column'] = None_list
    
    xs224_list = []
    xs224_err_list = []
    xs223_list = []
    xs223_err_list = []
    xs223_thstdonly_list = []
    xs223_thstdonly_err_list = []
    xs224_t0_list = []
    xs223_t0_list = []
    xs223_thstdonly_t0_list = []
    ra228_list = []
    ra228_err_list = []
    th228_list = []
    th228_err_list = []
    ac227_list = []
    ac227_err_list = []
    ac227_thstdonly_list = []
    ac227_thstdonly_err_list = []
    fraction_decayed_224_list = []
    fraction_decayed_223_list = []
    fraction_decayed_223_thstdonly_list = []
    error_list = []
    read_error_list = []
    ra226_list = []
    ra226_err_list = []
    
    
#   Index list for xs_calculator ##################################################################################################################
    xs = 0
    xs_err = 1
    fraction_decayed = 2
    xs_t0 = 3
    parent_activity = 4
    parent_activity_err = 5
    row_errors = 6
    read_errors = 7
    
    error_flag = -999
    
    for index, row in summary_df.iterrows():
        row_specific_errors = []
        read_specific_errors = {}
        
        row_sample_variable = row[sample_variable]
        if linear_data_type == False:
            row_sub_sample_variable = str(row[sub_sample_variable])
            read_number_set = set(lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) &
                                 (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)), 'read_number'])
        else:
            row_sub_sample_variable = str(row['subsample_dummy_column'])
            read_number_set = set(lvl2_main_df.loc[(lvl2_main_df[sample_variable]==row_sample_variable), 'read_number'])

        
#        print (row_sample_variable, row_sub_sample_variable)
       
        

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
            read_specific_errors.update(xs_calc_results[read_errors])

                
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
            read_specific_errors.update(xs_calc_results[read_errors])

#####   Reads missing      ##################################################################################################################       
        else:
            row_specific_errors.append('(224xs, 228Th) Required reads not available')
            read_specific_errors.update({'(224xs, 228Th)': 'Required reads not available'})
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
            read_specific_errors.update(xs_calc_results[read_errors])
            

        
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
            read_specific_errors.update(xs_calc_results[read_errors])

#####   Reads missing       ##################################################################################################################         
        else:
            row_specific_errors.append('(223xs,227Ac) Required reads not available')
            read_specific_errors.update({'(223xs,227Ac)': 'Required reads not available'})
            ac227_list.append(error_flag)
            ac227_err_list.append(error_flag)
            xs223_list.append(error_flag)
            xs223_err_list.append(error_flag)
            xs223_t0_list.append(error_flag)
            fraction_decayed_223_list.append(error_flag)


###########################################################################################################################################
#       223xs_from_thstd calculations      
###########################################################################################################################################

#####   Read2 - Read4   ##################################################################################################################    
        if 2 in read_number_set and 4 in read_number_set:
            
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-223', isotope_column_string = 'vdpm223_thstdonly (dpm/m^3)', isotope_column_string_err = 'vdpm223_thstdonly_err (dpm/m^3)', 
                   isotope_lambda_days = ra223_lambda_days, 
                   read_a = 2, read_b = 4, 
                   read_number_set = read_number_set)
            
            xs223_thstdonly_list.append(xs_calc_results[xs])
            xs223_thstdonly_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_223_thstdonly_list.append(xs_calc_results[fraction_decayed])
            xs223_thstdonly_t0_list.append(xs_calc_results[xs_t0])
            ac227_thstdonly_list.append(xs_calc_results[parent_activity])
            ac227_thstdonly_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])
            read_specific_errors.update(xs_calc_results[read_errors])
            

        
#####   Read1 - Read4      #################################################################################################################
        elif 1 in read_number_set and 4 in read_number_set:
#            xs223_t0_list.append('(223xs) using read 1 instead of 2')
            row_specific_errors.append('(223xs) using read 1 instead of 2')
            xs_calc_results = xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope = 'Ra-223', isotope_column_string = 'vdpm223_thstdonly (dpm/m^3)', isotope_column_string_err = 'vdpm223_thstdonly_err (dpm/m^3)', 
                   isotope_lambda_days = ra223_lambda_days, 
                   read_a = 1, read_b = 4, 
                   read_number_set = read_number_set)
            
            xs223_thstdonly_list.append(xs_calc_results[xs])
            xs223_thstdonly_err_list.append(xs_calc_results[xs_err])
            fraction_decayed_223_thstdonly_list.append(xs_calc_results[fraction_decayed])
            xs223_thstdonly_t0_list.append(xs_calc_results[xs_t0])
            ac227_thstdonly_list.append(xs_calc_results[parent_activity])
            ac227_thstdonly_err_list.append(xs_calc_results[parent_activity_err])
            row_specific_errors.append(xs_calc_results[row_errors])
            read_specific_errors.update(xs_calc_results[read_errors])
            
        
#####   Reads missing       ##################################################################################################################         
        else:
            row_specific_errors.append('(223xs_thstdonly,227Ac_thstdonly) Required reads not available')
            read_specific_errors.update({'(223xs_thstdonly, 227Ac_thstdonly)': 'Required reads not available'})
            ac227_thstdonly_list.append(error_flag)
            ac227_thstdonly_err_list.append(error_flag)
            xs223_thstdonly_list.append(error_flag)
            xs223_thstdonly_err_list.append(error_flag)
            xs223_thstdonly_t0_list.append(error_flag)
            fraction_decayed_223_thstdonly_list.append(error_flag)


###########################################################################################################################################
#       228Ra calculations      
###########################################################################################################################################
        
        if 4 in read_number_set and 5 in read_number_set:
            
            read4_vdpm = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm224 (dpm/m^3)']
            read4_vdpm_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'vdpm224_err (dpm/m^3)']
            read4_datetime = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'Mid_Read_Datetime']
            
            read5_vdpm = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==5))
                    , 'vdpm224 (dpm/m^3)']
            read5_vdpm_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==5))
                    , 'vdpm224_err (dpm/m^3)']
            read5_datetime = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==5))
                    , 'Mid_Read_Datetime']
            
            read4_errors = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==4))
                    , 'Error_List']
            read5_errors = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==5))
                    , 'Error_List']

            
            if len(read4_vdpm)>1 and len(read5_vdpm)==1:
                # print ('>=')
                timedelta_read4_to_read5_list = []
                time_read4_to_read5_list = []
                for i in range(len(read4_datetime)):
                    timedelta_read4_to_read5_list.append(read5_datetime.iloc[0]-read4_datetime.iloc[i])
                    time_read4_to_read5_list.append(timedelta_read4_to_read5_list[-1].days + (timedelta_read4_to_read5_list[-1].seconds/(24*60*60)))
                time_read4_to_read5 = np.average(time_read4_to_read5_list)
                # print(time_read4_to_read5)
                ra228_list.append(
                                    read5_vdpm.iloc[0] - (np.average(read4_vdpm) - np.exp(-th228_lambda_days* (time_read4_to_read5)/(1.499* (np.exp(-ra228_lambda_days*time_read4_to_read5)-np.exp(-th228_lambda_days*time_read4_to_read5)))))
                                    )
                ra228_err_list.append(
                    np.sqrt(read5_vdpm_err.iloc[0]**2 + np.average(read4_vdpm_err)**2)
                )
                row_specific_errors.append('Multiple 4th reads Averaged')
                # read_specific_errors.update(xs_calc_results[read_errors])
            
            if len(read4_vdpm)==1 and len(read5_vdpm)>1:
                # print ('=>')
                
                timedelta_read4_to_read5_list = []
                time_read4_to_read5_list = []
                for i in range(len(read5_datetime)):
                    timedelta_read4_to_read5_list.append(read5_datetime.iloc[i]-read4_datetime.iloc[0])
                    time_read4_to_read5_list.append(timedelta_read4_to_read5_list[-1].days + (timedelta_read4_to_read5_list[-1].seconds/(24*60*60)))
                time_read4_to_read5 = np.average(time_read4_to_read5_list)
                # print(time_read4_to_read5)
                ra228_list.append(
                                    np.average(read5_vdpm) - (read4_vdpm.iloc[0] - np.exp(-th228_lambda_days* (time_read4_to_read5)/(1.499* np.exp((-ra228_lambda_days*time_read4_to_read5)-(-th228_lambda_days*time_read4_to_read5)))))
                                    )
                ra228_err_list.append(
                    np.sqrt(np.average(read5_vdpm_err)**2 + read4_vdpm_err.iloc[0]**2)
                )
                row_specific_errors.append('Multiple 5th reads Averaged')
                # read_specific_errors.update(xs_calc_results[read_errors])
            
            if len(read4_vdpm)>1 and len(read5_vdpm)>1:
                # print ('>>')
                timedelta_read4_to_read5_list = []
                time_read4_to_read5_list = []
                for i in range(len(read5_datetime)):
                    for j in range(len(read4_datetime)):
                        timedelta_read4_to_read5_list.append(read5_datetime.iloc[i]-read4_datetime.iloc[j])
                        time_read4_to_read5_list.append(timedelta_read4_to_read5_list[-1].days + (timedelta_read4_to_read5_list[-1].seconds/(24*60*60)))
                
                time_read4_to_read5 = np.average(time_read4_to_read5_list)
                
                # print(time_read4_to_read5)
                ra228_list.append(
                                    np.average(read5_vdpm) - (np.average(read4_vdpm) - np.exp(-th228_lambda_days* (time_read4_to_read5)/(1.499* np.exp((-ra228_lambda_days*time_read4_to_read5)-(-th228_lambda_days*time_read4_to_read5)))))
                                    )
                
                ra228_err_list.append(
                    np.sqrt(np.average(read5_vdpm_err)**2 + np.average(read4_vdpm_err)**2)
                )
                row_specific_errors.append('Multiple 4th and 5th reads averaged')
                # read_specific_errors.update(xs_calc_results[read_errors])
            
            if len(read4_vdpm)==1 and len(read5_vdpm)==1:
                # print ('==')
                timedelta_read4_to_read5 = read5_datetime.iloc[0]-read4_datetime.iloc[0]
                time_read4_to_read5 = timedelta_read4_to_read5.days + (timedelta_read4_to_read5.seconds/(24*60*60))
                # print(time_read4_to_read5)
                ra228_list.append(
                                    read5_vdpm.iloc[0] - (read4_vdpm.iloc[0] - np.exp(-th228_lambda_days* (time_read4_to_read5)/(1.499* np.exp((-ra228_lambda_days*time_read4_to_read5)-(-th228_lambda_days*time_read4_to_read5)))))
                                    )
                ra228_err_list.append(
                    np.sqrt(read5_vdpm_err.iloc[0]**2 + read4_vdpm_err.iloc[0]**2)
                )
            ###############################################################################################################################
            # Bring Diego-Feliu Errors through from results dataframe to summary dataframe.
            ###############################################################################################################################
            read_specific_errors.update({'Read4' : list(read4_errors.iloc[0].keys()),'Read5' :list(read5_errors.iloc[0].keys())})

                
        else:
            ra228_list.append('(228Ra) Required reads not available')
            ra228_err_list.append('(228Ra) Required reads not available')
            # read_specific_errors.update({'(228Ra)': 'Required reads not available'})
        
###########################################################################################################################################
        
    
###########################################################################################################################################
#       226Ra calculations      
###########################################################################################################################################
        ra226_row_list = list(lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) &
                                 (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)), 'vdpm226 (dpm/m^3)'])
        ra226_err_row_list = list(lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) &
                                 (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)), 'vdpm226_err (dpm/m^3)'])
        
        upper_limit_226_err = np.average(ra226_err_row_list)+np.std(ra226_err_row_list)
        lower_limit_226_err = np.average(ra226_err_row_list)-np.std(ra226_err_row_list)
        
        
        
        
        if len(ra226_row_list)==0 :
            ra226_list.append(error_flag)
            row_specific_errors.append('No_226_Value calculated')
            
        else:
            ra226_row_list = [i for i in ra226_row_list if i != -999]
            upper_limit_226 = np.average(ra226_row_list)+np.std(ra226_row_list)
            lower_limit_226 = np.average(ra226_row_list)-np.std(ra226_row_list)
            ra226_outliers_removed_list = [i for i in ra226_row_list if i < upper_limit_226 and i > lower_limit_226]
            # ra226_outliers_removed_list = [i for i in ra226_row_list if i != -999]
            
            
            if len(ra226_outliers_removed_list)>1:
                ra226_list.append(np.average(ra226_outliers_removed_list))
            if len(ra226_outliers_removed_list)==1:
                ra226_list.append(np.average(ra226_outliers_removed_list))
                row_specific_errors.append('Only one 226-Ra value averaged')
                
            if len(ra226_outliers_removed_list)<1:
                ra226_list.append(np.average(error_flag))
                row_specific_errors.append('226-Ra values non-concordant')
                
                
        if len(ra226_err_row_list)==0 :
            ra226_err_list.append(error_flag)
            row_specific_errors.append('No_226_err_Value calculated')
            
        else:
            ra226_err_row_list = [i for i in ra226_err_row_list if i != -999]
            upper_limit_226_err = np.average(ra226_err_row_list)+np.std(ra226_err_row_list)
            lower_limit_226_err = np.average(ra226_err_row_list)-np.std(ra226_err_row_list)
            ra226_err_outliers_removed_list = [i for i in ra226_err_row_list if i < upper_limit_226_err and i > lower_limit_226_err]
            # ra226_err_outliers_removed_list = [i for i in ra226_err_row_list if i != -999]
            #print (ra226_err_outliers_removed_list)
            
            if len(ra226_err_outliers_removed_list)>1:
                ra226_err_list.append(np.average(ra226_err_outliers_removed_list))
            if len(ra226_err_outliers_removed_list)==1:
                ra226_err_list.append(np.average(ra226_err_outliers_removed_list))
                row_specific_errors.append('Only one 226-Ra_err value averaged')
                
            if len(ra226_err_outliers_removed_list)<1:
                ra226_err_list.append(error_flag)
                row_specific_errors.append('226-Ra_err values non-concordant')
                
            
            
    
        
########################################################################################################################################### 
        error_list.append(row_specific_errors)
        read_error_list.append(read_specific_errors)

        # print (len(error_list), len(read_error_list), len(xs224_list))
    
    summary_df['224xs'] = xs224_list    
    summary_df['224xs_err'] = xs224_err_list    
    summary_df['224xs_t0'] = xs224_t0_list
    summary_df['224xs_t0_err'] = summary_df['224xs_err']*(summary_df['224xs_t0']/summary_df['224xs'])
    summary_df['Fraction_of_original_224_remaining'] = fraction_decayed_224_list
    summary_df['228Th'] = th228_list
    summary_df['228Th_err'] = th228_err_list

    summary_df['223xs'] = xs223_list 
    summary_df['223xs_err'] = xs223_err_list 
    summary_df['223xs_t0'] = xs223_t0_list
    summary_df['223xs_t0_err'] = summary_df['223xs_err']*(summary_df['223xs_t0']/summary_df['223xs'])
    summary_df['Fraction_of_original_223_remaining'] = fraction_decayed_223_list
    summary_df['227Ac'] = ac227_list
    summary_df['227Ac_err'] = ac227_err_list

    summary_df['223xs_thstdonly'] = xs223_thstdonly_list 
    summary_df['223xs_thstdonly_err'] = xs223_thstdonly_err_list 
    summary_df['223xs_thstdonly_t0'] = xs223_thstdonly_t0_list
    summary_df['223xs_thstdonly_t0_err'] = summary_df['223xs_thstdonly_err']*(summary_df['223xs_thstdonly_t0']/summary_df['223xs_thstdonly'])
    summary_df['Fraction_of_original_223_thstdonly_remaining'] = fraction_decayed_223_thstdonly_list
    summary_df['227Ac_thstdonly'] = ac227_thstdonly_list
    summary_df['227Ac_thstdonly_err'] = ac227_thstdonly_err_list

    summary_df['228Ra'] = ra228_list
    summary_df['228Ra_err'] = ra228_err_list
    summary_df['xs_calc_errors'] = error_list
    summary_df['read_errors'] = read_error_list

    summary_df['226Ra'] = ra226_list
    summary_df['226Ra_err'] = ra226_err_list
    
    
    cols = list(log_df.columns) + ['224xs','224xs_err', '224xs_t0', '224xs_t0_err',	'Fraction_of_original_224_remaining', '228Th',	 '228Th_err', 
                                   '223xs','223xs_err', '223xs_t0', '223xs_t0_err', 'Fraction_of_original_223_remaining', '227Ac',	'227Ac_err',
                                   '223xs_thstdonly','223xs_thstdonly_err', '223xs_thstdonly_t0', '223xs_thstdonly_t0_err', 'Fraction_of_original_223_thstdonly_remaining', '227Ac_thstdonly',	'227Ac_thstdonly_err', 
                                   '226Ra', '226Ra_err', '228Ra', '228Ra_err', 'xs_calc_errors', 'read_errors' ]
    summary_df = summary_df[cols]
    
    summary_df.to_csv(output_directory/Path('Dataframes/Summary_Sample_Results_Dataframe'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv'))
    
    
    return(summary_df)

# print (create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable,output_directory))