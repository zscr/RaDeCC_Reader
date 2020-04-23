# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:41:41 2018

@author: sedm5551
e"""
import os
import pandas as pd
import numpy as np
import time
from pathlib import Path
from dir_constructor_linear_sampling_v2 import dir_constructor_linear 
from dir_constructor_v2 import dir_constructor
from dir_filler_linear_sampling import dir_filler_linear
from dir_filler import dir_filler
from detector_efficiencies_2_1 import create_effdf
from amalgam_2_1 import amalgam_2
from logsheet_reader_2_0 import logsheet_scan
from create_summary_dataframe import create_summary_dataframe
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________




#__________________________________________________________________________________________________________________________________________________________
"""##########  USER INPUT AREA  ###########"""
#__________________________________________________________________________________________________________________________________________________________
#input_directory*: This is the filepath of the folder in which the sample, standard and blank read files as well as logsheets were placed. 
# e.g. /Users/username/Desktop/Project_X/raw_data
input_directory = Path('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Raw_Data_Example')
#*output_directory*: This is filepath of the folder in which you would like the output to be placed.   e.g. Filepath: /Users/username/Desktop/Project_X/Output_Data
output_directory = Path('/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/Example_Output_Folder')
#*output_filename* : the name you would like to give the ouput file.   e.g. project_x_output.csv
output_filename = 'Example_Results_Dataframe.csv'

#Date Format: If the dates in read files and logsheets are DD/MM/YYYY (day first) then input 'True' else for MM/DD/YYYY input 'False'
DDMMYYY_DateFormat = True

#*linear_data_type* : This variable is set to True if the dataset being input is linear/1-dimensional (e.g. a string of ocean surface samples or a time series at one point/location). 
# Alternatively this is set to False if the dataset being input is 2-dimensional (e.g. a time-series at a string of locations or a string of depth profiles).
linear_data_type = False


#spike_sensitivity is the threshold of counts in a time interval that determines whether a spike is anomalous or not. 
# Set spike_sensitivity = 1000 to disable spike removal or reduce to below 100 to increase sensitivity.
spike_sensitivity = 100

#Enter below, the initial equilibration time (minutes) to be deducted from the 222Rn ingrowth slope calculation for the evaluation of 226Ra dpm
equilibration_time = 100

#Enter below, the runtime counting intervals in minutes that were set for the RaDeCC detectors for these sample reads (default = 10 minute intervals)
time_interval_mins = 10


#__________________________________________________________________________________________________________________________________________________________
"""Info for directory builder"""
#__________________________________________________________________________________________________________________________________________________________

#*sample_type*: This is the sample naming convention e.g. if your first sample is sample001 and your second is sample002 then sample_type is 'sample'
sample_type = 'StnX'
#*number_of_samples*: The is the number of samples (not sub-samples) (1-999) 
number_of_samples = 30


#__________________________________________________________________________________________________________________________________________________________
"""Information for the efficiency calculations"""
#__________________________________________________________________________________________________________________________________________________________

#Specify, if different from the below, the identifiers used for each of the standards and the blank below:
# 228-Thorium Standard:
thstd = 'thstd'
thstd_date_dict = {'green':'13/10/2014 00:00:00', 'yellow':'13/10/2014 00:00:00'}
thstd_start_activity_dict = {'green':12.20454, 'yellow':12.20454}

# 227-Actinium Standard:

acstd_date_dict = {'red':'13/10/2014 00:00:00', 'blue':'13/10/2014 00:00:00'}
acstd_start_activity_dict = {'red':10.49429, 'blue':10.49429}

# Blank:
blank = 'blank'
blank_name_list = ['exposure', 'analytical']



adjustment_coefficient = 0.45
adjustment_coefficient_uncertainty = 0.05

#detector_list: list all detectors used for the analysis of the sample set in the form: ['detector_1', 'detector_2', ..., 'detector_n']
detector_list = ['detector1', 'detector2']

#__________________________________________________________________________________________________________________________________________________________
"""Information for logsheet reader"""
#__________________________________________________________________________________________________________________________________________________________

sample_variable = 'sample_name'

#Confirm the exact names of the columns in the logsheet which correspond to the following variables:
#The name of the column in the logsheet(s) that contains the start time of sampling for each sample/sub_sample.
sample_mid_time = 'Sampling_Start_Time'

#The sub sample variable could be depth for a string of depth profiles or time for time-series at a string of locations.
#sub_sample_variable is the name of the column in the logsheet(s) that contains the value of the sub sample variable for each sub sample
sub_sample_variable = 'Sample_Depth'

#sample_volume is the name of the column in the logsheet(s) that contains the volumes of each sample/sub-sample.
sample_volume = 'Volume_sampled'
sample_volume_error = 'Volume_error'


#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________























#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________


#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________
start = time.time()

acstd = 'acstd'

# 227-Actinium half-life (years):
ac_halfLife = 21.772 #YEARS
half_life223 = 11.43 #days
half_life224 = 3.6 #days

equilibration_time_variable = int(equilibration_time/time_interval_mins)

deployment_dir_list = []
deployment_dir_list.append(sample_type)
deployment_dir_list.append(thstd)
deployment_dir_list.append(acstd)
deployment_dir_list.append(blank)
deployment_dir_list.append('misc')
deployment_dir_list.append('logsheet')


if linear_data_type == True:
    dir_constructor_linear(input_directory, output_directory, sample_type, number_of_samples, deployment_dir_list)
    dir_filler_linear(output_directory, input_directory, sample_type, acstd_date_dict, thstd_date_dict, blank_name_list)

if linear_data_type == False:
    dir_constructor(input_directory, output_directory, sample_type, number_of_samples, deployment_dir_list)
    dir_filler(output_directory, input_directory, sample_type, acstd_date_dict, thstd_date_dict, blank_name_list)

#thstd_prepDate = pd.to_datetime(thstd_prepDatestr, dayfirst = DDMMYYY_DateFormat)
#acstd_prepDate = pd.to_datetime(acstd_prepDatestr, dayfirst = DDMMYYY_DateFormat)

ra223_lambda = (np.log(2)/(half_life223*24*60))
ra224_lambda = (np.log(2)/(half_life224*24*60))

detector_list.append('No_Read')

eff_df = create_effdf (output_directory, thstd, acstd, blank, ac_halfLife, 
                       detector_list, adjustment_coefficient, spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat,
                       acstd_start_activity_dict, acstd_date_dict, thstd_start_activity_dict, thstd_date_dict, blank_name_list)

log_df = logsheet_scan(output_directory)

lvl2_main_df = amalgam_2(eff_df, ra223_lambda, ra224_lambda, log_df, sample_volume, sample_volume_error, sample_variable, sub_sample_variable, spike_sensitivity, equilibration_time_variable, output_directory, sample_type, sample_mid_time, linear_data_type, DDMMYYY_DateFormat, thstd, acstd, blank)

folder_filepath = output_directory/'Dataframes'
if folder_filepath.exists() == False:
    os.mkdir(folder_filepath)

if (folder_filepath/output_filename).exists() == False:
    lvl2_main_df.to_csv(folder_filepath/output_filename)

print (lvl2_main_df)

create_summary_dataframe(lvl2_main_df, sample_variable, sub_sample_variable)

end = time.time()
print ('Calculations completed in ',end-start,'seconds.')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    