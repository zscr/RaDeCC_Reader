



#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________

"""
This script takes the the main deployment type and number of deployments as well as any other types of sample as specified in the radecc_main.py script. It then creates a library of folders (or directory)
for each type of deployment type and then each deployment within each type.

The script then searches the folder of all sample reads for each deployment. It then creates a new folder within each deployment folder for each depth (structure: sample_type>deployment>depth).
"""


import os, shutil
    

def dir_constructor(new_master_dir, log_df, sample_variable, sub_sample_variable, linear_data_type, folder_list):


    if os.path.exists(new_master_dir) == False:
        os.mkdir(new_master_dir)
    for folder_name in folder_list:
        if os.path.exists(new_master_dir/folder_name) == False:
            os.mkdir(new_master_dir/folder_name)
    for i in range(len(log_df)):
        # print (new_master_dir/'Read_Files'/log_df[sample_variable].iloc[i]/log_df[sub_sample_variable].iloc[i])
        if os.path.exists(new_master_dir/'Read_Files'/log_df[sample_variable].iloc[i]) == False:
            os.mkdir(new_master_dir/'Read_Files'/log_df[sample_variable].iloc[i])
        if linear_data_type == False:
            if os.path.exists(new_master_dir/'Read_Files'/log_df[sample_variable].iloc[i]/str(log_df[sub_sample_variable].iloc[i])) == False:
                os.mkdir(new_master_dir/'Read_Files'/log_df[sample_variable].iloc[i]/str(log_df[sub_sample_variable].iloc[i]))




