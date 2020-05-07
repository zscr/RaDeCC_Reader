



#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________

"""
This script takes the the main deployment type and number of deployments as well as any other types of sample as specified in the radecc_main.py script. It then creates a library of folders (or directory)
for each type of deployment type and then each deployment within each type.

The script then searches the folder of all sample reads for each deployment. It then creates a new folder within each deployment folder for each depth (structure: sample_type>deployment>depth).
"""


import os, shutil
from deployment_lister import *
from file_searcher import *
    

def dir_constructor(output_directory, new_master_dir, sample_type, number_of_samples, deployment_dir_list):

    #Original Unsorted folder of files: output_directory 

    #Location of new sorted library of files: new_master_dir 

    #Read original unsorted folder into list called 'directory'
    directory = os.listdir(output_directory)

    #Change directory so that we are now operating in the original unsorted folder
    os.chdir(output_directory)
    
    #Create the new master directory if it doesn't already exist
    if os.path.exists(new_master_dir) == False:
        os.mkdir(new_master_dir)
    
    #Create new directory within the new master directory for each member of deployment_dir_list:
    for deployment in deployment_dir_list:
        if os.path.exists(new_master_dir/(deployment+'_folder')) == False:
            os.mkdir(new_master_dir/(deployment+'_folder'))

    #If the directory already exists, return message stating this rather than overwriting an existing directory
        if os.path.exists(new_master_dir/(deployment+'_folder')) == True:
            print ('Directory exists: ', new_master_dir/(deployment+'_folder'))
            
    saps_list = deployment_lister(sample_type, number_of_samples)

    #For each deployment in the newly created list, search through each directory entry for the deployment name, if this is found then extract the depth
    #and append to a list of depths for that deployment
    for deployment in saps_list:

        depth_list = []
        search_str = deployment
        for i in range (len(directory)):								
            temp_string = directory[i].lower()									
            for j in range(len(temp_string)-1):	
                if search_str.lower() in temp_string:
                    split_list = directory[i].split('-')
                    if len(split_list) >=3:
                        
                        #print (split_list)
                        str_list = list(split_list[2])
                        str_list2 = []
                        #for i in range(len(str_list)):
                            #if str_list[i].isdigit():
                                #str_list2.append(str_list[i])
                        depth_list.append(''.join(str_list))

    #Turn the depth list into a set to get rid of duplicates	
        depth_set = set(depth_list)
        #print (depth_set)

    #Create a new directory within the deployment directory for each depth, unless this directory already exists, in which case print message explaining this
        for depth in depth_set:
            if os.path.exists(new_master_dir/(sample_type+'_folder')/deployment) == False:
                os.mkdir(new_master_dir/(sample_type+'_folder')/deployment)
            if os.path.exists(new_master_dir/(sample_type+'_folder')/deployment) == True:
                print ('Directory exists: ', new_master_dir/(sample_type+'_folder')/deployment)
        
            if os.path.exists(new_master_dir/(sample_type+'_folder')/deployment/depth.lower()) == False:
                os.mkdir(new_master_dir/(sample_type+'_folder')/deployment/depth.lower())
            if os.path.exists(new_master_dir/(sample_type+'_folder')/deployment/depth.lower()) == True:
                print ('Directory exists: ', new_master_dir/(sample_type+'_folder')/deployment/depth.lower())



