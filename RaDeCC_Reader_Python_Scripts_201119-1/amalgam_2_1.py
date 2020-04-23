#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 12:15:22 2019

@author: seanselzer
"""

import pandas as pd
import os
import numpy as np
import datetime
import re
from pathlib import Path
from detector_efficiencies_2_1 import create_effdf
from radecc_reader_lvl1_2_0 import slope_calculator





#____________________________________________________________________________________________________________________________________________________________

def amalgam_2(eff_df, ra223_lambda, ra224_lambda, log_df, sample_volume, sample_volume_error, sample_variable, sub_sample_variable, spike_sensitivity, equilibration_time_variable, output_directory, sample_type, sample_mid_time, linear_data_type, DDMMYYY_DateFormat, thstd, acstd, blank ):
    main_samplelist = []
    
    print('\n---Creating sample results dataframe---\n')
    
    if linear_data_type == False:
    
        for i in range(len(log_df[sample_variable])):
            sample_series = log_df[sample_variable].iloc[i]
            #print('\n', type(sample_series), sample_series)
            for dirName, subdirList, fileList in os.walk(output_directory/(sample_type+'_folder')/sample_series):
                
                dirName = Path(dirName)
                
                #print(int(log_df[sub_sample_variable].iloc[i]), [int(s) for s in re.findall(r'-?\d+\.?\d*',dirName.split('/')[-1])][0],dirName.split('/')[-1])
                print ('££££££££',log_df[sub_sample_variable].iloc[i], dirName.parts)
                if log_df[sub_sample_variable].iloc[i]in dirName.parts[-1]:
                    for file in fileList:
                        print (file, sample_series, log_df[sub_sample_variable].iloc[i])
                        main_samplelist.append(list(log_df.iloc[i])+[os.path.join(dirName, file)])
    else:
        sample_set = list(set(log_df[sample_variable]))
        #print(sample_set)
        for i in range(len(sample_set)):
            sample_series = sample_set[i]
            #print('\n', type(sample_series), sample_series)
            for dirName, subdirList, fileList in os.walk(output_directory/(sample_type+'_folder')/sample_series):
                
                dirName = Path(dirName)
                
                #print (dirName.split('/')[-1])
                if sample_series.lower() in dirName.parts[-1].lower():
                    
                    for file in fileList:
                        #print (file, sample_series)
                        main_samplelist.append(list(log_df.iloc[i])+[os.path.join(dirName, file)])
                         
    sample_array = np.array(main_samplelist)
    temp_df = pd.DataFrame(sample_array)
    
    temp_df.columns = log_df.columns.values.tolist()+['Filepath'] 
    
    lvl1_calc_list = []
    for i in range(len(temp_df[sample_variable])):

        lvl1_calc_list.append(slope_calculator(output_directory, Path(temp_df['Filepath'].iloc[i]), spike_sensitivity, equilibration_time_variable, DDMMYYY_DateFormat, thstd, acstd, blank))
    
    lvl1_calc_df = pd.DataFrame(lvl1_calc_list, columns = ['Read_Start_Time', 'Read_End_Time', 'Slope', 'stderr_slope', 'cnt219', 'cnt219_abserr', 'cnt220', 'cnt220_abserr', 'cpm_219', 'err_219', 'cpm_220', 'err_220', 'cpm_Tot', 'err_Tot', 'y219cc', 'y219cc_err', 
                                                'y220cc', 'y220cc_err', 'corr219', 'corr219_err', 'corr220', 'corr220_err','final219', 
                                                       'final220', 'Read_Runtime', 'final219_err', 'final220_err', 'cntTot_abserr', 
                                                      'errslope_abs', 'Detector_Name', 'Cartridge_Type', 'Read_Number', 'Spike_Value'])
    
    lvl1_main_df = pd.concat([temp_df, lvl1_calc_df], axis=1, join_axes=[temp_df.index])
    
    lvl1_main_df['Mid_Sample_Datetime'] = pd.to_datetime(lvl1_main_df.Date+' '+lvl1_main_df[sample_mid_time], dayfirst=DDMMYYY_DateFormat)
    lvl1_main_df['Mid_Read_Datetime'] = pd.to_datetime(lvl1_main_df['Read_Start_Time'], dayfirst=DDMMYYY_DateFormat) + pd.to_timedelta(lvl1_main_df['Read_Runtime']/2, unit='m')
    
    
    
    blankcorr219 = []
    blankcorr219_err =[]
    blankcorr220 = []
    blankcorr220_err = []
    dpm219 = []
    dpm219_err = []
    dpm219_thstdonly = []
    dpm219_thstdonly_err = []
    dpm220 = []
    dpm220_err = []
    dpm220tot = []
    vdpm219 = []
    vdpm219_err = []
    vdpm219_thstdonly = []
    vdpm219_thstdonly_err = []
    vdpm220 = []
    vdpm220_err = []
    vdpm220tot = []               
    t1 = []
    vdpm226 = []
    vdpm226_err = []
    
    for i in range(len(lvl1_main_df)):
        
        if lvl1_main_df['Detector_Name'][i].lower() in list(eff_df.Detector):
        
            #final219 - 219 channel blank for relevant detector
            blankcorr219.append(float(lvl1_main_df.final219[i] - eff_df.Average_Blank_219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]))
            #error associated with blankcorr219 correction added
            blankcorr219_err.append(float(np.sqrt(eff_df.Standard_Deviation_Blank_219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]**2 + lvl1_main_df['final219_err'][i]**2)))
            
            #final220 - 220 channel blank for relevant detector
            blankcorr220.append(float(lvl1_main_df.final220[i] - eff_df.Average_Blank_220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]))
            #error associated with blankcorr220 correction added
            blankcorr220_err.append(float(np.sqrt(eff_df.Standard_Deviation_Blank_220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]**2 + lvl1_main_df['final220_err'][i]**2)))
            
            #dpm219 calculation 
            dpm219.append(float(blankcorr219[-1]/eff_df.Average_E219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]))
            #dpm219 error 
            dpm219_err.append(float((np.sqrt((blankcorr219_err[-1]/eff_df.Average_E219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])**2 + ((lvl1_main_df['final219'][i]*eff_df.Standard_Deviation_E219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])/eff_df.Average_E219[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]**2)**2))/dpm219[-1]))
                
            #dpm220 calculation 
            dpm220.append(float(blankcorr220[-1]/eff_df.Average_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]))
            #dpm219 error 
            dpm220_err.append(float((np.sqrt((blankcorr220_err[-1]/eff_df.Average_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])**2 + ((lvl1_main_df['final220'][i]*eff_df.Standard_Deviation_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])/eff_df.Average_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]**2)**2))/dpm220[-1]))
            
            #219 Volume corrections
            vdpm219.append((dpm219[-1]/float(lvl1_main_df[sample_volume][i]))*1000)
            #219 Volume corrections error
            vdpm219_err.append(np.sqrt((dpm219_err[-1]/float(lvl1_main_df[sample_volume][i]))**2 + ((dpm219[-1]*float(lvl1_main_df[sample_volume_error][i]))/(float(lvl1_main_df[sample_volume][i])**2))**2)*1000)
            
            #220 Volume corrections
            vdpm220.append((dpm220[-1]/float(lvl1_main_df[sample_volume][i]))*1000)
            #220 Volume corrections error
            vdpm220_err.append(np.sqrt((dpm220_err[-1]/float(lvl1_main_df[sample_volume][i]))**2 + ((dpm220[-1]*float(lvl1_main_df[sample_volume_error][i]))/(float(lvl1_main_df[sample_volume][i])**2))**2)*1000)
            
                
            ##############################################
            #dpm219_thstdonly calculation using 
            dpm219_thstdonly.append(float(blankcorr219[-1]/eff_df.E219_from_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]))
            #dpm219_thstdonly error 
            dpm219_thstdonly_err.append(float((np.sqrt((blankcorr219_err[-1]/eff_df.E219_from_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])**2 + ((lvl1_main_df['final219'][i]*eff_df.E219_from_E220_uncertainty[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()])/eff_df.E219_from_E220[eff_df.Detector == lvl1_main_df['Detector_Name'][i].lower()]**2)**2))/dpm219_thstdonly[-1]))
                    
            ################################################
                            
            ###############################################################################
            #dpm219_thstdonly Volume corrections
            vdpm219_thstdonly.append((dpm219_thstdonly[-1]/float(lvl1_main_df[sample_volume][i]))*1000)
            #dpm219_thstdonly_err Volume corrections error
            vdpm219_thstdonly_err.append(np.sqrt((dpm219_thstdonly_err[-1]/float(lvl1_main_df[sample_volume][i]))**2 + ((dpm219_thstdonly[-1]*float(lvl1_main_df[sample_volume_error][i]))/(float(lvl1_main_df[sample_volume][i])**2))**2)*1000)
            
            if float(vdpm219_thstdonly[-1]) < 0 :
                vdpm219_thstdonly[-1] = 0
            ###############################################################################
            
            #dpm226 calculation 
            vdpm226.append(((lvl1_main_df['Slope'][i]/0.000186)/float(lvl1_main_df[sample_volume][i]))*1000)
            #dpm226_err calculation 
            vdpm226_err.append(np.sqrt(((lvl1_main_df['stderr_slope'][i]/0.000186)/float(lvl1_main_df[sample_volume][i]))**2 + (((lvl1_main_df['Slope'][i]/0.000186)*float(lvl1_main_df[sample_volume_error][i]))/(float(lvl1_main_df[sample_volume][i])**2))**2)*1000)
            
            
            #Time difference between sampling datetime and read datetime (t1 in Garcia-Solsona)
            diff = pd.to_datetime(lvl1_main_df['Mid_Read_Datetime'][i]) - pd.to_datetime(lvl1_main_df['Mid_Sample_Datetime'][i]) 
            t1.append((diff.seconds/60)+diff.days*24*60)
        
        else:
            print ('\n***ERROR***\nDetector name:', lvl1_main_df['Detector_Name'][i].lower(),'does not match a detector in detector_list\n')
        
            #final219 - 219 channel blank for relevant detector
            blankcorr219.append(999)
            #error associated with blankcorr219 correction added
            blankcorr219_err.append(999)
            
            #final220 - 220 channel blank for relevant detector
            blankcorr220.append(999)
            #error associated with blankcorr220 correction added
            blankcorr220_err.append(999)
            
            #dpm219 calculation 
            dpm219.append(999)
            #dpm219 error 
            dpm219_err.append(999)
                
            #dpm220 calculation 
            dpm220.append(999)
            #dpm219 error 
            dpm220_err.append(999)
            
            #219 Volume corrections
            vdpm219.append(999)
            #219 Volume corrections error
            vdpm219_err.append(dpm219_err[-1]*vdpm219[-1])
            if vdpm219[-1] < 0 :
                vdpm219[-1] = 0
            
            #220 Volume corrections
            vdpm220.append((dpm220[-1]/float(lvl1_main_df[sample_volume][i]))*1000)
            #220 Volume corrections error
            vdpm220_err.append(dpm220_err[-1]*vdpm220[-1])  
            if vdpm220[-1] < 0 :
                vdpm220[-1] = 0 
                
            ##############################################
            #dpm219 calculation using 
            dpm219_thstdonly.append(999)
            #dpm219 error 
            dpm219_thstdonly_err.append(999)
                    
            ################################################
                            
            ###############################################################################
            #219 Volume corrections
            vdpm219_thstdonly.append((dpm219_thstdonly[-1]/float(lvl1_main_df[sample_volume][i]))*1000)
            #219 Volume corrections error
            vdpm219_thstdonly_err.append(dpm219_thstdonly_err[-1]*vdpm219_thstdonly[-1])
            if float(vdpm219_thstdonly[-1]) < 0 :
                vdpm219_thstdonly[-1] = 0
            ###############################################################################
            
            
            vdpm226.append(((lvl1_main_df['Slope'][i]/0.000186)/float(lvl1_main_df[sample_volume][i]))*1000)
            if vdpm226[-1]<0:
                vdpm226[-1] = 0
            vdpm226_err.append(np.sqrt(((lvl1_main_df['stderr_slope'][i]/0.000186)/float(lvl1_main_df[sample_volume][i]))**2 + (((lvl1_main_df['Slope'][i]/0.000186)*float(lvl1_main_df[sample_volume_error][i]))/(float(lvl1_main_df[sample_volume][i])**2))**2)*1000)
            
            #Time difference between sampling datetime and read datetime (t1 in Garcia-Solsona)
            diff = pd.to_datetime(lvl1_main_df['Mid_Read_Datetime'][i]) - pd.to_datetime(lvl1_main_df['Mid_Sample_Datetime'][i]) 
            t1.append((diff.seconds/60)+diff.days*24*60)
            
        
    lvl1_main_df['blankcorr223'] = blankcorr219
    lvl1_main_df['blankcorr223_err'] = blankcorr219_err
    lvl1_main_df['blankcorr224'] = blankcorr220
    lvl1_main_df['blankcorr224_err'] = blankcorr220_err
    lvl1_main_df['dpm223'] = dpm219
    lvl1_main_df['dpm223_err'] = dpm219_err
    lvl1_main_df['dpm223_thstdonly'] = dpm219_thstdonly
    lvl1_main_df['dpm223_thstdonly_err'] = dpm219_thstdonly_err
    lvl1_main_df['dpm224'] = dpm220
    lvl1_main_df['dpm224_err'] = dpm220_err
    lvl1_main_df['vdpm223 (dpm/m^3)'] = vdpm219
    lvl1_main_df['vdpm223_err (dpm/m^3)'] = vdpm219_err
    lvl1_main_df['vdpm223_thstdonly (dpm/m^3)'] = vdpm219_thstdonly
    lvl1_main_df['vdpm223_thstdonly_err (dpm/m^3)'] = vdpm219_thstdonly_err
    lvl1_main_df['vdpm224 (dpm/m^3)'] = vdpm220
    lvl1_main_df['vdpm224_err (dpm/m^3)'] = vdpm220_err
    lvl1_main_df['t1_(mins)'] = t1
    lvl1_main_df['vdpm226 (dpm/m^3)'] = vdpm226
    lvl1_main_df['vdpm226_err (dpm/m^3)'] = vdpm226_err

    return(lvl1_main_df)








    
