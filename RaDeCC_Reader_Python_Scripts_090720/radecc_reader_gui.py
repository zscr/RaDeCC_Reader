from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from ast import literal_eval
import pandas as pd
import os
import time
import tkinter as tk



def popupmsg(msg):
    popup = Toplevel()
    
    popup.wm_title("Error")
    label = ttk.Label(popup, text= msg, padding=(10, 2, 10, 6))
    label.grid(column = 0, row = 0)
    B1 = ttk.Button(popup, text='Close', command = lambda: popup.destroy())
    B1.grid(column = 1, row = 0)
    popup.mainloop()
    
    print ('pop_created')
    return()


def make_labelled_entry(variable_type, labeltext, labelrow):
    entry_label = Label(
            text = labeltext
        )
    entry_label.grid(column = 0, row = labelrow, sticky=W)

    entry_variable = variable_type
    entry_entry = Entry(
            textvariable=entry_variable, 
            width = 10
            )
    entry_entry.grid(column = 1, row = labelrow)
    return(entry_variable)


class App:

    def __init__ (self, master):
        self.master  = master
        self.padx_variable = 0
        self.panel1_entry_width = 10
        ###### Select Saved file Button ##################################################################
        self.load_saved_fields_button_row = 0
        self.load_saved_fields_button = Button(text="Load Saved Entries", command= lambda: self.find_saved_fields_file(1,0) )
        self.load_saved_fields_button.grid(column = 0, row = self.load_saved_fields_button_row)
        self.load_saved_fields_variable = StringVar()
        self.load_saved_fields_entry = Entry(textvariable = self.load_saved_fields_variable, width = self.panel1_entry_width)
        self.load_saved_fields_entry.grid(column = 1, row = self.load_saved_fields_button_row)
        ######################################################################################
        
        ###### Choose Input Directory Button ########################################################
        self.input_directory_button_row = 1
        self.input_directory_button = Button(
            master, text="Choose Input Directory...", bg='blue', command=self.find_input_directory)
        self.input_directory_button.grid(column = 0, row = self.input_directory_button_row)
        self.input_directory_variable = StringVar()
        self.input_directory_entry = Entry(textvariable = self.input_directory_variable, width = self.panel1_entry_width)
        self.input_directory_entry.grid(column = 1, row = self.input_directory_button_row)

        ###### Choose Output Directory Button ########################################################
        self.output_directory_button_row = 2
        self.output_directory_button = Button(
            master, text="Choose Output Directory...", bg='blue', command=self.find_output_directory)
        self.output_directory_button.grid(column = 0, row = self.output_directory_button_row )
        self.output_directory_variable = StringVar()
        self.output_directory_entry = Entry(textvariable = self.output_directory_variable, width = self.panel1_entry_width)
        self.output_directory_entry.grid(column = 1, row = self.output_directory_button_row )
        ######################################################################################
        
        ###### Select Logsheet Button ##################################################################
        self.load_logsheet_row = 3
        self.load_logsheet = Button(text="Select Logsheet File", command= lambda: self.find_logfile(1,self.load_logsheet_row))
        self.load_logsheet.grid(column = 0, row = self.load_logsheet_row )
        self.load_logsheet_variable = StringVar()
        self.load_logsheet_entry = Entry(textvariable = self.load_logsheet_variable, width = self.panel1_entry_width)
        self.load_logsheet_entry.grid(column = 1, row = self.load_logsheet_row)
        #########################################################################################
        
        ###### Check Inputs Button ##################################################################
        self.check_inputs = Button(text="Check Inputs", fg='green', command=self.panel1_checks)
        self.check_inputs.grid(column = 2, row = 4)
        ######################################################################################
        
        

        ###### Choose DDMMYYYY Format ########################################################        
        self.date_format_label = Label(
            master,
            text = 'DDMMYYYY Format:'
        )
        self.date_format_label.grid(column = 0, row = 4, sticky=W)

        self.date_format_variable = IntVar()
        c = Checkbutton(
            master,
            variable=self.date_format_variable,
            )
        c.grid(column = 1, row = 4)

        ###### Are there sub-samples? ########################################################
        self.subsample_check_label = Label(
            master,
            text = 'Contains sub-samples:'
        )
        self.subsample_check_label.grid(column = 0, row = 5, sticky=W)

        self.subsample_check_variable = IntVar()
        c = Checkbutton(
            master,
            variable=self.subsample_check_variable,
            )
        c.grid(column = 1, row = 5)

        ###### Spike_sensitivity ########################################################
        self.spike_sensitivity_row = 6
        self.spike_sensitivity_variable = make_labelled_entry(IntVar(), 'Spike sensitivity:', self.spike_sensitivity_row)
        self.spike_sensitivity_variable.set(10e6)

        ###### Equilibration time (minutes) ##############################################
        self.equilibration_time_variable_row = 7
        self.equilibration_time_variable = make_labelled_entry(IntVar(),'Equilibration time (mins):', self.equilibration_time_variable_row)

        ###### Number of Thorium-228 Standards ##############################################
        self.no_of_thstds_variable_row = 8
        self.no_of_thstds_variable = make_labelled_entry(IntVar(),'No. of 228Th Standards:', self.no_of_thstds_variable_row)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_acstds_variable_row = 9
        self.no_of_acstds_variable = make_labelled_entry(IntVar(),'No. of 227Ac Standards:', self.no_of_acstds_variable_row)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_blanks_variable_row = 10
        self.no_of_blanks_variable = make_labelled_entry(IntVar(),'No. of Blanks:', self.no_of_blanks_variable_row)

        ###### Number of Detectors ##############################################
        self.no_of_detectors_variable_row = 11
        self.no_of_detectors_variable = make_labelled_entry(IntVar(),'No. of Detectors:', self.no_of_detectors_variable_row)

        self.logo_filename = "RaDeCC_Reader_Python_Scripts_090720/RR_logo.png"
        self.rr_logo = PhotoImage(file=self.logo_filename)
        self.logo_label = Label(image = self.rr_logo)
        self.logo_label.grid(column = 2, row=0, rowspan = 3)

    def find_input_directory(self):
    
        self.chosen_query_input_directory = fd.askdirectory(mustexist = True)
        print (self.chosen_query_input_directory)
        self.input_directory_variable.set(self.chosen_query_input_directory)

    def find_output_directory(self):
    
        self.chosen_query_output_directory = fd.askdirectory(mustexist = True)
        print (self.chosen_query_output_directory)
        self.output_directory_variable.set(self.chosen_query_output_directory)

    def find_logfile(self, column_number, row_number):
        self.logfile_to_load = fd.askopenfilename()
        try:
            self.logfile_to_load_as_df = pd.read_csv(self.logfile_to_load)
            self.load_logsheet_variable.set(self.logfile_to_load)
        except:
            self.load_logsheet_variable.set('Error: Select another file')
    
    def find_saved_fields_file(self, column_number, row_number):
        self.saved_fields_file_to_load = fd.askopenfilename()
        self.saved_fields_file_to_load_as_df = pd.read_csv(self.saved_fields_file_to_load)
        self.load_saved_fields_variable.set(self.saved_fields_file_to_load)

        """Set self.variables from saved_fields_file_to_load_as_df"""
        self.chosen_query_input_directory = self.saved_fields_file_to_load_as_df.Input_Directory[0]
        self.input_directory_variable.set(self.chosen_query_input_directory)
        
        self.chosen_query_output_directory = self.saved_fields_file_to_load_as_df.Output_Directory[0]
        self.output_directory_variable.set(self.chosen_query_output_directory)


        self.logfile_to_load = self.saved_fields_file_to_load_as_df.Logsheet_Filepath[0]
        self.load_logsheet_variable.set(self.logfile_to_load)


        self.date_format_variable.set(self.saved_fields_file_to_load_as_df.DDMMYY_Format[0])
        self.subsample_check_variable.set(self.saved_fields_file_to_load_as_df.sub_sample_variable[0])
        self.spike_sensitivity_variable.set(self.saved_fields_file_to_load_as_df.Spike_sensitivity_variable[0])
        self.equilibration_time_variable.set(self.saved_fields_file_to_load_as_df.Equilibration_time[0])

        self.no_of_thstds_variable.set(self.saved_fields_file_to_load_as_df.number_of_thorium_stds[0])
        self.no_of_acstds_variable.set(self.saved_fields_file_to_load_as_df.number_of_actinium_stds[0])

        self.no_of_blanks_variable.set(self.saved_fields_file_to_load_as_df.number_of_blanks[0])
        self.no_of_detectors_variable.set(self.saved_fields_file_to_load_as_df.number_of_detectors[0])

    def check_number_inputs(self, number_variable, column_number, row_number):
        
        try:
            number_variable.get()
            check_label = Label(text = 'OK', fg='green', padx = self.padx_variable)
            check_label.grid(column = column_number, row = row_number)
            return(True)
        except TclError: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Err', fg='red')
            check_label.grid(column = column_number, row = row_number)
            return(False)

    def check_string_inputs(self, string_variable, row_number, column_number):
        allowed_chars = list('ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz0123456789_')
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) != 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'OK', fg='green', padx = self.padx_variable+6)
            check_label.grid(column = column_number, row = row_number)
            return(True)
        
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) == 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'Err', fg='red', padx = self.padx_variable)
            check_label.grid(column = column_number, row = row_number)
            return(False)

        else: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Err', fg='red')
            check_label.grid(column = column_number, row = row_number)
            return(False)
 
    def panel1_checks (self):
        
        """ saved_fields_file_to_load Check"""
        try: 
            list(self.saved_fields_file_to_load)
            saved_fields_file_to_load_check = True
        except:
            saved_fields_file_to_load_check = False
            self.load_saved_fields_variable.set('Please select...')
            
        """Input Directory Check"""
        try: 
            chosen_query_input_directory_check = os.path.exists(self.chosen_query_input_directory)
        except:
            chosen_query_input_directory_check = False
            self.input_directory_variable.set('Please select...')
        
        """Output Directory Check"""
        try: 
            chosen_query_output_directory_check = os.path.exists(self.chosen_query_output_directory)
        except:
            chosen_query_output_directory_check = False
            self.output_directory_variable.set('Please select...')
            
        
        """Logsheet Select Check"""
        try: 
            logfile_to_load_check = os.path.exists(self.logfile_to_load)
        except:
            logfile_to_load_check = False
            self.load_logsheet_variable.set('Please select...')
            

        """Number checks"""
        spike_sensitivity_variable_check = self.check_number_inputs(self.spike_sensitivity_variable, column_number=2, row_number=self.spike_sensitivity_row)
        equilibration_time_variable_check = self.check_number_inputs(self.equilibration_time_variable , column_number=2, row_number=self.equilibration_time_variable_row)
        no_of_thstds_variable_check = self.check_number_inputs(self.no_of_thstds_variable ,column_number=2, row_number= self.no_of_thstds_variable_row)
        no_of_acstds_variable_check = self.check_number_inputs(self.no_of_acstds_variable ,column_number=2, row_number=self.no_of_acstds_variable_row)
        no_of_blanks_variable_check = self.check_number_inputs(self.no_of_blanks_variable ,column_number=2, row_number=self.no_of_blanks_variable_row)
        no_of_detectors_variable_check = self.check_number_inputs(self.no_of_detectors_variable ,column_number=2, row_number=self.no_of_detectors_variable_row)

        check_list = [chosen_query_input_directory_check,
                        chosen_query_output_directory_check,
                        logfile_to_load_check,
                        spike_sensitivity_variable_check,
                        equilibration_time_variable_check,
                        no_of_thstds_variable_check,
                        no_of_acstds_variable_check,
                        no_of_blanks_variable_check,
                        no_of_detectors_variable_check]
        
        # popupmsg(str(check_list))
        self.run_button_panel1_row = self.no_of_detectors_variable_row +1
        if False not in check_list:
            self.run_button_1 = Button(text="Continue", fg='green', command= lambda : self.create_panel2())
            self.run_button_1.grid(column = 2, row = self.run_button_panel1_row)
        
        if False in check_list:
            self.run_button_1 = Button(text="Continue", fg='grey', command=lambda : popupmsg('Errors apparent'))
            self.run_button_1.grid(column = 2, row = self.run_button_panel1_row)

    def save_previous_inputs(self):

        save_dict = {
            'Input_Directory':[self.chosen_query_input_directory],
            'Output_Directory':[self.chosen_query_output_directory],
            'Logsheet_Filepath': [self.logfile_to_load],
            'DDMMYY_Format': [self.date_format_variable.get()],
            'sub_sample_variable':[self.subsample_check_variable.get()],
            'Spike_sensitivity_variable':[self.spike_sensitivity_variable.get()],
            'Equilibration_time':[self.equilibration_time_variable.get()],
            'number_of_thorium_stds':[self.no_of_thstds_variable.get()],
            'number_of_actinium_stds':[self.no_of_acstds_variable.get()],
            'number_of_blanks':[self.no_of_blanks_variable.get()],
            'number_of_detectors':[self.no_of_detectors_variable.get()],
            'th228_standard_start_activities_dict':[self.th228_standard_start_activity_dict],
            'ac227_standard_manufacture_date_dict':[self.ac227_standard_manufacture_date_dict],
            'ac227_standard_start_activities_dict':[self.ac227_standard_start_activity_dict],
            'blank_standard_names_list':[self.blank_standard_names_list],
            'detector_calibration_values_dict':[self.detector_calibration_values_dict],
            'detector_adjustment_coefficient_dict':[self.detector_adjustment_coefficient_dict],
            'detector_226_efficiency_dict':[self.detector_226_efficiency_dict],
            'sample_name_column_variable':[self.sample_name_column_variable.get()],
            'sub_sample_variable':[self.sub_sample_variable.get()],
            'sample_mid_date':[self.sample_mid_date.get()],
            'sample_mid_time':[self.sample_mid_time.get()],
            'sample_volume_variable':[self.sample_volume_variable.get()],
            'sample_volume_error_variable':[self.sample_volume_error_variable.get()]

        }
        save_df = pd.DataFrame.from_dict(save_dict, orient = 'columns')
        save_df.to_csv(os.path.join(self.chosen_query_output_directory,'RR_GUI_entries_'+time.strftime("%H%M%S_%Y-%m-%d")+'.csv'))
        print ('Saved')
        
        return()

    def create_panel2(self):

        extra_padding = 0
        ###### Load Button ##################################################################
        self.load_saved_fields_button = Button(text="Load Saved Entries", command= lambda: self.load_panel2_entries() )
        self.load_saved_fields_button.grid(column = 4, row = 0)
        #####################################################################################
        
        # self.th228_standard_name_label = Label(text = 'Th228 Std Name:', fg = 'black', padx = self.padx_variable)
        # self.th228_standard_name_label.grid(column = 4, row = self.th228_entries_start_row)
        # '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        # self.th228_standard_name_widget_list = self.make_entry_widget_list( column_number = 4, start_row = self.th228_entries_start_row+1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'String')

        self.ac227_entries_start_row = 1
        
        self.ac227_standard_name_label = Label(text = '227Ac Std Name:', fg = 'black', padx = self.padx_variable+extra_padding)
        self.ac227_standard_name_label.grid(column = 4, row = self.ac227_entries_start_row)
        self.ac227_standard_name_widget_list = self.make_entry_widget_list(column_number = 4, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'String')
        
        self.ac227_standard_manufacture_date_label = Label(text = 'Date Made (DD/MM/YY HH:MM:SS):', fg = 'black', padx = self.padx_variable+extra_padding+3)
        self.ac227_standard_manufacture_date_label.grid(column = 6, row = self.ac227_entries_start_row)
        self.ac227_standard_manufacture_date_widget_list = self.make_entry_widget_list(column_number = 6, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'String')
        
        self.ac227_standard_start_activity_label = Label(text = 'Start Activity (dpm):', fg = 'black', padx = self.padx_variable+extra_padding)
        self.ac227_standard_start_activity_label.grid(column = 5, row = self.ac227_entries_start_row)
        self.ac227_standard_start_activity_widget_list = self.make_entry_widget_list(column_number = 5, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'Double')
        
        self.th228_entries_start_row = self.ac227_entries_start_row+self.no_of_acstds_variable.get()+1
        self.th228_standard_name_label = Label(text = 'Th228 Std Name:', fg = 'black', padx = self.padx_variable)
        self.th228_standard_name_label.grid(column = 4, row = self.th228_entries_start_row)
        '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        self.th228_standard_name_widget_list = self.make_entry_widget_list( column_number = 4, start_row = self.th228_entries_start_row+1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'String')

        self.th228_standard_start_activity_label = Label(text = 'Start Activity (dpm):', fg = 'black', padx = self.padx_variable+extra_padding)
        self.th228_standard_start_activity_label.grid(column = 5, row = self.th228_entries_start_row)
        '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        self.th228_standard_start_activity_widget_list = self.make_entry_widget_list(column_number = 5, start_row = self.th228_entries_start_row+1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'Double')
        
        self.blank_entries_start_row = self.th228_entries_start_row+self.no_of_thstds_variable.get()+1

        self.blank_standard_name_label = Label(text = 'Blank Std Name:', fg = 'black', padx = self.padx_variable+extra_padding)
        self.blank_standard_name_label.grid(column = 4, row = self.blank_entries_start_row)
        self.blank_standard_name_widget_list = self.make_entry_widget_list(column_number = 4, start_row = self.blank_entries_start_row+1, number_of_widgets =  self.no_of_blanks_variable.get(), var_type = 'String')

        if self.run_button_panel1_row+1 > self.blank_entries_start_row+self.no_of_blanks_variable.get()+1:
            self.detector_entries_start_row = self.run_button_panel1_row+1
        else:
            self.detector_entries_start_row = self.blank_entries_start_row+self.no_of_blanks_variable.get()+1
        
        self.detector_name_column = 0
        self.detector_name_label = Label(text = 'Detector Name:', fg = 'black', padx = self.padx_variable+extra_padding+6)
        self.detector_name_label.grid(column = self.detector_name_column, row = self.detector_entries_start_row)
        self.detector_name_widget_list = self.make_entry_widget_list(column_number = self.detector_name_column, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'String')

        self.detector_calibration_values_column = 1
        self.detector_calibration_values_label = Label(text = '226Ra Calibration Value:', fg = 'black', padx = self.padx_variable)
        self.detector_calibration_values_label.grid(column = self.detector_calibration_values_column, row = self.detector_entries_start_row)
        self.detector_calibration_values_widget_list = self.make_entry_widget_list(column_number = self.detector_calibration_values_column, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'Double')

        self.detector_226_efficiency_column = 2
        self.detector_226_efficiency_label = Label(text = '226Ra System Efficiency:', fg = 'black', padx = self.padx_variable)
        self.detector_226_efficiency_label.grid(column = self.detector_226_efficiency_column, row = self.detector_entries_start_row)
        self.detector_226_efficiency_widget_list = self.make_entry_widget_list(column_number = self.detector_226_efficiency_column, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'Double')
        
        self.detector_adjustment_coefficient_column = 4
        self.detector_adjustment_coefficient_label = Label(text = 'SE219/SE220 ratio:', fg = 'black', padx = self.padx_variable)
        self.detector_adjustment_coefficient_label.grid(column = self.detector_adjustment_coefficient_column, row = self.detector_entries_start_row)
        self.detector_adjustment_coefficient_widget_list = self.make_entry_widget_list(column_number = self.detector_adjustment_coefficient_column, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'Double')

        # # # # # Logsheet Identifier menus
        self.logfile_to_load_as_df = pd.read_csv(self.logfile_to_load)
        self.logsheet_columns = list(self.logfile_to_load_as_df.columns)

        self.logsheet_identifiers_label_row = self.th228_entries_start_row
        self.logsheet_identifiers_label_column = 6
        self.logsheet_identifiers_label = Label(text = "Logsheet Variable Selection:")
        self.logsheet_identifiers_label.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row, sticky = 'W')
        
        # options_list = ["Choose sample name column...", "one", "two", "three", "four"]
        
        # # # # # sample_variable
        self.sample_name_column_variable = StringVar()
        self.sample_name_column_variable.set("Sample name column...") # initial value
        self.sample_name_option = OptionMenu(self.master, self.sample_name_column_variable, *self.logsheet_columns)
        self.sample_name_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+1, sticky = W)
        # # # # # sub_sample_variable
        self.sub_sample_options = self.logsheet_columns + ['None']
        self.sub_sample_variable = StringVar()
        self.sub_sample_variable.set("Sub-sample name column...") # initial value
        self.sub_sample_name_option = OptionMenu(self.master, self.sub_sample_variable, *self.sub_sample_options)
        self.sub_sample_name_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+2, sticky = W)
        # # # # # sample_mid_date
        self.sample_mid_date = StringVar()
        self.sample_mid_date.set("Sampling date column...") # initial value
        self.sample_mid_date_option = OptionMenu(self.master, self.sample_mid_date, *self.logsheet_columns)
        self.sample_mid_date_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+3, sticky = W)
        # # # # # sample_mid_time
        self.sample_mid_time = StringVar()
        self.sample_mid_time.set("Mid-sampling time column...") # initial value
        self.sample_mid_time_option = OptionMenu(self.master, self.sample_mid_time, *self.logsheet_columns)
        self.sample_mid_time_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+4, sticky = W)
        # # # # # sample_volume
        self.sample_volume_variable = StringVar()
        self.sample_volume_variable.set("Volume column...") # initial value
        self.sample_volume_option = OptionMenu(self.master, self.sample_volume_variable, *self.logsheet_columns)
        self.sample_volume_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+5, sticky = W)
        # # # # # sample_volume_error
        self.sample_volume_error_variable = StringVar()
        self.sample_volume_error_variable.set("Volume error column...") # initial value
        self.sample_volume_error_option = OptionMenu(self.master, self.sample_volume_error_variable, *self.logsheet_columns)
        self.sample_volume_error_option.grid(column = self.logsheet_identifiers_label_column, row = self.logsheet_identifiers_label_row+6, sticky = W)



        ###### Check Inputs Button No.2 ##################################################################
        self.check_inputs = Button(text="Check Inputs", fg='green', 
                                    command= lambda: self.check_panel2())
        self.check_inputs.grid(column = 7, row = 0)
        ######################################################################################

    def make_entry_widget_list(self, column_number, start_row, number_of_widgets, var_type):
        entry_list = []
        variable_list = []
        widget_list = []
        for i in range(start_row, start_row+number_of_widgets):

            if var_type == 'String':
                variable_list.append(StringVar())
            if var_type == 'Int':
                variable_list.append(IntVar())
            if var_type == 'Double':
                variable_list.append(DoubleVar())

            entry_list.append( Entry(textvariable = variable_list[-1], width = 10))
            entry_list[-1].grid(column = column_number, row = i)
            widget_list.append([entry_list[-1],variable_list[-1]])

        return(widget_list)

    def check_date_inputs (self, date_variable, column_number=0, row_number=0):
        print (date_variable, type(date_variable))
        if '/' in date_variable.get():
            try:
                pd.to_datetime(date_variable.get())
                return(True)
            except:
                return(False)
        else:
            return(False)

    def check_panel2 (self):

        """Check Thorium-228 standard Entries"""
        # th228_standard_entries_boolean = self.check_widget_list_set(self.th228_standard_name_widget_list, 'N/A', 
        #                                                                         column_number = 7, row_number = self.th228_entries_start_row)
        th228_standard_entries_boolean_list = []
        for i in range(len(self.th228_standard_start_activity_widget_list)):
            th228_standard_entries_boolean_list.append(self.check_string_inputs(string_variable=self.th228_standard_name_widget_list[i][1], column_number=7, row_number=self.th228_entries_start_row+2))

        print("th names:", th228_standard_entries_boolean_list)

        th228_standard_start_activities_boolean_list = []
        for i in range(len(self.th228_standard_start_activity_widget_list)):
            th228_standard_start_activities_boolean_list.append(self.check_number_inputs(number_variable=self.th228_standard_start_activity_widget_list[i][1], column_number=7, row_number=self.th228_entries_start_row+2))

        print("th activities:", th228_standard_start_activities_boolean_list)
        
        if False in th228_standard_entries_boolean_list:
            check_label = Label(text = 'Error(std_name)', fg='red')
            check_label.grid(column = 7, row =self.th228_entries_start_row+1)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.th228_entries_start_row+1)

        if False in th228_standard_start_activities_boolean_list:
            check_label = Label(text = 'Error(activity)', fg='red')
            check_label.grid(column = 7, row =self.th228_entries_start_row+2)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.th228_entries_start_row+2)
        
        """Check Actinium-227 standard Entries"""
        # ac227_standard_entries_boolean = self.check_widget_list_set(self.ac227_standard_name_widget_list, self.ac227_standard_manufacture_date_widget_list, 
        #                                                                         column_number = 7, row_number = self.ac227_entries_start_row)
        ac227_standard_name_boolean_list = []
        for i in range(len(self.ac227_standard_start_activity_widget_list)):
            ac227_standard_name_boolean_list.append(self.check_string_inputs(string_variable=self.ac227_standard_name_widget_list[i][1], column_number=7, row_number=self.ac227_entries_start_row))
        ac227_standard_start_activities_boolean_list = []
        for i in range(len(self.ac227_standard_start_activity_widget_list)):
            ac227_standard_start_activities_boolean_list.append(self.check_number_inputs(number_variable=self.ac227_standard_start_activity_widget_list[i][1], column_number=7, row_number=self.ac227_entries_start_row+1))
        ac227_standard_manufacture_date_boolean_list = []
        for i in range(len(self.ac227_standard_start_activity_widget_list)):
            ac227_standard_manufacture_date_boolean_list.append(self.check_date_inputs(date_variable=self.ac227_standard_manufacture_date_widget_list[i][1], column_number=7, row_number=self.ac227_entries_start_row+2))
        

        if False in ac227_standard_name_boolean_list:
            check_label = check_label = Label(text = 'Error(name)', fg='red')
            check_label.grid(column = 7, row =self.ac227_entries_start_row)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.ac227_entries_start_row)

        if False in ac227_standard_start_activities_boolean_list:
            check_label = check_label = Label(text = 'Error(activity)', fg='red')
            check_label.grid(column = 7, row =self.ac227_entries_start_row+1)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.ac227_entries_start_row+1)

        if False in ac227_standard_manufacture_date_boolean_list:
            check_label = check_label = Label(text = 'Error(date)', fg='red')
            check_label.grid(column = 7, row =self.ac227_entries_start_row+2)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.ac227_entries_start_row+2)
        
        
        
        """Check Blank Entries"""
        # blank_entries_boolean = self.check_widget_list_set(self.blank_standard_name_widget_list, 'N/A', 
        #                                                                         column_number = 7, row_number = self.blank_entries_start_row+1)
        blank_entries_boolean_list = []
        for i in range(len(self.blank_standard_name_widget_list)):
            blank_entries_boolean_list.append(self.check_string_inputs(string_variable=self.blank_standard_name_widget_list[i][1], column_number=7, row_number=self.blank_entries_start_row+1))
        
        if False in blank_entries_boolean_list:
            check_label = Label(text = 'Error(name)', fg='red', padx = self.padx_variable)
            check_label.grid(column = 7, row =self.blank_entries_start_row+1)
        else:
            check_label = Label(text = 'OK', fg='green')
            check_label.grid(column = 7, row =self.blank_entries_start_row+1)

        """Detector Entries"""
        detector_names_boolean_list = []
        detector_calibration_values_boolean_list = []
        detector_226_efficiency_boolean_list = []
        detector_adjustment_coefficient_boolean_list = []

        for i in range(len(self.detector_name_widget_list)):
            detector_names_boolean_list.append(self.check_string_inputs(string_variable = self.detector_name_widget_list[i][1], 
                                                                                row_number = self.detector_entries_start_row+1, column_number = 7))
            detector_calibration_values_boolean_list.append(self.check_number_inputs(number_variable=self.detector_calibration_values_widget_list[i][1], 
                                                                                column_number = 7, row_number=self.detector_entries_start_row+2))
            detector_226_efficiency_boolean_list.append(self.check_number_inputs(number_variable=self.detector_226_efficiency_widget_list[i][1], 
                                                                                column_number = 7, row_number=self.detector_entries_start_row+3))
            detector_adjustment_coefficient_boolean_list.append(self.check_number_inputs(number_variable=self.detector_adjustment_coefficient_widget_list[i][1], 
                                                                                column_number = 7, row_number=self.detector_entries_start_row+4))
        print (detector_226_efficiency_boolean_list,detector_adjustment_coefficient_boolean_list)
        if False in detector_names_boolean_list:
            check_label = check_label = Label(text = 'Error(name)', fg='red')
            check_label.grid(column = 7, row =self.detector_entries_start_row+1)
        if False in detector_calibration_values_boolean_list:
            check_label = check_label = Label(text = 'Error(calib_value)', fg='red')
            check_label.grid(column = 7, row =self.detector_entries_start_row+2)
        if False in detector_226_efficiency_boolean_list:
            check_label = check_label = Label(text = 'Error(226_Eff)', fg='red')
            check_label.grid(column = 7, row =self.detector_entries_start_row+3)
        if False in detector_adjustment_coefficient_boolean_list:
            check_label = check_label = Label(text = 'Error(ratio)', fg='red')
            check_label.grid(column = 7, row =self.detector_entries_start_row+4)

        """________________________________________________________________________________________Check Logsheet Identifier Entries________________________________________________________________________________________________________________________"""
        logsheet_identifiers_boolean_list = [False,False,False,False,False,False]
        # # # sample_name_column_variable
        if self.sample_name_column_variable.get() != 'Sample name column...':
            sample_name_list = list(set(self.logfile_to_load_as_df[self.sample_name_column_variable.get()]))
            count = 0
            for test_name_a in sample_name_list:
                for test_name_b in sample_name_list:
                    if str(test_name_a) in str(test_name_b):
                        count = count+1
            if count>len(sample_name_list):
                logsheet_identifiers_boolean_list[1] = False
                showinfo('Warning: RaDeCC Reader','Sample names provided are non-unique: some sample names are contained within others')
            else:
                logsheet_identifiers_boolean_list[0] = True
        else:
            showinfo('Warning: RaDeCC Reader','Please choose sample name column...')
            logsheet_identifiers_boolean_list[1] = False

        # # # sub_sample_variable
        if self.sample_name_column_variable.get() != 'Sample name column...':

            if self.sub_sample_variable.get() != 'Sub-sample name column...' and self.sub_sample_variable.get() != 'None':

                sub_sample_name_list = list(set(self.logfile_to_load_as_df[self.sub_sample_variable.get()]))
                test_list = []
                for i in range(len(self.logfile_to_load_as_df[self.sample_name_column_variable.get()])):
                    test_list.append(str(self.logfile_to_load_as_df[self.sample_name_column_variable.get()].iloc[i])+str(self.logfile_to_load_as_df[self.sub_sample_variable.get()].iloc[i]))

                print (test_list)
                sub_sample_name_list = list(set(test_list))
                count = 0
                for test_name_a in sub_sample_name_list:
                    for test_name_b in sub_sample_name_list:
                        if str(test_name_a) in str(test_name_b):
                            count = count+1
                if count>len(sub_sample_name_list):
                    logsheet_identifiers_boolean_list[1] = False
                    showinfo('Warning: RaDeCC Reader','Sub-sample names provided are non-unique: some sample names are contained within others')
                else:
                    logsheet_identifiers_boolean_list[1] = True
            if self.sub_sample_variable.get() == 'None':
                print('Linear', self.sub_sample_variable.get())
                logsheet_identifiers_boolean_list[1] = True

            if self.sub_sample_variable.get() == 'Sub-sample name column...':
                showinfo('Warning: RaDeCC Reader','Please choose sub-sample name column...')
                logsheet_identifiers_boolean_list[1] = False
        # # # sample_mid_date
        if self.sample_mid_date.get() != 'Sampling date column...':
            mid_date_boolean_list = []
            for mid_date in list(self.logfile_to_load_as_df[self.sample_mid_date.get()]):
                if '/' in str(mid_date):
                    try:
                        pd.to_datetime(str(mid_date))
                        mid_date_boolean_list.append(True)
                    except:
                        mid_date_boolean_list.append(False)
                else:
                    mid_date_boolean_list.append(False)

            if all(mid_date_boolean_list)==True:
                logsheet_identifiers_boolean_list[2] = True
            else:
                logsheet_identifiers_boolean_list[2] = False
                showinfo('Warning: RaDeCC Reader','Sample dates column selected contains non-date values')
        
        # # # sample_mid_time
        if self.sample_mid_time.get() != 'Mid-sampling time column...':
            mid_time_boolean_list = []
            for mid_time in list(self.logfile_to_load_as_df[self.sample_mid_time.get()]):
                if ':' in str(mid_time):
                    try:
                        pd.to_datetime(str(mid_time))
                        mid_time_boolean_list.append(True)
                    except:
                        mid_time_boolean_list.append(False)
                else:
                    mid_time_boolean_list.append(False)

            if all(mid_time_boolean_list)==True:
                logsheet_identifiers_boolean_list[3] = True
            else:
                logsheet_identifiers_boolean_list[3] = False
                showinfo('Warning: RaDeCC Reader','Sample times column selected contains non-time values')
        
        # # # sample_volume_variable
        if self.sample_volume_variable.get() != 'Volume column...':
            volume_boolean_list = []
            for volume in list(self.logfile_to_load_as_df[self.sample_volume_variable.get()]):
                try:
                    float(str(volume))
                    volume_boolean_list.append(True)
                except ValueError:
                    volume_boolean_list.append(False)
            
            if all(volume_boolean_list)==True:
                logsheet_identifiers_boolean_list[4] = True
            else:
                logsheet_identifiers_boolean_list[4] = False
                showinfo('Warning: RaDeCC Reader','Sample volume column contains non-numeric values')
        
        # # # sample_volume_error_variable
        if self.sample_volume_error_variable.get() != 'Volume error column...':
            volume_error_boolean_list = []
            for volume_error in list(self.logfile_to_load_as_df[self.sample_volume_error_variable.get()]):
                try:
                    float(str(volume_error))
                    volume_error_boolean_list.append(True)
                except ValueError:
                    volume_error_boolean_list.append(False)
            
            if all(volume_error_boolean_list)==True:
                logsheet_identifiers_boolean_list[5] = True
            else:
                logsheet_identifiers_boolean_list[5] = False
                showinfo('Warning: RaDeCC Reader','Sample volume error column contains non-numeric values')







        # # # Check that a column hasn't been picked twice
        option_picked_twice = [False]
        list_of_option_variables = [self.sample_name_column_variable.get(),
                                    self.sub_sample_variable.get(),
                                    self.sample_mid_date.get(),
                                    self.sample_mid_time.get(),
                                    self.sample_volume_variable.get(),
                                    self.sample_volume_error_variable.get()]
        if len(set(list_of_option_variables))<len(list_of_option_variables):
            showinfo('Warning: RaDeCC Reader','A logsheet column has been selected twice')
            option_picked_twice[0]=False
        else:
            option_picked_twice[0]=True
        """_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________"""





        print('log:', logsheet_identifiers_boolean_list)
        # detector_entries_boolean = all(detector_names_boolean_list+
        #                                 detector_calibration_values_boolean_list+
        #                                 detector_226_efficiency_boolean_list+
        #                                 detector_adjustment_coefficient_boolean_list)
        
        all_new_entries_boolean = all(th228_standard_entries_boolean_list+ 
                                        th228_standard_start_activities_boolean_list+
                                        ac227_standard_name_boolean_list+
                                        blank_entries_boolean_list+
                                        ac227_standard_start_activities_boolean_list+
                                        detector_names_boolean_list+
                                        detector_calibration_values_boolean_list+
                                        detector_226_efficiency_boolean_list+
                                        detector_adjustment_coefficient_boolean_list+
                                        logsheet_identifiers_boolean_list)
        

        if all_new_entries_boolean is True:
            
            # self.th228_standard_manufacture_date_dict = dict(zip([x[1].get() for x in self.th228_standard_name_widget_list], [x[1].get() for x in self.th228_standard_manufacture_date_widget_list]))
            self.th228_standard_start_activity_dict = dict(zip([x[1].get() for x in self.th228_standard_name_widget_list], [x[1].get() for x in self.th228_standard_start_activity_widget_list]))
            
            self.ac227_standard_manufacture_date_dict = dict(zip([x[1].get() for x in self.ac227_standard_name_widget_list], [x[1].get() for x in self.ac227_standard_manufacture_date_widget_list]))
            self.ac227_standard_start_activity_dict = dict(zip([x[1].get() for x in self.ac227_standard_name_widget_list], [x[1].get() for x in self.ac227_standard_start_activity_widget_list]))
            
            self.blank_standard_names_list = [x[1].get() for x in self.blank_standard_name_widget_list]

            self.detector_calibration_values_dict = dict(zip([x[1].get() for x in self.detector_name_widget_list], [x[1].get() for x in self.detector_calibration_values_widget_list]))
            self.detector_adjustment_coefficient_dict = dict(zip([x[1].get() for x in self.detector_name_widget_list], [x[1].get() for x in self.detector_adjustment_coefficient_widget_list]))
            self.detector_226_efficiency_dict = dict(zip([x[1].get() for x in self.detector_name_widget_list], [x[1].get() for x in self.detector_226_efficiency_widget_list ]))
            
            ###### Save Inputs Button No.2 ##################################################################
            self.save_previous_inputs_button_2 = Button(text = "Save Field Inputs", command = lambda : self.save_previous_inputs())
            self.save_previous_inputs_button_2.grid(column = 7, row = self.detector_entries_start_row+4+1)
            #################################################################################################

            ###### Run Program Button ##################################################################
            self.run_button = Button(text = "Run RaDeCC Reader", fg = 'green', command = lambda : print(self.saved_fields_file_to_load_as_df))
            self.run_button.grid(column = 7, row = self.detector_entries_start_row+4+2)
            #################################################################################################
            

            



        if all_new_entries_boolean is False:
            print('nay.', [th228_standard_entries_boolean_list, ac227_standard_name_boolean_list,blank_entries_boolean_list,detector_names_boolean_list])
            ###### Save Inputs Button No.2 ##################################################################
            # self.save_previous_inputs_error_label = Label(text = "Input Error(s)", fg = 'red', padx = self.padx_variable)
            # self.save_previous_inputs_error_label.grid(column = 7, row = self.detector_entries_start_row+4+1)
            #################################################################################################

            ###### Run Program Button ##################################################################
            self.run_error_button = Button(text = "Run RaDeCC Reader", fg = 'grey')
            self.run_error_button.grid(column = 7, row = self.detector_entries_start_row+4+2)
            #################################################################################################

    def load_panel2_entries (self):
        df = self.saved_fields_file_to_load_as_df
        '''load th228_fields'''
        th228_standard_names_list = list(literal_eval(df.th228_standard_start_activities_dict[0]).keys())
        th228_standard_start_activity_list = list(literal_eval(df.th228_standard_start_activities_dict[0]).values())

        for i in range(len(self.th228_standard_name_widget_list)):
            self.th228_standard_name_widget_list[i][1].set(th228_standard_names_list[i])
            self.th228_standard_start_activity_widget_list[i][1].set(th228_standard_start_activity_list[i])
        
        '''load ac227_fields'''
        ac227_standard_names_list = list(literal_eval(df.ac227_standard_manufacture_date_dict[0]).keys())
        ac227_standard_manufacture_date_list = list(literal_eval(df.ac227_standard_manufacture_date_dict[0]).values())
        ac227_standard_start_activity_list = list(literal_eval(df.ac227_standard_start_activities_dict[0]).values())

        for i in range(len(self.ac227_standard_name_widget_list)):
            self.ac227_standard_name_widget_list[i][1].set(ac227_standard_names_list[i])
            self.ac227_standard_manufacture_date_widget_list[i][1].set(ac227_standard_manufacture_date_list[i])
            self.ac227_standard_start_activity_widget_list[i][1].set(ac227_standard_start_activity_list[i])

        '''load blank_fields'''
        blank_standard_names_list = literal_eval(df.blank_standard_names_list[0])
        for i in range(len(blank_standard_names_list)):
            self.blank_standard_name_widget_list[i][1].set(blank_standard_names_list[i])
        
        '''load detector_fields'''
        detector_names_list = list(literal_eval(df.detector_calibration_values_dict[0]).keys())
        detector_calibration_values_list = list(literal_eval(df.detector_calibration_values_dict[0]).values())
        detector_adjustment_coefficient_list = list(literal_eval(df.detector_adjustment_coefficient_dict[0]).values())
        detector_226_efficiency_list = list(literal_eval(df.detector_226_efficiency_dict[0]).values())

        for i in range(len(detector_names_list)):
            self.detector_name_widget_list[i][1].set(detector_names_list[i])
            self.detector_calibration_values_widget_list[i][1].set(detector_calibration_values_list[i])
            self.detector_adjustment_coefficient_widget_list[i][1].set(detector_adjustment_coefficient_list[i])
            self.detector_226_efficiency_widget_list[i][1].set(detector_226_efficiency_list[i])
        
        '''load logsheet identifier option menus'''
                        # list_of_option_variables = [self.sample_name_column_variable.get(),
                #                     self.sub_sample_variable.get(),
                #                     self.sample_mid_date.get(),
                #                     self.sample_mid_time.get(),
                #                     self.sample_volume_variable.get(),
                #                     self.sample_volume_error_variable.get()]
        self.sample_name_column_variable.set(df.sample_name_column_variable[0])
        self.sub_sample_variable.set(df.sub_sample_variable[0])
        self.sample_mid_date.set(df.sample_mid_date[0])
        self.sample_mid_time.set(df.sample_mid_time[0])
        self.sample_volume_variable.set(df.sample_volume_variable[0])
        self.sample_volume_error_variable.set(df.sample_volume_error_variable[0])

    
    


def run_GUI():
    window_1 = Tk()
    window_1.title('RaDeCC Reader')

    # container = ttk.Frame(window_1)
    # canvas = Canvas(container)
    # scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    # scrollable_frame = ttk.Frame(canvas)
    # scrollable_frame.bind(
    # "<Configure>",
    # lambda e: canvas.configure(
    # scrollregion=canvas.bbox("all")
    #     )
    # )
    # canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # canvas.configure(yscrollcommand=scrollbar.set)
    # canvas.grid(column = 0,row = 0)
    # container.pack()
    # canvas.pack(side="left", fill="both", expand=True)
    # scrollbar.pack(side="right", fill="y")

    # sub_container = ttk.Frame(container)

    app = App(window_1)
    #print (app.equilibration_time_variable.get())
    window_1.mainloop()
    # root.destroy()
    return(app.equilibration_time_variable.get())

print (run_GUI())


