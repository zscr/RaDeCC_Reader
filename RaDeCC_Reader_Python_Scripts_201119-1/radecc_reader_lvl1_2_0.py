



#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________

"""
This script reads the raw data from the RaDeCC text (.txt) files and the performs corrections and uncertainty propagations described by
Garcia-Solsona et al. (2008) (Marine Chemistry, 109, pp. 198-219) in order to quantify 223Ra and 224Ra. It also calculates the slope of
total counts per minute for later estimation of 226Ra via 222Rn ingrowth (Geibert et al. (2013), Limnol. Oceanogr. Methods, 11).
The input is a RaDeCC read file.
The output is a list of numbers, strings and lists including final CPMs and associated metadata.
"""


import os
import scipy.stats as sci
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from pathlib import Path
from get_digits import *

def interval_calculator (list_, runtime):					#This finds the counts within each interval. The range is length of list -1 as the last
    list1 = []										        #value of each list is the summary value. This is excluded by using (len(list_)-1)
    for i in range (len(list_)-1):
        if i == 0:
            list1.append(list_[i]/(runtime[i]-0))
        else:
            list1.append(list_[i]/(runtime[i]-runtime[i-1]))
    return (list1)

def cc_calculator (list1, list2, list3, cc_value):	#calculates channel corrections
    listx = []
    for i in range (len(list1)):
        listx.append((((list1[i] - list2[i] - list3[i])**2)*cc_value)/(1-((list1[i] - list2[i] - list3[i])*cc_value)))
    return (listx)

def slope_calculator (output_directory, arg_file = None, spike_sensitivity = 100, equilibration_time_variable = 0, DDMMYYY_DateFormat = True, thstd = 'thstd', acstd = 'acstd', blank = 'blank'):
    runtimecopy = []
    CPM219copy = []
    cnt219copy = []
    CPM220copy = []
    cnt220copy = []
    CPMTotcopy = []
    cntTotcopy = []
    runtime = []
    CPM219 = []
    cnt219 = []
    CPM220 = []
    cnt220 = []
    CPMTot = []
    cntTot = []
    spike_list = []
    
    file_name = arg_file
    spike = 0
    
    #print (file_name)
    #Open txt file
    f = open(file_name, 'r')
    print (file_name)

    with open (file_name) as f:
        
#_________________________________________________________________________________________________________________________________________________												
#RAW [RUNTIME, CPM219, cnt219, CPM220, cnt220, CPMTot, cntTot]____________________________________________________________________________________

        for line in f:
            line = line.replace('"','')
            if line[0] == '0'or line[0] == '1':						#Find lines containing data rather than titles
                x = line.split()                                    #Split data within each line#Split data within each line#Split data within each line
                runtimecopy.append(float(x[0]))			            #Append data to appropriate variable lists
                CPM219copy.append(float(x[1]))
                cnt219copy.append(int(x[2]))
                CPM220copy.append(float(x[3]))
                cnt220copy.append(int(x[4]))
                CPMTotcopy.append(float(x[5]))
                cntTotcopy.append(float(x[6]))
                
                
        
#_______________________________________________________________________________________________________________________________________________
#START DATETIME_________________________________________________________________________________________________________________________________
            # Find and extract the start date and time of the read from the radecc read file
            if line[0:5] == 'Start':
                date_time = pd.to_datetime(line [10:], dayfirst = DDMMYYY_DateFormat)
        
        #Find and remove spikes in counts (here a spike is defined by a count that is more than 100 counts higher than the last count period as default)      
        for i in range (len(cntTotcopy)):
            if (cnt219copy[i]-cnt219copy[i-1])>spike_sensitivity or (cnt220copy[i]-cnt220copy[i-1])>spike_sensitivity or (cntTotcopy[i]-cntTotcopy[i-1])>spike_sensitivity:
                if i != len(runtimecopy) - 1:
                    print ('Spike detected and removed in file:',arg_file,'\ncnt219 cnts',cnt219copy[i],'\ncnt220 cnts',cnt220copy[i],'\ntot cnts :', cntTotcopy[i])
                    spike = cntTotcopy[i]
            else:
                runtime.append(runtimecopy[i])
                CPM219.append(CPM219copy[i])
                cnt219.append(cnt219copy[i])
                CPM220.append(CPM220copy[i])
                cnt220.append(cnt220copy[i])
                CPMTot.append(CPMTotcopy[i])
                cntTot.append(cntTotcopy[i])
         
        f.close()
#________________________________________________________________________________________________________________________________________________
#END DATETIME____________________________________________________________________________________________________________________________________	
    #calculate the end date and time of the read by adding the read-time to the start datetime
    end_date_time = date_time + datetime.timedelta(minutes = runtime[-1])
          
#________________________________________________________________________________________________________________________________________________
#CPM220,CPM219,CPMTot for each 10 min time interval______________________________________________________________________________________________	
    #Calculate the counts per minute (CPM) for each time period (interval) for each channel, using interval_calculator
    CMP219_interval = interval_calculator(cnt219, runtime)		
    CMP220_interval = interval_calculator(cnt220, runtime)
    CMPTot_interval = interval_calculator(cntTot, runtime)

#________________________________________________________________________________________________________________________________________________
#CHANNEL CORRECTIONS ON EACH INTERVAL____________________________________________________________________________________________________________


    y_220_cc = cc_calculator(CMPTot_interval, CMP220_interval, CMP219_interval, 0.01)		#220 channel correction (value = 0.01)

    CMP220_corr = []
    for i in range (len(CMP220_interval)):													#Find corrected 220 cpm
        CMP220_corr.append(CMP220_interval[i] -y_220_cc[i])
        #print (y_220_cc[i], CMP220_corr[i])
        
    y_219_cc = cc_calculator(CMPTot_interval, CMP220_corr, CMP219_interval, 0.0000935)		#219 channel correction (value = 0.0000935)

    CMP219_corr = []
    for i in range (len(CMP219_interval)):
        CMP219_corr.append(CMP219_interval[i]-y_219_cc[i])		                            #Find corrected 219 cpm

    CPM220_final = []
    for i in range (len(CMP219_corr)):
        CPM220_final.append(CMP220_corr[i] - ((((1.65*CMP219_corr[i])**2)*0.01)/(1-((1.65*CMP219_corr[i])*0.01))))	#Find Final 220 cpm
    
    CPM219_final = []
    for i in range(len(CMP219_corr)):
        CPM219_final.append(CMP219_corr[i] - (CMP220_corr[i] * 0.0255))                     #Find final 219CPM (corrected 219 cpm    - (CMP220_corr[i] * 0.0255))
    #print (np.average(y_219_cc))
        
    CPMTot_corr = []
    for i in range(len (CMPTot_interval)):
        CPMTot_corr.append(CMPTot_interval[i] - 2*CPM220_final[i] - 2*CPM219_final[i])      #Find corrected Total CPM

    #print (arg_file)
#________________________________________________________________________________________________________________________________________________
#CALCULATE LINEAR REGRESSION OF CPMTot_corr______________________________________________________________________________________________________
    if thstd in file_name.parts or acstd in file_name.parts or blank in file_name.parts:
        if len(runtime[:-1]) == len(CPMTot_corr[:]) and len(CPMTot_corr[:])>3:
            slope = sci.linregress(runtime[:-1], CPMTot_corr[:])
        else:
            print ('\n***ERROR***\nThe read file ',arg_file,'does not contain enough data points to perform a linear regression: 222Rn ingrowth slope set to 999\n')
            slope = [999,999,999,999,999]
    else:
        if len(runtime[equilibration_time_variable:-1]) == len(CPMTot_corr[equilibration_time_variable:]) and len(CPMTot_corr[equilibration_time_variable:])>3:
            slope = sci.linregress(runtime[equilibration_time_variable:-1], CPMTot_corr[equilibration_time_variable:])
        else:
            print ('\n***ERROR***\nThe read file ',arg_file,'does not contain enough data points to perform a linear regression: 222Rn ingrowth slope set to 999\n')
            slope = [999,999,999,999,999]

#________________________________________________________________________________________________________________________________________________
#Propagation of Uncertainties___________________________________________________________________________________________
    
    if  np.sum(cnt219[:-1]) == 0:
        err_219 = 0
    if  np.sum(cnt219[:-1]) != 0:
        err_219 = np.sqrt(np.sum(cnt219))/np.sum(cnt219)				#[-1] index is the final list value which is the summary line in the txt file
        
    if  np.sum(cnt220[:-1]) == 0:
        err_220 = 0
    if  np.sum(cnt220[:-1]) != 0:
        err_220 = np.sqrt(np.sum(cnt220))/np.sum(cnt220)
        
    
    err_Tot = np.sqrt(np.sum(cnt220))/np.sum(cnt220)
    
    cpm_219 = np.sum(cnt219)/runtime[-1]
    
    cnt219_abserr = err_219*cpm_219
    
    cpm_220 = np.sum(cnt220)/runtime[-1]
    cnt220_abserr = err_220*cpm_220
    
    cpm_Tot = np.sum(cntTot)/runtime[-1]
    cntTot_abserr = err_Tot*cpm_Tot
    
    y_ = (cpm_Tot-cpm_220-cpm_219)
   
    
    y219cc = ((y_**2)*0.000093)/(1-(y_*0.000093))
    
    y220cc = ((y_**2)*0.01)/(1-(y_*0.01))

    
    y_err = (np.sqrt((cntTot_abserr)**2+(cnt220_abserr)**2+(cnt219_abserr)**2))
    
    y219cc_err = y_err*(((2*0.000093*y_)-(0.000093*y_)**2)/(1-0.000093*y_)**2)
    
    y220cc_err = y_err*(((2*0.01*y_)-(0.01*y_)**2)/(1-0.01*y_)**2)
    
  
    corr219 = cpm_219 - y219cc
    corr219_err = np.sqrt(cnt219_abserr**2 +y219cc_err**2)
    
    
    corr220 = cpm_220 - y220cc
    
    corr220_err = np.sqrt(cnt220_abserr**2 +y220cc_err**2)
    
    
    
    final219 = corr219 - (corr220*0.0255)
    final219_err = np.sqrt(corr219_err**2 + (0.0255*corr220_err)**2) 
      
    
    final220 = corr220 - ((1.6*corr219)**2 * 0.01)/(1 + ((1.6*corr219)*0.01))
    
    final220_err = np.sqrt(corr220_err**2 + ((((2*1.6)**2 *0.01*corr219-(1.6**3 * 0.01**2 * corr219**2))/(1-(1.6*0.01*corr219))**2)*corr219_err)**2)
    
    
#________________________________________________________________________________________________________________________________________________
#cnttotnet____(= cntTot - 2*cnt219 - 2*cnt220)___________________________________________________________________________________________________

    cnttotnet = cntTot[-1] - 2*cnt219[-1] - 2*cnt220[-1]
#________________________________________________________________________________________________________________________________________________
#erslope_abs_(errslope_rel currently set at 20%)_________________________________________________________________________________________________
    errslope_rel = slope[4]
    errslope_abs = slope[4]/slope[0]
    #print (slope[0], slope[4]/slope[0], errslope_rel)
#________________________________________________________________________________________________________________________________________________
#Detector Name (detname), Cartridge type, Read Number_________________________________________________________________________________________________
    
    tempname=arg_file.parts
    tempname2 = tempname[-1].split('-')
    cart_type = tempname2[-3][-1].lower()
    
    #find detector name
    tempname3=tempname2[-1].split('.')
    detname=tempname3[0].lower()   
    
    #find read number
    read_number = get_digits(tempname2[0])
    
    
    
    
    base_dir = output_directory/'Read_Plots'
    #print (base_dir)
    
    
    sample_dir = Path(os.path.join(*arg_file.parts[-4:-1]))
    
    
    if sample_dir.parts[-1].split('_')[-1] == 'folder':
        sample_dir = Path('Standards_and_Blanks')/sample_dir.parts[-1]
    
    
    
    read_name = arg_file.parts[-1].split('.')[0]
    #print (sample_dir)
    
    
    if (base_dir/(str(sample_dir)+'_plots')).exists() == False:
        os.makedirs(base_dir/(str(sample_dir)+'_plots'))
        
    
    if (base_dir/sample_dir/read_name).exists() == False:
        
        
        #fig = plt.figure()
        ax = plt.subplot(111)
        
        ax.plot(runtime[:-1], CPMTot_corr[:], '-')
        ax.scatter(runtime[:-1], CPMTot_corr[:], label = 'Total CPM')
        
        if len(runtime[equilibration_time_variable:-1]) == len(CPMTot_corr[equilibration_time_variable:]) and len(CPMTot_corr[equilibration_time_variable:])>3:
        
            ax.plot(runtime[0:equilibration_time_variable], CPMTot_corr[0:equilibration_time_variable], '-')
            ax.scatter(runtime[0:equilibration_time_variable], CPMTot_corr[0:equilibration_time_variable], label = 'Total CPM (Equilibration Time)')
        
        ax.plot(runtime[:-1], CPM220_final[:], '-')
        ax.scatter(runtime[:-1], CPM220_final[:], label = '220 CPM')
        
        ax.plot(runtime[:-1], CPM219_final[:], '-')
        ax.scatter(runtime[:-1], CPM219_final[:], label = '219 CPM')
        
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2)
        
        plt.title(read_name)
        plt.xlabel('Read Time (mins)')
        plt.ylabel('Counts per minute (cpm)')
        plt.savefig(base_dir/(str(sample_dir)+'_plots')/read_name, dpi = 250, bbox_inches = 'tight')
        #plt.show()
        plt.clf()
        
    cnt219, cnt219_abserr, cnt220, cnt220_abserr, cpm_219, err_219, cpm_220, err_220, cpm_Tot, err_Tot, y219cc, y219cc_err, y220cc, y220cc_err, corr219, corr219_err, corr220, corr220_err,

    if runtime[-1] > 10.0:
        return (date_time, end_date_time, slope[0], slope[4], sum(cnt219), cnt219_abserr, sum(cnt220), cnt220_abserr, cpm_219, err_219, cpm_220, err_220, cpm_Tot, err_Tot, y219cc, y219cc_err, y220cc, y220cc_err, corr219, corr219_err, corr220, corr220_err,  final219, final220, runtime[-1], final219_err, final220_err, cntTot_abserr, errslope_abs, detname, cart_type, read_number, spike)
    else:
        return (pd.to_datetime('01/01/1900 00:00:00'), pd.to_datetime('01/01/1900 00:00:00'), -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, 'no_read', 'no_read', -999, -999)
 
    
    
	
	
"""Below used for testing/debugging"""	
#slope_calc_list = slope_calculator('/Users/seanselzer/Desktop/RaDeCC-Reader_2/FRidge_Beta', "/Users/seanselzer/Desktop/RaDeCC-Reader_2/FRidge_beta/saps_folder/saps002/1500m/1-Saps002-1500A-170105-HE.txt", 100, 0)
#slope_calc_list = slope_calculator('/Users/seanselzer/Desktop/RaDeCC-Reader_2/FRidge_Beta', "/Users/seanselzer/Desktop/RaDeCC-Reader_2/FRidge_Beta/thstd_folder/thstd-180524-bw.txt", 100, 0)
#print (slope_calc_list)
#print ('\nSlope: ',slope_calc_list[2], '\nR: ', slope_calc_list[3], '\ndetname: ', slope_calc_list[-1])
#cnt219, cnt219_abserr, cnt220, cnt220_abserr, cpm_219, err_219, cpm_220, err_220, cpm_Tot, err_Tot, y219cc, y219cc_err, y220cc, y220cc_err, corr219, corr219_err, corr220, corr220_err,

	