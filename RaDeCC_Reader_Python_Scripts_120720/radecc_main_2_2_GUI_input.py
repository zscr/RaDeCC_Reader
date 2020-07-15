# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:41:41 2018

@author: sedm5551
e"""
import os
import pandas as pd
import numpy as np
import time
import ast
from pathlib import Path
from dir_constructor_v2 import dir_constructor
from dir_filler import dir_filler
from detector_efficiencies_2_1 import create_effdf
from amalgam_2_1 import amalgam_2
from logsheet_reader_2_0 import logsheet_scan
from create_summary_dataframe import create_summary_dataframe
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________




# #__________________________________________________________________________________________________________________________________________________________
# """##########  USER INPUT AREA  ###########"""
# #__________________________________________________________________________________________________________________________________________________________
# #input_directory*: This is the filepath of the folder in which the sample, standard and blank read files as well as logsheets were placed. 
# # e.g. /Users/username/Desktop/Project_X/raw_data
# input_directory = Path('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Raw_Data_Example')
# #*output_directory*: This is filepath of the folder in which you would like the output to be placed.   e.g. Filepath: /Users/username/Desktop/Project_X/Output_Data
# output_directory = Path('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Results_Folder_'+time.strftime("%Y-%m-%d_%H%M%S"))
# #*output_filename* : the name you would like to give the ouput file.   e.g. project_x_output.csv
# output_filename = 'Example_Results_Dataframe_'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv'

# logfile_directory = Path('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Raw_Data_Example/StnX_Logsheet.csv')

# #Date Format: If the dates in read files and logsheets are DD/MM/YYYY (day first) then input 'True' else for MM/DD/YYYY input 'False'
# DDMMYYY_DateFormat = True

# #*linear_data_type* : This variable is set to True if the dataset being input is linear/1-dimensional (e.g. a string of ocean surface samples or a time series at one point/location). 
# # Alternatively this is set to False if the dataset being input is 2-dimensional (e.g. a time-series at a string of locations or a string of depth profiles).
# linear_data_type = False


# #spike_sensitivity is the threshold of counts in a time interval that determines whether a spike is anomalous or not. 
# # Set spike_sensitivity = 1000 to disable spike removal or reduce to below 100 to increase sensitivity.
# spike_sensitivity = 100

# #Enter below, the initial equilibration time (minutes) to be deducted from the 222Rn ingrowth slope calculation for the evaluation of 226Ra dpm
# equilibration_time = 0

# #Enter below, the runtime counting intervals in minutes that were set for the RaDeCC detectors for these sample reads (default = 10 minute intervals)
# time_interval_mins = 10


# #__________________________________________________________________________________________________________________________________________________________
# """Info for directory builder"""
# #__________________________________________________________________________________________________________________________________________________________

# #*sample_type*: This is the sample naming convention e.g. if your first sample is sample001 and your second is sample002 then sample_type is 'sample'
# # sample_type = 'StnX'
# #*number_of_samples*: The is the number of samples (not sub-samples) (1-999) 
# # number_of_samples = 30


# #__________________________________________________________________________________________________________________________________________________________
# """Information for the efficiency calculations"""
# #__________________________________________________________________________________________________________________________________________________________

# #Specify, if different from the below, the identifiers used for each of the standards and the blank below:
# # 228-Thorium Standard:

# # thstd_date_dict = {'green':'13/10/2014 00:00:00', 'yellow':'13/10/2014 00:00:00'}
# thstd_start_activity_dict = {'green':12.20454, 'yellow':12.20454}

# # 227-Actinium Standard:

# acstd_date_dict = {'red':'09/10/2014 ', 'blue':'13/10/2014 00:00:00'}
# acstd_start_activity_dict = {'red':10.49429, 'blue':10.49429}

# # Blank:
# blank_name_list = ['exposure', 'analytical']



# adjustment_coefficient = 0.45
# # adjustment_coefficient_uncertainty = 0.05

# #detector_dict: list all detectors used for the analysis of the sample set in the form: ['detector_1', 'detector_2', ..., 'detector_n']
# detector_dict = {'detector1':0.000186, 'detector2':0.000187}
# detector_226_efficiencies_dict = {'detector1':1, 'detector2':1}
# detector_adjustment_coefficients_dict = {'detector1':0.45, 'detector2':45}

# #__________________________________________________________________________________________________________________________________________________________
# """Information for logsheet reader"""
# #__________________________________________________________________________________________________________________________________________________________

# sample_variable = 'sample_name'

# #Confirm the exact names of the columns in the logsheet which correspond to the following variables:
# #The name of the column in the logsheet(s) that contains the start time of sampling for each sample/sub_sample.
# sample_mid_time = 'Sampling_Start_Time'
# sample_mid_date = 'Date'

# #The sub sample variable could be depth for a string of depth profiles or time for time-series at a string of locations.
# #sub_sample_variable is the name of the column in the logsheet(s) that contains the value of the sub sample variable for each sub sample
# sub_sample_variable = 'Sample_Depth'

# #sample_volume is the name of the column in the logsheet(s) that contains the volumes of each sample/sub-sample.
# sample_volume = 'Volume_sampled'
# sample_volume_error = 'Volume_error'


# #__________________________________________________________________________________________________________________________________________________________
# #__________________________________________________________________________________________________________________________________________________________
# #__________________________________________________________________________________________________________________________________________________________



# #__________________________________________________________________________________________________________________________________________________________
# """Working Code, Do Not Change"""
# #__________________________________________________________________________________________________________________________________________________________

def radecc_reader_main(gui_input_df):
    input_directory = Path(gui_input_df['Input_Directory'][0])
    
    print(Path(gui_input_df['Output_Directory'][0])/('RaDeCC_Reader_Ouput'+time.strftime("%Y-%m-%d_%H%M%S")))

    output_directory = Path(gui_input_df['Output_Directory'][0])/('RaDeCC_Reader_Ouput'+time.strftime("%Y-%m-%d_%H%M%S"))
    print(output_directory)
    output_filename = 'Read_Results_Dataframe_'+time.strftime("%Y-%m-%d_%H%M%S")+'.csv'
    logfile_directory = Path(gui_input_df['Logsheet_Filepath'][0])
    DDMMYYY_DateFormat = gui_input_df['DDMMYY_Format'][0]
    if gui_input_df['sub_sample_check_variable'][0] == 1:
        linear_data_type = True 
    else:
        linear_data_type = False
    spike_sensitivity = gui_input_df['Spike_sensitivity_variable'][0]
    equilibration_time = gui_input_df['Equilibration_time'][0]
    #time_interval_mins = gui_input_df['Input_Directory']
    thstd_start_activity_dict = ast.literal_eval(gui_input_df['th228_standard_start_activities_dict'][0])
    acstd_date_dict = ast.literal_eval(gui_input_df['ac227_standard_manufacture_date_dict'][0])
    acstd_start_activity_dict = ast.literal_eval(gui_input_df['ac227_standard_start_activities_dict'][0])
    blank_name_list = ast.literal_eval(gui_input_df['blank_standard_names_list'][0])
    detector_dict = ast.literal_eval(gui_input_df['detector_calibration_values_dict'][0])
    detector_226_efficiencies_dict = ast.literal_eval(gui_input_df['detector_226_efficiency_dict'][0])
    detector_adjustment_coefficients_dict = ast.literal_eval(gui_input_df['detector_adjustment_coefficient_dict'][0])
    sample_mid_time = gui_input_df['sample_mid_time'][0]
    sample_mid_date = gui_input_df['sample_mid_date'][0]
    sample_variable = gui_input_df['sample_name_column_variable'][0]
    sub_sample_variable = gui_input_df['sub_sample_option_variable'][0]
    sample_volume = gui_input_df['sample_volume_variable'][0]
    sample_volume_error = gui_input_df['sample_volume_error_variable'][0]


    start = time.time()

    acstd = 'actinium_standards'
    thstd = 'thorium_standards'
    blank = 'blank_standards'

    # 227-Actinium half-life (years):
    ac_halfLife = 21.772 #YEARS
    half_life223 = 11.43 #days
    half_life224 = 3.6 #days

    equilibration_time_variable = int(equilibration_time)

    folder_names_list = []
    folder_names_list.append('Read_Files')
    folder_names_list.append(thstd)
    folder_names_list.append(acstd)
    folder_names_list.append(blank)
    folder_names_list.append('Misc')
    folder_names_list.append('Logsheet')

    log_df = pd.read_csv(logfile_directory)
    dir_constructor(output_directory, log_df, sample_variable, sub_sample_variable, linear_data_type, folder_names_list)
    dir_filler(output_directory, input_directory, acstd_date_dict, thstd_start_activity_dict, blank_name_list, acstd, thstd, blank, log_df, logfile_directory, linear_data_type, sample_variable, sub_sample_variable)

    #thstd_prepDate = pd.to_datetime(thstd_prepDatestr, dayfirst = DDMMYYY_DateFormat)
    #acstd_prepDate = pd.to_datetime(acstd_prepDatestr, dayfirst = DDMMYYY_DateFormat)

    ra223_lambda = (np.log(2)/(half_life223*24*60))
    ra224_lambda = (np.log(2)/(half_life224*24*60))

    detector_dict.update({'No_Read':-999})
    detector_226_efficiencies_dict.update({'No_Read':-999})
    detector_adjustment_coefficients_dict.update({'No_Read':-999})

    eff_df = create_effdf (output_directory, thstd, acstd, blank, ac_halfLife, 
                        list(detector_dict.keys()), spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat,
                        acstd_start_activity_dict, acstd_date_dict, thstd_start_activity_dict, blank_name_list, detector_dict, detector_adjustment_coefficients_dict)

    # log_df = logsheet_scan(output_directory, sample_variable)

    lvl2_main_df = amalgam_2(eff_df, ra223_lambda, ra224_lambda, log_df, sample_volume, sample_volume_error, sample_variable, sub_sample_variable, 
                                spike_sensitivity, equilibration_time_variable, output_directory, sample_mid_time, sample_mid_date, 
                                linear_data_type, DDMMYYY_DateFormat, thstd, acstd, blank, detector_dict, detector_226_efficiencies_dict, )

    folder_filepath = output_directory/'Dataframes'
    if folder_filepath.exists() == False:
        os.mkdir(folder_filepath)

    if (folder_filepath/output_filename).exists() == False:
        lvl2_main_df.to_csv(folder_filepath/output_filename)

    print (lvl2_main_df)

    create_summary_dataframe(lvl2_main_df, log_df, sample_variable, sub_sample_variable, output_directory)

    end = time.time()
    print ('Calculations completed in ',end-start,'seconds.')
    return_string = 'Run Complete ('+time.strftime("%H:%M:%S %Y-%m-%d")+')'
    return ([True, return_string])


# radecc_reader_main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    