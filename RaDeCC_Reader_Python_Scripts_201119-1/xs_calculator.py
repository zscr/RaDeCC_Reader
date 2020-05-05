#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:04:37 2020

@author: seanselzer
"""
read_a = 2
read_b = 4
isotope_column_string = 'vdpm223 (dpm/m^3)'

import numpy as np


def xs_calculator (lvl2_main_df, sample_variable, sub_sample_variable, row_sample_variable, row_sub_sample_variable, 
                   isotope, isotope_column_string, isotope_column_string_err, isotope_lambda_days, 
                   read_a, read_b, read_number_set):
            
            if isotope == 'Ra-223':
                parent = 'Ac-227'
            else:
                parent = 'Th-228'

            reada_vdpm = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==read_a))
                    , isotope_column_string]
            reada_vdpm_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==read_a))
                    , isotope_column_string_err]
            reada_days_since_sampling = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==read_a))
                    , 'sampling_to_read_time_(days)']
            
            readb_vdpm = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==read_b))
                    , isotope_column_string]
            readb_vdpm_err = lvl2_main_df.loc[((lvl2_main_df[sample_variable]==row_sample_variable) 
                    & (lvl2_main_df[sub_sample_variable]==row_sub_sample_variable)
                    & (lvl2_main_df['read_number']==read_b))
                    , isotope_column_string_err]
            
            if len(reada_vdpm)>1 and len(readb_vdpm)<1:
                row_specific_error = (isotope, ': multiple_'+read_a+'_reads_averaged')
                remaining_fraction_of_isotope = np.exp(-isotope_lambda_days*np.average(reada_days_since_sampling))
                sample_xs_list = []
                sample_xs_err_list = []
                sample_xs_t0_list = []
                for i in range(len(reada_vdpm)):
                    fraction_decayed_since_sampling = np.exp(-isotope_lambda_days*reada_days_since_sampling.iloc[i])
                    sample_xs_list.append(reada_vdpm.iloc[i]-readb_vdpm.iloc[0])
                    sample_xs_err_list.append(np.sqrt(reada_vdpm_err.iloc[i]**2 + readb_vdpm_err.iloc[0]**2))
                    sample_xs_t0_list.append((reada_vdpm.iloc[i]-readb_vdpm.iloc[0])/fraction_decayed_since_sampling)
                
                xs = np.average(sample_xs_list)
                xs_err = np.average(sample_xs_err_list)
                xs_t0 = np.average(sample_xs_t0_list)
                parent_activity = readb_vdpm.iloc[0]
                parent_activity_err = readb_vdpm.iloc[0]
                
            if len(reada_vdpm)<1 and len(readb_vdpm)>1:
                row_specific_error = (isotope,', ', parent,': multiple_'+read_b+'_reads_averaged')
                remaining_fraction_of_isotope = np.exp(-isotope_lambda_days*reada_days_since_sampling.iloc[0])
                xs = reada_vdpm.iloc[0]-np.average(readb_vdpm)
                xs_err = np.sqrt(reada_vdpm_err.iloc[0]**2 + np.average(readb_vdpm_err)**2)
                xs_t0 = (reada_vdpm.iloc[0]-np.average(readb_vdpm))/remaining_fraction_of_isotope
                parent_activity = np.average(readb_vdpm)
                parent_activity_err = np.average(readb_vdpm_err)
                
            if len(reada_vdpm)>1 and len(readb_vdpm)>1:
                row_specific_error = (isotope,', ',parent,': multiple_'+read_a+'_and_'+read_b+'_reads_averaged')
                remaining_fraction_of_isotope = np.exp(-isotope_lambda_days*np.average(reada_days_since_sampling))
                sample_xs_list = []
                sample_xs_err_list = []
                sample_xs_t0_list = []
                for i in range(len(reada_vdpm)):
                    fraction_decayed_since_sampling = np.exp(-isotope_lambda_days*reada_days_since_sampling.iloc[i])
                    sample_xs_list.append(reada_vdpm.iloc[i]-np.average(readb_vdpm))
                    sample_xs_err_list.append(np.sqrt(reada_vdpm_err.iloc[i]**2 + np.average(readb_vdpm_err)**2))
                    sample_xs_t0_list.append((reada_vdpm.iloc[i]-np.average(readb_vdpm))/fraction_decayed_since_sampling)
                xs = np.average(sample_xs_list)
                xs_err = np.average(sample_xs_err_list)
                xs_t0 = np.average(sample_xs_t0_list)
                parent_activity = np.average(readb_vdpm)
                parent_activity_err = np.average(readb_vdpm_err)
                
            else:
                row_specific_error = None
                remaining_fraction_of_isotope = np.exp(-isotope_lambda_days*reada_days_since_sampling.iloc[0])
                xs = reada_vdpm.iloc[0]-readb_vdpm.iloc[0]
                xs_err = np.sqrt(reada_vdpm_err.iloc[0]**2 + readb_vdpm_err.iloc[0]**2)
                xs_t0 = (reada_vdpm.iloc[0]-readb_vdpm.iloc[0])/remaining_fraction_of_isotope
                parent_activity = readb_vdpm.iloc[0]
                parent_activity_err = readb_vdpm_err.iloc[0]
                
            return(xs, xs_err, remaining_fraction_of_isotope, xs_t0, parent_activity, parent_activity_err, row_specific_error)
   
