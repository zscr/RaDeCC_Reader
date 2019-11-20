#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:36:13 2018

@author: seanselzer
"""
def deployment_lister(deployment_type, number_of_deployments):
    deployment_list = []
    #Create list of main deployment names based on no. of deployments variable:
    for i in range(number_of_deployments+1):
        if 0<i<10:
            deployment_list.append(deployment_type+'00'+str(i))
        if 100>i>=10:
            deployment_list.append(deployment_type+'0'+str(i))
        if i>=100:
            deployment_list.append(deployment_type+str(i))
    return (deployment_list)

