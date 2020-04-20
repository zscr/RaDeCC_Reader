



#__________________________________________________________________________________________________________________________________________________________
"""Working Code, Do Not Change"""
#__________________________________________________________________________________________________________________________________________________________

"""
This function takes directory tree generated by dir_constructor_v2 and searches the folder containing all the reads (copyDir) for each deployment type, deployment number and depth, populating
each folder with the corresponding reads.

At the end it compares the list of files in the copyDir with a list of files that have been copied to see if any have been left out. It then prints the number of files that were left out or
not copied.
"""



# Import the os module, for the os.walk function
import os, shutil
from pathlib import Path
from get_digits import *
from file_searcher import *

def dir_filler_linear(rootDir, copyDir, sample_type, acstd_date_dict, thstd_date_dict, blank_name_list):

    #Extract name of new directory e.g. 'FRidge_Beta'
    rootsplit = rootDir.parts
    rootname = rootsplit[-1]

    #Create list objects
    dir_list = []
    test_filelist = []

    #Fill fileList_copy with all the files in the directory to be copied (copyDir)
    for dirName, subdirList, fileList in os.walk(copyDir):
        fileList_copy = fileList
        #print(fileList_copy)
        #print (dirName)



    #dir_list = []
    for dirName, subdirList, fileList in os.walk(rootDir):
	
        #For each directory name in rootDir split the directory name string into list using '/' as a separator	
        dirName_split = Path(dirName).parts
        dirName_splitsplit = dirName_split[-1].split('_')
       # print (dirName_splitsplit)
        #If the second last dirName_split list entry starts with rootname and the last entry in the list does not start with sample type: 
        if dirName_split[-2][:len(rootname)]==rootname and sample_type not in dirName_split[-1].lower():
            #print (dirName_split[-2][:len(rootname)], sample_type)

        #For each filename in fileList_copy, convert to all lowercase letters, then search this filename for each directory name. When there is a match,
        #copy the file with that filename from copyDir to the new directory in rootDir and append test_filelist.
            for fname in fileList_copy:
                search_str=fname.lower()
                #print (search_str)
                if dirName_splitsplit[0].lower() in search_str.lower() and sample_type.lower() not in search_str:
                    #print (dirName_splitsplit,search_str, sample_type)
                    test_filelist.append(fname)
                        
                    
                    if (rootDir/dirName/fname).exists()==False:
                        #print (fname)
                        shutil.copy(str(copyDir/fname), str(rootDir/dirName/fname))

#############################################################################################################################
                        '''Acstd mod'''
#############################################################################################################################
                        
                for standard_name in acstd_date_dict.keys():
                    
                    if standard_name.lower() in search_str:
#                        print ( str(rootDir/'acstd_folder'/fname))
                        
                        test_filelist.append(fname)
                        
                    
                        if (rootDir/'acstd_folder'/fname).exists()==False:
                            #print (fname)
                            shutil.copy(str(copyDir/fname), str(rootDir/'acstd_folder'/fname))
#############################################################################################################################
#############################################################################################################################
                        '''Thstd mod'''
#############################################################################################################################
                        
                for standard_name in thstd_date_dict.keys():
                    
                    if standard_name.lower() in search_str:
#                        print ( str(rootDir/'acstd_folder'/fname))
                        
                        test_filelist.append(fname)
                        
                    
                        if (rootDir/'thstd_folder'/fname).exists()==False:
                            #print (fname)
                            shutil.copy(str(copyDir/fname), str(rootDir/'thstd_folder'/fname))
#############################################################################################################################
#############################################################################################################################
                        '''Blank mod'''
#############################################################################################################################
                        
                for standard_name in blank_name_list:
                    
                    if standard_name.lower() in search_str:
#                        print ( str(rootDir/'acstd_folder'/fname))
                        
                        test_filelist.append(fname)
                        
                    
                        if (rootDir/'blank_folder'/fname).exists()==False:
                            #print (fname)
                            shutil.copy(str(copyDir/fname), str(rootDir/'blank_folder'/fname))
#############################################################################################################################
                            
        if sample_type.lower() in dirName_split[-2].lower() and sample_type.lower() in dirName_split[-1].lower():
            #print (dirName_split[-1])

            
            #For each filename in the list of files to copy: convert filename to lowercase 	
            for fname in fileList_copy:  
                search_str=fname.lower()
                #print (search_str)
                    
                #then search this for dirName_split[2](deployment name)	
                if dirName_split[-1].lower() in search_str.lower():
                    test_filelist.append(fname)
                    
                    if (rootDir/dirName/fname).exists()==False:
                        
                        shutil.copy(str(copyDir/fname), str(rootDir/dirName/fname))
                        print (str(copyDir/fname), str(rootDir/dirName/fname))
                    
                            
        
        
    #Compare list of all files copied so far and the original list to copy, make a new list of all files not yet copied.
    a = set(fileList_copy)
    b = set(test_filelist)
    set_diff = a-b
    if '.DS_Store' in set_diff:
        set_diff.remove('.DS_Store')
    
    print ('\nNumber of files going into misc_folder: ',len(set_diff))
    #Copy each file in this list to the misc folder in rootDir and add filename to test_filelist. This will catch any files that don't fall into the other folders ensuring that
    #all files get copied
    for f in set_diff:
        test_filelist.append(f)
        if os.path.exists(rootDir/'misc_folder'/f)==False:
            shutil.copy(copyDir/f,rootDir/'misc_folder'/f)
            

    #Compare 'copied files' with 'files to copy' again to check that there are none left. set_diff should be an empty set now.
    a = set(fileList_copy)
    b = set(test_filelist)
    set_diff = a-b	
    if '.DS_Store' in set_diff:
        set_diff.remove('.DS_Store')

    #Display length of the set_diff set which should be zero if all the 'files to be copied' have been copied to the new directory
    print ('Number of files not copied:', len(set_diff))

#dir_filler('/Users/seanselzer/Documents/FRidge_data_mac/FRidge_Beta', '/Users/seanselzer/Documents/FRidge_data_mac/FRidge_2')



