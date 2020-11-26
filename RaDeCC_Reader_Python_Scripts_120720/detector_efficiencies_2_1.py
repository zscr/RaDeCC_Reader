



#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________

"""
This script uses the radecc_reader_lvl1_1 script to analyse the raw read files and then calculates the efficiencies of each channel on each detector.
Calculations from Geibert et al. (2013), Limnol. Oceanogr. Methods, 11.
Output: CSV table of efficiencies and errors (or standard deviations)
"""


# -*- coding: utf-8 -*-
"""
Created on Thu May 31 19:10:08 2018

@author: sedm5551
"""
import os
import time
import numpy as np
import math
import pandas as pd
from radecc_reader_lvl1_2_0 import slope_calculator, cc_calculator, interval_calculator


def create_effdf(output_directory, thstd, acstd, blank, ac_halfLife, 
                 detector_list, spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat, 
                 acstd_start_activity_dict, acstd_date_dict, thstd_start_activity_dict, blank_name_list, detector_dict, detector_adjustment_coefficients_dict):
    thstdList = []
    acstdList = []
    blankstdList = []
    #***220 Efficiencies***
    #____________________________________________________________________________________________________________________________________________________________________
    #Make dataframe of thstd reads
    #____________________________________________________________________________________________________________________________________________________________________
    standard_name_list = []
    # standard_manufacture_date_list = []
    standard_start_activity_list = []
    
    print('\n---Calculating efficiencies---\n')
    # print (detector_list)
    
    for dirName, subdirList, fileList in os.walk(output_directory/(thstd)):
        if len(fileList)!= 0:
            for file in fileList:
                thstdList.append(slope_calculator(output_directory , detector_dict, output_directory/(thstd)/file, spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat, thstd, acstd, blank))
                for thstd_name in thstd_start_activity_dict.keys():
                    if thstd_name.lower() in file.lower():
                        # print (thstd_name)
                        standard_name_list.append(thstd_name)
                        # standard_manufacture_date_list.append(pd.to_datetime(thstd_date_dict[thstd_name], dayfirst = DDMMYYY_DateFormat))
                        standard_start_activity_list.append(thstd_start_activity_dict[thstd_name])
                        

                        
    thstd_df = pd.DataFrame(thstdList, columns=['Read_Start_Time', 'Read_End_Time', 'Slope', 'R_slope', 'cnt219', 'cnt219_abserr', 'cnt220', 'cnt220_abserr', 
                                                'cpm_219', 'err_219', 'cpm_220', 'err_220', 'cpm_Tot', 'err_Tot', 'y219cc', 'y219cc_err', 
                                                'y220cc', 'y220cc_err', 'corr219', 'corr219_err', 'corr220', 'corr220_err','final219', 
                                                       'final220',  'Read_Runtime', 'final219_err', 'final220_err', 'cntTot_abserr', 
                                                      'errslope_abs', 'Detector_Name', 'Cartridge_Type', 'Read_Number', 'Spike_Value', 'Error_List'])
    # print(len(fileList), len(standard_name_list))
    thstd_df['Filename']= fileList
    thstd_df['Standard_name']= standard_name_list
    # thstd_df['Standard_manufacture_date'] = standard_manufacture_date_list
    thstd_df['Standard_start_activity'] = standard_start_activity_list
    thstd_df['E220'] = thstd_df.final220/thstd_df['Standard_start_activity']
    



    #____________________________________________________________________________________________________________________________________________________________________
    #Make dataframe of acstd reads
    #____________________________________________________________________________________________________________________________________________________________________
    standard_name_list = []
    standard_manufacture_date_list = []
    standard_start_activity_list = []
    
    for dirName, subdirList, fileList in os.walk(output_directory/(acstd)):
        if len(fileList)!= 0:
            for file in fileList:
                acstdList.append(slope_calculator(output_directory , detector_dict, output_directory/(acstd)/file, spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat, thstd, acstd, blank))
                for acstd_name in acstd_date_dict.keys():
                    if acstd_name.lower() in file.lower():
                        # print (acstd_name)
                        standard_name_list.append(acstd_name)
                        standard_manufacture_date_list.append(pd.to_datetime(acstd_date_dict[acstd_name], dayfirst = DDMMYYY_DateFormat))
                        standard_start_activity_list.append(acstd_start_activity_dict[acstd_name])
                        
                        
    acstd_df = pd.DataFrame(acstdList, columns=['Read_Start_Time', 'Read_End_Time', 'Slope', 'R_slope', 'cnt219', 'cnt219_abserr', 'cnt220', 'cnt220_abserr', 
                                                'cpm_219', 'err_219', 'cpm_220', 'err_220', 'cpm_Tot', 'err_Tot', 'y219cc', 'y219cc_err', 
                                                'y220cc', 'y220cc_err', 'corr219', 'corr219_err', 'corr220', 'corr220_err','final219', 
                                                       'final220',  'Read_Runtime', 'final219_err', 'final220_err', 'cntTot_abserr', 
                                                      'errslope_abs', 'Detector_Name', 'Cartridge_Type', 'Read_Number', 'Spike_Value', 'Error_List'])
    acstd_df['Filename']= fileList
    acstd_df['Standard_name']= standard_name_list
    acstd_df['Standard_manufacture_date'] = standard_manufacture_date_list
    acstd_df['Standard_start_activity'] = standard_start_activity_list
    acstd_df['Time_since_std_made'] = acstd_df.Read_Start_Time - acstd_df['Standard_manufacture_date']
    acstd_df['Time_since_std_made_in_s'] = acstd_df['Time_since_std_made'].dt.total_seconds()
    #t2 = ((acstd_df.Read_Start_Time[0]-acstd_prepDate).delta*1e-9)/60/60/24
    #print (t2)
    acstd_df['E219'] = acstd_df.final219/(acstd_df['Standard_start_activity']* np.exp(-(np.log(2)/(ac_halfLife*365*24*60*60))*(acstd_df['Time_since_std_made_in_s'])))
    
    #____________________________________________________________________________________________________________________________________________________________________
    #Make dataframe of blank reads
    #____________________________________________________________________________________________________________________________________________________________________
    standard_name_list = []
    for dirName, subdirList, fileList in os.walk(output_directory/(blank)):
        if len(fileList)!= 0:
            for file in fileList:
                blankstdList.append(slope_calculator(output_directory , detector_dict, output_directory/(blank)/file, spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat, thstd, acstd, blank))
                for blank_name in blank_name_list:
                    if blank_name.lower() in file.lower():
                        # print (blank_name)
                        standard_name_list.append(blank_name)
                        
    blank_df = pd.DataFrame(blankstdList, columns=['Read_Start_Time', 'Read_End_Time', 'Slope', 'R_slope', 'cnt219', 'cnt219_abserr', 'cnt220', 'cnt220_abserr',
                                                   'cpm_219', 'err_219', 'cpm_220', 'err_220', 'cpm_Tot', 'err_Tot', 'y219cc', 'y219cc_err', 
                                                'y220cc', 'y220cc_err', 'corr219', 'corr219_err', 'corr220', 'corr220_err','final219', 
                                                       'final220',  'Read_Runtime', 'final219_err', 'final220_err', 'cntTot_abserr', 
                                                      'errslope_abs', 'Detector_Name', 'Cartridge_Type', 'Read_Number', 'Spike_Value', 'Error_List'])
    blank_df['Filename']= fileList
    blank_df['Standard_name']= standard_name_list
    
    no_of_thstd_reads = []
    no_of_acstd_reads = []
    no_of_blank_reads = []
    
    for detector in detector_list:
        
        no_of_acstd_reads.append(len(acstd_df[acstd_df['Detector_Name']== detector].E219))
        print (len(acstd_df[acstd_df['Detector_Name']== detector].E219))
        no_of_thstd_reads.append(len(thstd_df[thstd_df['Detector_Name']== detector].E220))
        print (len(thstd_df[thstd_df['Detector_Name']== detector].E220))
        no_of_blank_reads.append(len(blank_df[blank_df['Detector_Name']== detector].final220))
        print (len(blank_df[blank_df['Detector_Name']== detector].final220))
       
    summary_df = pd.DataFrame(np.transpose([detector_list, no_of_acstd_reads, no_of_thstd_reads, no_of_blank_reads]), columns = ['Detector','no_of_acstd_reads', 'no_of_thstd_reads','no_of_blank_reads'])
    
    ave_e220 = []
    stdev_e220 = []
    ave_e219 = []
    stdev_e219 = []
    ave_blank219 = []
    stdev_blank219 = []
    ave_blank220 = []
    stdev_blank220 = []
    ave_blanktot = []
    stdev_blanktot = []
    adjustment_coefficient_list = []
    
    for detector in summary_df.Detector:
        ave_e220.append(np.average(thstd_df[thstd_df['Detector_Name']== detector].E220))
        stdev_e220.append(np.std(thstd_df[thstd_df['Detector_Name']== detector].E220))
        ave_e219.append(np.average(acstd_df[acstd_df['Detector_Name']== detector].E219))
        stdev_e219.append(np.std(acstd_df[acstd_df['Detector_Name']== detector].E219))
        if len(blank_df)>0:
            ave_blank219.append(np.average(blank_df[blank_df['Detector_Name']== detector].final219))
            stdev_blank219.append(np.std(blank_df[blank_df['Detector_Name']== detector].final219))
            ave_blank220.append(np.average(blank_df[blank_df['Detector_Name']== detector].final220))
            stdev_blank220.append(np.std(blank_df[blank_df['Detector_Name']== detector].final220))
            ave_blanktot.append(np.average(blank_df[blank_df['Detector_Name']== detector].cpm_Tot))
            stdev_blanktot.append(np.std(blank_df[blank_df['Detector_Name']== detector].cpm_Tot))
        else:
            ave_blank219.append(0)
            stdev_blank219.append(0)
            ave_blank220.append(0)
            stdev_blank220.append(0)
            ave_blanktot.append(0)
            stdev_blanktot.append(0)
        
        adjustment_coefficient_list.append(detector_adjustment_coefficients_dict[detector])
    
    summary_df['Average_E220'] = ave_e220
    summary_df['Standard_Deviation_E220'] = stdev_e220
    summary_df['Average_E219'] = ave_e219
    summary_df['Standard_Deviation_E219'] = stdev_e219
    summary_df['Average_bkg_219'] = ave_blank219
    summary_df['Standard_Deviation_Blank_219'] = stdev_blank219
    summary_df['Average_bkg_220'] = ave_blank220
    summary_df['Standard_Deviation_Blank_220'] = stdev_blank220
    summary_df['Average_bkg_Tot'] = ave_blanktot
    summary_df['Standard_Deviation_Blank_Tot'] = stdev_blanktot
    summary_df['E219_from_E220_adjustment_coefficient'] = adjustment_coefficient_list
    
    summary_df['E219_from_E220'] = summary_df.Average_E220*summary_df.E219_from_E220_adjustment_coefficient
    summary_df['E219_from_E220_uncertainty'] = summary_df.Standard_Deviation_E220*summary_df.E219_from_E220_adjustment_coefficient
    
    if os.path.exists(output_directory/'Dataframes') == False:
            os.mkdir(output_directory/'Dataframes')
    
    csv_filepath_220s = output_directory/'Dataframes'/('220_channel_efficiencies_dataframe'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv')
    if os.path.exists(csv_filepath_220s) == False:
        thstd_df.to_csv(csv_filepath_220s)
    
    csv_filepath_219s = output_directory/'Dataframes'/('219_channel_efficiencies_dataframe'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv')
    if os.path.exists(csv_filepath_219s) == False:
        acstd_df.to_csv(csv_filepath_219s)
    
    csv_filepath_blanks = output_directory/'Dataframes'/('blank_channel_efficiencies_dataframe'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv')
    if os.path.exists(csv_filepath_blanks) == False:
        blank_df.to_csv(csv_filepath_blanks)
        
    csv_filepath_summary = output_directory/'Dataframes'/('Summary_efficiencies_dataframe'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv')
    if os.path.exists(csv_filepath_summary) == False:
        summary_df.to_csv(csv_filepath_summary)
    
    return(summary_df)
    
#print (create_effdf (output_directory, thstd, acstd, blank, thstd_activity, acstd_activity, acstd_prepDate, ac_halfLife, detector_list, adjustment_coefficient, spike_sensitivity, equilibration_time_variable))