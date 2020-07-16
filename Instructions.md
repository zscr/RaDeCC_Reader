# RaDeCC Reader
## Version 2.0.0

This program calculates:
- Fully corrected dpm(223Ra)/1000 L and dpm(224Ra)/1000 L with propagated uncertainties for each read
- Excess radium-223 and excess radium-224 activities for each sample
- Supporting thorium-228 and actinium-227 for each sample
- Estimated dpm(226Ra)/1000 L (via the rate of 222Rn ingrowth)
- Detector efficiencies (Using 227-Actinium and 228-Thorium Standards)


Required input:
- RaDeCC system read files from samples, thorium-228 standard and blanks (background measurements). Actinium-227 standards are optional as 219-channel efficiency can also be determined via 220-channel efficiency.
- Logsheet with sample collection metadata (as .txt files)
- User input via the Graphical User Interface (GUI) 

## Prerequisites

Hardware Requirements: 2 x 64-bit 2.8 GHz 8.00 GT/s CPUs, 32 GB RAM (or 16 GB of 1600 MHz DDR3 RAM), 300 GB Storage. 

Written in Python 3.6, RaDeCC Reader (235.7 MB) is available on GitHub (https://github.com/oxradreader/RaDeCC_Reader)


**It is advised to run the program with the data in Raw_Data_Example first in order to check that the program itself is functioning properly.**


## Preparing Input Data

### Logsheet formatting

- Logsheets should be formatted such that each row represents a sample and each column a variable such as sample name, latitude, sample volume etc. (See Example_Logsheet.csv)
- Logsheets must be in a comma-separated value (.csv) format.
- Sample names in the loghsheet must match the sample names used in filenames.
- If using sub-sample names/values, those in the logsheet must match those in the filenames(e.g. individual sub-samples at different depths at a string of locations, each location being a sample, each depth being a sub-sample)

**IMPORTANT: Sample/sub-sample names must be unique to each sample/sub-sample and a sample/sub-sample name must not be contained within another sample/sub-sample name (e.g. 'sample2' can be found within 'sample20')**


### File naming conventions
- For linear sample sets (e.g. 1-dimensional surface sampling), read file names need to follow the format (addition details such as date or read number can be included but will not be used by the program): 
		
		[Sample]-[Detector_Name].txt
	
	- [Sample] : this is the name of your sample, e.g. StnX001 (N.B. samples need to be numbered 001-999 e.g. StnX001 to StnX999)
	- [Detector_Name] : this is the name of the detector used for this particular read of this sample.
	
	For example:
		
		 StnX042-detector1-250119.txt


	- For sample sets that contain sub-samples (e.g. multiple depth profiles creating a 2-dimensional transect), sample read file names need to follow the format:
	
		[Sample]-[Sub-Sample]-[Detector_Name].txt


	- [Sample] : this is the name of your sample, e.g. StnX001 (N.B. samples need to be numbered 001-999 e.g. StnX001 to StnX999)
	- [Sub-Sample] : this is the name of the sub sample, for example if one sample contains a number of sub-samples at different depths or times this could be the sub-sample depth or time. These values or names should match those in the logsheet(s)
	- [Detector_Name] : this is the name of the detector used for this particular read of this sample.
	
	For example:
	
		 StnX042-1700A-detector1-250119.txt
	
	- For 227-actinium standard, 228-thorium standard and blank reads, the following file name format must be followed:

		[Standard_or_Blank_Type]-[Detector_Name].txt

		- [Standard_or_Blank_Type] : this is the name of the standard or blank cartridge ( e.g 228-thorium standard = thstd, 227-actinium standard = acstd and blank = blank)
		- [Detector_Name] : this is the name of the detector used for this particular read of this sample.

	For example:
	
		 thstd-detector1.txt
	
	The addition of dates to filenames is advisable in order to differentiate them. In this case add dates to file names without spaces or slashes.

## Downloading RaDeCC_Reader

- The RaDeCC_Reader application can be found on the 'Releases' page of the RaDeCC_Reader repository (https://github.com/oxradreader/RaDeCC_Reader/releases)
- Each release includes:
	1.  RaDeCC_Reader_OS_vX_X.zip file containing the application itself
	2.  'Source code' : This comes as a .zip folder anda  .tar.gz file. Both contain a copy of the files in the repository which inclludes: Example Input data, example output files and the python script behind the application.

- To get the program running:
	1. Download the RaDeCC_Reader_OS_vX_X.zip file containing the application itself
	2. Open the RaDeCC_Reader_OS_vX_X file (this should result in a terminal window appearing with some code and then after a few moments the GUI should appear)
	3. Fill in all the fields in the GUI as per guidance below.
	4. Click 'Run RaDeCC Reader'
	5. When 'Run Complete' appears below the 'Run RaDeCC Reader' button, your corrected sample activities are ready!

## Using the RaDeCC Reader GUI

Once the GUI window has appear the data entry fields can be filled in:

**The first time the RaDeCC Reader GUI is used all fields must be filled out manually. Entries can however be saved before running the program and reloaded for later runs of the program.**

Panel 1:

1. Complete entry fields:

	- *Input directory* : The folder which contains the read files and logsheet that the user want to input to the RaDeCC Reader.

	- *Output directory* : The folder in which the RaDeCC Reader will place its output folder of calculation results.

	- *Logsheet File* : The .csv file containing the logsheet for the files in the 'Input directory'.

	- *DDMMYYYY Format* : This box is ticked if all read files and logsheets are dated using the the days before months convention. For months before days leave the box unticked.

	- *Contains sub-samples*: This box is ticked if the dataset contains sub-samples ('Branched') as opposed to unticked if the dataset does not contain sub-samples ('Linear')

	- *Spike Sensitivity*: The RaDeCC Reader defines 'spikes' (often electrical) by the number of counts higher the 'spike' interval is compared to the previous interval. Here the user can set this count threshold. If spike removal is not desired then the spike sensitivity number can be set very high (as is default). For more detail see 'Electrical spike detection and removal' below.

	- *Equilibration time (mins)*: When calculating the slope of radon-222 ingrowth in the total channel of a read a portion of time at the start of the read is ignored as the activity of radon-222 is equilibrating around the RaDeCC apparatus. The length of the portion of time that is ignore when calculating radon-222 ingrowth is set by the 'Equilibration time'.

- The number of thorium-228 standards, actinium-227 standards, blank standards and detectors is then indicated in the appropriate fields.

2. Check entries:
	- If no errors are apparent, 'OK' will appear next to each field and a 'Continue' button will appear.
	- If there is an error in one of the entry fields this will be indicated by an 'Error' next to the field containing the error.

3. Click 'Continue'

4. Complete Panel 2 entry fields:

	- Detector Fields:
		The below entry fields will need to be completed for each detector.
		- *Detector Name* :  the name used to identify the detector in read file names.
		- *226Ra Conversion Factor* : this is the change in total channel slope with radium-226 activity as described in Diego-Feliu et al. (2020).
		- *226Ra System Efficiency*: The efficiency with which the detector measures radium-226 activity as described by Diego-Feliu et al. (2020).
		- *SE219/220 Ratio*: The ratio of 219- and 220-channel efficiency as described by Moore and Cai (2013).
	
	- Actinium-227 Standard Fields:
		The below entry fields will need to be completed for each actinium-227 standard.
		- *227Ac Std Name*: The name used to identify the actinium-227 standard in standard read filenames. 
		- *Start Activity (dpm)* : The activity of the standard on its date of preparation.
		- *Date Made (DD/MM/YY HH:MM:SS)*: The date of preparation of the standard in 'DD/MM/YY HH:MM:SS' format.
	
	- Thorium-228 Standard:
		The below entry fields will need to be completed for each thorium-228standard.
		- *227Ac Std Name*: The name used to identify the thorium-228 standard in standard read filenames. 
		- *Start Activity (dpm)* : The activity of the standard on its date of preparation.
	
	


































## User Input to radecc_main.py

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
		
		linear_data_type = True
		linear_data_type = False
	
	Not:

		linear_data_type = 'True'
		linear_data_type = 'False'	

### Electrical spike detection and removal
The RaDeCC_Reader program is able to find spikes in read data that are anomalous (often due to a surge in the electrical supply to the RaDeCC detector). If a spike is found, it is removed and so is not included in the correction and error propagation calulcations that follow. The threshold that determines whether a spike is anomalous is set by the variable *spike_sensitivity*. This variable is set to 100 by default, meaning that if the number of counts in any time interval is more than 100 counts higher than the previous time interval it is deemed a spike and removed from calculations. To disable this function set *spike_sensitivity* = 1e6.

- *spike_sensitivity* : The threshold of counts in a time interval that determines whether a spike is anomalous or not.

### Information for the directory builder

- *sample_type*: This is the sample naming convention e.g. if your first sample is sample001 and your second is sample002 then sample_type is 'sample'
- *number_of_samples*: The is the number of samples (1-999).

### Information for the detector efficiency calculations

- *thstd*: This is the filename identifier for Thorium-228 standards e.g. 'thstd' in the filename 'thstd-250119-detector1.txt'
- *acstd*: This is the filename identifier for Actinium-227 standards e.g. 'acstd' in the filename 'acstd-250119-detector1.txt'
- *blank*: This is the filename identifier for blank standards e.g. 'blank' in the filename 'blank-250119-detector1.txt'
- *acstd_activity*: This is the start activity of the actinium-227 standard at the date of preparation
- *thstd_activity*:	This is the start activity of the thorium-228 standard at the date of preparation
- *thstd_prepDatestr* = date and time of thorium-228 standard preparation in the form - 'dd/mm/yyyy hh:mm:ss'
- *acstd_prepDatestr* = date and time of actinium-227 standard preparation in the form - 'dd/mm/yyyy hh:mm:ss'
- *det_list* =  list of detectors in the form - ['detector_1', 'detector_2', ..., 'detector_n']

### Logsheet identifiers (below)

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



### The program will also output the following files in .csv format

#### Dataframes (Found in the Dataframes Folder)
- A main table (.csv format) containing all metadata from logsheets as well as values for each level of the Garcia-Solsona corrections and uncertainty propagations, ending with dpm/1000L for both 223Ra and 224Ra as well as an estimation of 226Ra based on 222Rn ingrowth. All this is displayed for each read of each sample, ready for easy data-manipulation in Microsoft Excel.
- A summary table of detector efficiencies. 
- A table of efficiencies for each channel, detailing the efficiency calculated for each standard read.
- An output logsheet, the amalgamation of all input logsheets.

#### Plots (Found in the Read_Plots Folder)
- A plot of counts per minute for the total, radon-219 and radon-220 channels over the course of each read. Spikes in counts per minute (any counts that exceeded the default spike_sensitivity constant) have been removed. 




## Authors

* **Sean Selzer** - (https://github.com/oxradreader)
* **Amber L. Annett**
* **William B. Homoky**

## License

MIT

## Acknowledgments

The authors gratefully acknowledge support from the UK’s Natural Environment Research Council who funded S.S. through the Environmental Research Doctoral Training Partnership with University of Oxford, and A.L.A. and W.B.H. through Independent Research Fellowships (NE/P017630/1 and NE/K009532/1).