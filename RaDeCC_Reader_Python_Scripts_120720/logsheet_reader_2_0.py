#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 15:27:09 2019

@author: seanselzer
"""
import pandas as pd
import os
import numpy as np


def logsheet_scan (folder_filepath, sample_variable):
    log_list = []
    for dirName, subdirList, fileList in os.walk(folder_filepath/'logsheet_folder'):
        for file in fileList:
            log_list.append(pd.read_csv(folder_filepath/'logsheet_folder'/file))
            
    log_df =  pd.concat(log_list, sort = False)
    log_df = log_df.sort_values(sample_variable, ascending = True)
    log_df.to_csv(folder_filepath/'Dataframes'/'Amalgamated_Logsheet.csv')     
    
    return(log_df)
    
