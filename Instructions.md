# RaDeCC Reader
## Version 1.0.0

This program calculates:
- Fully corrected dpm(223Ra)/1000 L and dpm(224Ra)/1000 L with propagated uncertainties
- Detector efficiencies (Using 227-Actinium and 228-Thorium Standards)
- Estimated dpm(226Ra)/1000 L (via the rate of 222Rn ingrowth)

Required input:
- RaDeCC system read files from samples, 227-actinium and 228-thorium standards and blanks (background measurements)
- Logsheet with sample collection metadata (as .txt files)
- User input to radecc_main.py 

## Prerequisites

Hardware Requirements: 2 x 64-bit 2.8 GHz 8.00 GT/s CPUs, 32 GB RAM (or 16 GB of 1600 MHz DDR3 RAM), 300 GB Storage. 

Written in Python 3.6 (Spyder 3.3.4), RaDeCC Reader (179 KB) is available on GitHub (https://github.com/oxradreader/RaDeCC_Reader)


## Installing Python (Anaconda)

Before running the program scripts you will need a way of running python on your computer. The easiest method is to install Anaconda Navigator which includes Spyder, a scientific python development environment. Downloads for Anaconda distributions can be found at the below link:

https://www.anaconda.com/download/

Once the Anaconda distribution is successfully installed, open 'Anaconda Navigator' and launch 'Spyder'.

Spyder is where you will open and run the RaDeCC Reader program.

**It is advised to run the program with the data in Raw_Data_Example first in order to check that the program itself is functioning properly.**


## Preparing Input Data

### Logsheet formatting

- Logsheets should be formatted such that each row represents a sample and each column a variable such as sample name, latitude, sample volume etc. (See Example_Logsheet.csv)
- Logsheets must be in a comma-separated value (.csv) format.
- Sample names in the loghsheet must match the sample names used in filenames.
- If using sub-sample names/values, those in the logsheet must match those in the filenames(e.g. individual sub-samples at different depths at a string of locations, each location being a sample, each depth being a sub-sample)


### File naming conventions
- For linear sample sets (e.g. 1-dimensional surface sampling), read file names need to follow the format: 
		
		[Read_Number]-[Sample]-[Cartridge_Type]-[Date]-[Detector_Name].txt

	- [Read_Number] : Usually 1-4 this indicates whether it is a first, second, third or fourth read.
	- [Sample] : this is the name of your sample, e.g. StnX001 (N.B. samples need to be numbered 001-999 e.g. StnX001 to StnX999)
	- [Cartridge_Type] : When sampling with two MnO-fibres in series in order to calculate scavenging efficiency, the first MnO-fibre in the series may be the 'A' fibre and the second the 'B' fibre.
	- [Date] : this is the date of this particular read of this sample in DDMMYY or MMDDYY form, it cannot contain any punctuation e.g.(/.,-)
	- [Detector_Name] : this is the name of the detector used for this particular read of this sample.
	
	For example:
		
		 1-StnX042-250119-detector1.txt


	- For sample sets that contain sub-samples (e.g. multiple depth profiles creating a 2-dimensional transect), sample read file names need to follow the format:
	
		[read_number]-[Sample]-[Sub-Sample][Cartridge_Type]-[Date]-[Detector_Name].txt

	- [Read_Number] : Usually 1-4 this indicates whether it is a first, second, third or fourth read.
	- [Sample] : this is the name of your sample, e.g. StnX001 (N.B. samples need to be numbered 001-999 e.g. StnX001 to StnX999)
	- [Sub-Sample] : this is the name of the sub sample, for example if one sample contains a number of sub-samples at different depths or times this could be the sub-sample depth or time. These values or names should match those in the logsheet(s)
	- [Cartridge_Type] : When sampling with two MnO-fibres in series in order to calculate scavenging efficiency, the first MnO-fibre in the series may be the 'A' fibre and the second the 'B' fibre.
	- [Date] : this is the date of this particular read of this sample. the format of this date is flexible but cannot contain any punctuation e.g.(/.,-)
	- [Detector_Name] : this is the name of the detector used for this particular read of this sample.
	
	For example:
	
		 1-StnX042-1700A-250119-detector1.txt
	
	- For 227-actinium standard, 228-thorium standard and blank reads, the following file name format must be followed:

		[Standard_or_Blank_Type]-[Date]-[Detector_Name].txt

		- [Standard_or_Blank_Type] : this is the name of the standard or blank cartridge ( e.g 228-thorium standard = thstd, 227-actinium standard = acstd and blank = blank)
		- [Date] : this is the date of this particular read of this sample. the format of this date is flexible but cannot contain any punctuation e.g.(/.,-)
		- [Detector_Name] : this is the name of the detector used for this particular read of this sample.

	For example:
	
		 thstd-250119-detector1.txt
	  	


In order to place the data where the program can find it:

1. Create a main project folder, this will contain the raw data folder, the program scripts folder ond the output folder.
	Filepath (MacOS): /Users/username/Desktop/Project_X

2. Create a folder within the main project folder (/Users/username/Desktop/Project_X) for the raw data and place all logsheets as well as standard, blank and sample reads here.
	e.g. Filepath: /Users/username/Desktop/Project_X/Raw_Data_Example
	
3. Copy and paste the RaDeCC_Reader_Scripts folder into the main project folder (Filepath: /Users/username/Desktop/Project_X).
	e.g. Filepath: /Users/username/Desktop/Project_X/RaDeCC_Reader_Scripts

You should now have the following folder structure:

Filepath: /Users/username/Desktop/Project_X
Filepath: /Users/username/Desktop/Project_X/Raw_Data_Example
Filepath: /Users/username/Desktop/Project_X/RaDeCC_Reader_Scripts


# User Input to radecc_main.py

Open Anaconda Navigator  and launch Spyder. Once Spyder is running open radecc_main.py. Follow the below guide on user input within this file.

**Important**: Ensure there are no spaces anywhere in the filepaths used for *input_directory* or *output_directory*
- *input_directory*: This is the filepath of the folder in which the sample, standard and blank read files as well as logsheets were placed 
	
	For Example: 
		
		Filepath (Linux, OS X): /Users/username/Desktop/Project_X/Raw_Data_Example
		Filepath (Windows): C:\\Users\\username\\Desktop\\Project_X\\Raw_Data_Example

- *output_directory*: This is filepath of the folder in which you would like the output to be placed.
	
	For Example: 
		
		Filepath (Linux, OS X): /Users/username/Desktop/Project_X/Output_Data
		Filepath (Windows): C:\\Users\\username\\Desktop\\Project_X\\Output_Data

- *output_filename* : the name you would like to give the ouput file.
	
	For Example:
		
		project_x_output.csv

- *linear_data_type* : This variable is set to True if the dataset being input is linear/1-dimensional (e.g. a string of ocean surface samples or a time series at one point/location). Alternatively this is set to False if the dataset being input is 2-dimensional (e.g. a time-series at a string of locations or a string of depth profiles).
	**Note**
	This variable should be set as either of the below:
		
	- linear_data_type = True
	- linear_data_type = False
	
	Not:
	- linear_data_type = 'True'
	- linear_data_type = 'False'	

## Electrical spike detection and removal
The RaDeCC_Reader program is able to find spikes in read data that are anomalous (often due to a surge in the electrical supply to the RaDeCC detector). If a spike is found, it is removed and so is not included in the correction and error propagation calulcations that follow. The threshold that determines whether a spike is anomalous is set by the variable *spike_sensitivity*. This variable is set to 100 by default, meaning that if the number of counts in any time interval is more than 100 counts higher than the previous time interval it is deemed a spike and removed from calculations. To disable this function set *spike_sensitivity* = 1000.

- *spike_sensitivity* : The threshold of counts in a time interval that determines whether a spike is anomalous or not.

## Information for the directory builder

- *sample_type*: This is the sample naming convention e.g. if your first sample is sample001 and your second is sample002 then sample_type is 'sample'
- *number_of_samples*: The is the number of samples (1-999).

## Information for the detector efficiency calculations

- *thstd*: This is the filename identifier for Thorium-228 standards e.g. 'thstd' in the filename 'thstd-250119-detector1.txt'
- *acstd*: This is the filename identifier for Actinium-227 standards e.g. 'acstd' in the filename 'acstd-250119-detector1.txt'
- *blank*: This is the filename identifier for blank standards e.g. 'blank' in the filename 'blank-250119-detector1.txt'
- *acstd_activity*: This is the start activity of the actinium-227 standard at the date of preparation
- *thstd_activity*:	This is the start activity of the thorium-228 standard at the date of preparation
- *ac_halflife*: This is the half-life of actinium-227
- *thstd_prepDatestr* = date and time of thorium-228 standard preparation in the form - 'dd/mm/yyyy hh:mm:ss'
- *acstd_prepDatestr* = date and time of actinium-227 standard preparation in the form - 'dd/mm/yyyy hh:mm:ss'
- *det_list* =  list of detectors in the form - ['detector_1', 'detector_2', ..., 'detector_n']

#Logsheet identifiers (below)

These are the row names used in the logsheet for each variable (e.g. Latitude may be abbreviated in the logsheet to 'Lat'). These are used by the programme to search for the relevant data
in the logsheet.

e.g.

- *sample_mid_time* = 'Time Bot'
- *sample_variable* = 'StnX'	
- *sub_sample_variable* = 'Sample_Depth'
- *sample_volume* = 'Volume_sampled'

The program should now be ready to run. With radecc_main_2_1.py open in Spyder 3.3.4, click run (green triangle).

## Output from radecc_main.py

### While the program runs there will be some output to the terminal (or console). The program will notify the user via the terminal in the following events

- If a directory that the program is trying to create already exists, the program will not overwrite the existing directory and notify the user via the terminal
- After the files have been copied from the source directory(source_dir) to the newly constructed original directory (original_dir), the program will report the number of files not copied (should be 0)
- If a spike ( when the *spike_sensitivity* is exceeded in either the 219 or 220 channel) is detected in a readfile, that interval is removed and the summary values are calculated without them. The user is notified via the terminal or console as well as in the .csv file contain the output results
- If there are not enough data points to find a slope for 222Rn ingrowth. The user is notified



##The program will also output the following files in .csv format

###Dataframes (Found in the Dataframes Folder)
- A main table (.csv format) containing all metadata from logsheets as well as values for each level of the Garcia-Solsona corrections and uncertainty propagations, ending with dpm/1000L for both 223Ra and 224Ra as well as an estimation of 226Ra based on 222Rn ingrowth. All this is displayed for each read of each sample, ready for easy data-manipulation in Microsoft Excel.
- A summary table of detector efficiencies. 
- A table of efficiencies for each channel, detailing the efficiency calculated for each standard read.
- An output logsheet, the amalgamation of all input logsheets.
###Plots (Found in the Read_Plots Folder)
- A plot of counts per minute for the total, radon-219 and radon-220 channels over the course of each read. Spikes in counts per minute (any counts that exceeded the default spike_sensitivity constant) have been removed. 




## Authors

* **Sean Selzer** - (https://github.com/Rad-Reader)
* **Amber L. Annett**
* **William B. Homoky**

## License

MIT

## Acknowledgments

The authors gratefully acknowledge support from the UK’s Natural Environment Research Council who funded S.S. through the Environmental Research Doctoral Training Partnership with University of Oxford, and A.L.A. and W.B.H. through Independent Research Fellowships (NE/P017630/1 and NE/K009532/1).