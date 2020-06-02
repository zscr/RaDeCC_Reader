from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from ast import literal_eval
import pandas as pd
import os
import time



def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Error")
    label = ttk.Label(popup, text= msg, padding=(10, 2, 10, 6))
    label.grid(column = 0, row = 0)
    B1 = ttk.Button(popup, text='Close', command = popup.destroy())
    B1.grid(column = 1, row = 0)
    popup.mainloop()


def make_labelled_entry(variable_type, labeltext, labelrow):
    entry_label = Label(
            text = labeltext
        )
    entry_label.grid(column = 0, row = labelrow, sticky=W)

    entry_variable = variable_type
    entry_entry = Entry(
            textvariable=entry_variable
            )
    entry_entry.grid(column = 1, row = labelrow, sticky=W)
    return(entry_variable)


class App:

    def __init__ (self, master):

        self.padx_variable = 20
        ###### Select Saved file Button ##################################################################
        self.load_saved_fields_button = Button(text="Load Saved Entries", command= lambda: self.find_saved_fields_file(1,0) )
        self.load_saved_fields_button.grid(column = 0, row = 0)
        self.load_saved_fields_variable = StringVar()
        self.load_saved_fields_entry = Entry(textvariable = self.load_saved_fields_variable)
        self.load_saved_fields_entry.grid(column = 1, row = 0)
        ######################################################################################
        ###### Choose Input Directory Button ########################################################
        self.input_directory_button = Button(
            master, text="Choose Input Directory...", bg='blue', command=self.find_directory)
        self.input_directory_button.grid(column = 0, row = 1)
        self.input_directory_variable = StringVar()
        self.input_directory_entry = Entry(textvariable = self.input_directory_variable)
        self.input_directory_entry.grid(column = 1, row = 1)
        ######################################################################################
        ###### Select Logsheet Button ##################################################################
        self.load_logsheet = Button(text="Select Logsheet File", command= lambda: self.find_logfile(1,2))
        self.load_logsheet.grid(column = 0, row = 2)
        self.load_logsheet_variable = StringVar()
        self.load_logsheet_entry = Entry(textvariable = self.load_logsheet_variable)
        self.load_logsheet_entry.grid(column = 1, row = 2)
        #########################################################################################
        
        ###### Check Inputs Button ##################################################################
        self.check_inputs = Button(text="Check Inputs", fg='green', command=self.check_all_inputs)
        self.check_inputs.grid(column = 2, row = 0)
        ######################################################################################
        
        

        ###### Choose DDMMYYYY Format ########################################################        
        self.date_format_label = Label(
            master,
            text = 'DDMMYYYY Format for Read Files and Logsheets:'
        )
        self.date_format_label.grid(column = 0, row = 3, sticky=W)

        self.date_format_variable = IntVar()
        c = Checkbutton(
            master,
            variable=self.date_format_variable,
            )
        c.grid(column = 1, row = 3)

        ###### Are there sub-samples? ########################################################
        self.subsample_check_label = Label(
            master,
            text = 'Tick if dataset contains sub-samples:'
        )
        self.subsample_check_label.grid(column = 0, row = 4, sticky=W)

        self.subsample_check_variable = IntVar()
        c = Checkbutton(
            master,
            variable=self.subsample_check_variable,
            )
        c.grid(column = 1, row = 4)

        ###### Spike_sensitivity ########################################################
        self.spike_sensitivity_label = Label(
            text = 'Spike sensitivity:'
        )
        self.spike_sensitivity_label.grid(column = 0, row = 5, sticky=W)
        self.spike_sensitivity_scale = Scale(master, from_=0, to=100, orient=HORIZONTAL)
        self.spike_sensitivity_scale.grid(column = 1, row = 5)

        ###### Equilibration time (minutes) ##############################################
        self.equilibration_time_variable = make_labelled_entry(IntVar(),'Equilibration time (no. of read file intervals):', 6)
        
        ###### Enter sample type name ##############################################
        self.sample_type_name_variable = make_labelled_entry(StringVar(),'Sample type name:', 7)
        
        ###### Number of Samples ##############################################
        self.number_of_samples_variable = make_labelled_entry(IntVar(),'Number of Samples:', 8)

        ###### Thorium-228 Standard File Identifier ##############################################
        self.thstd_identifier_variable = make_labelled_entry(StringVar(),'Thorium-228 Standard File Identifier:', 9)

        ###### Number of Thorium-228 Standards ##############################################
        self.no_of_thstds_variable = make_labelled_entry(IntVar(),'Number of Thorium-228 Standards:', 10)
        
        ###### Actinium-227 Standard File Identifier ##############################################
        self.acstd_identifier_variable = make_labelled_entry(StringVar(),'Actinium-227 Standard File Identifier:', 11)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_acstds_variable = make_labelled_entry(IntVar(),'Number of Actinium-227 Standards:', 12)

        ###### Blank Standard File Identifier ##############################################
        self.blank_identifier_variable = make_labelled_entry(StringVar(),'Blank Standard File Identifier:', 13)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_blanks_variable = make_labelled_entry(IntVar(),'Number of Blank Standards:', 14)

        ###### Number of Detectors ##############################################
        self.no_of_detectors_variable = make_labelled_entry(IntVar(),'Number of Detectors:', 15)
    
        ###### Adjustment Coefficient ##############################################
        self.adjustment_coefficient_variable = make_labelled_entry(DoubleVar(),'Adjustment Coefficient:', 16)

        ###### Adjustment Coefficient Uncertainty ##############################################
        self.adjustment_coefficient_uncertainty_variable = make_labelled_entry(DoubleVar(),'Adjustment Coefficient Uncertainty:', 17)

    def find_directory(self):
    
        self.chosen_query_directory = fd.askdirectory(mustexist = True)
        print (self.chosen_query_directory)
        self.input_directory_text = Label(
            text = self.chosen_query_directory
        )
        self.input_directory_text.grid(column = 1, row = 1)
    
    def find_logfile(self, column_number, row_number):
        self.logfile_to_load = fd.askopenfilename()
        self.logfile_to_load_as_df = pd.read_csv(self.logfile_to_load)
        # print (list(self.logfile_to_load_as_df.columns))
        self.logfile_to_load_label = Label(text = self.logfile_to_load)
        self.logfile_to_load_label.grid(column = column_number, row = row_number)
    
    def find_saved_fields_file(self, column_number, row_number):
        self.saved_fields_file_to_load = fd.askopenfilename()
        self.saved_fields_file_to_load_as_df = pd.read_csv(self.saved_fields_file_to_load)
        self.load_saved_fields_variable.set(self.saved_fields_file_to_load)
        # print (list(self.saved_fields_file_to_load_as_df.columns))
        # self.saved_fields_file_to_load_label = Label(text = self.saved_fields_file_to_load)
        # self.saved_fields_file_to_load_label.grid(column = column_number, row = row_number)
        """Set self.variables from saved_fields_file_to_load_as_df"""
        self.chosen_query_directory = self.saved_fields_file_to_load_as_df.Input_Directory[0]
        self.input_directory_variable.set(self.chosen_query_directory)
        # self.input_directory_text = Label(text = self.chosen_query_directory)
        # self.input_directory_text.grid(column = 1, row = 1)

        self.logfile_to_load = self.saved_fields_file_to_load_as_df.Logsheet_Filepath[0]
        self.load_logsheet_variable.set(self.logfile_to_load)
        # self.logfile_to_load_label = Label(text = self.logfile_to_load)
        # self.logfile_to_load_label.grid(column = 1, row = 2)

        self.date_format_variable.set(self.saved_fields_file_to_load_as_df.DDMMYY_Format[0])
        self.subsample_check_variable.set(self.saved_fields_file_to_load_as_df.sub_sample_variable[0])
        self.spike_sensitivity_scale.set(self.saved_fields_file_to_load_as_df.Spike_sensitivity_variable[0])
        self.equilibration_time_variable.set(self.saved_fields_file_to_load_as_df.Equilibration_time[0])
        self.sample_type_name_variable.set(self.saved_fields_file_to_load_as_df.sample_type_name[0])
        self.number_of_samples_variable.set(self.saved_fields_file_to_load_as_df.number_of_samples[0])
        self.thstd_identifier_variable.set(self.saved_fields_file_to_load_as_df.thorium_228_identifier[0])
        self.no_of_thstds_variable.set(self.saved_fields_file_to_load_as_df.number_of_thorium_stds[0])
        self.acstd_identifier_variable.set(self.saved_fields_file_to_load_as_df.actinium_227_identifier[0])
        self.no_of_acstds_variable.set(self.saved_fields_file_to_load_as_df.number_of_actinium_stds[0])
        self.blank_identifier_variable.set(self.saved_fields_file_to_load_as_df.blank_identifier[0])
        self.no_of_blanks_variable.set(self.saved_fields_file_to_load_as_df.number_of_blanks[0])
        self.no_of_detectors_variable.set(self.saved_fields_file_to_load_as_df.number_of_detectors[0])
        self.adjustment_coefficient_variable.set(self.saved_fields_file_to_load_as_df.adjustment_coefficient[0])
        self.adjustment_coefficient_uncertainty_variable.set(self.saved_fields_file_to_load_as_df.adjustment_coefficient_uncertainty[0])
        
    def check_number_inputs(self, number_variable, column_number, row_number):
        
        try:
            number_variable.get()
            check_label = Label(text = 'OK', fg='green', padx = self.padx_variable)
            check_label.grid(column = column_number, row = row_number)
            return(True)
        except TclError: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Number Required', fg='red')
            check_label.grid(column = column_number, row = row_number)
            return(False)

    def check_string_inputs(self, string_variable, row_number, column_number):
        allowed_chars = list('ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz0123456789_')
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) != 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'OK', fg='green', padx = self.padx_variable)
            check_label.grid(column = column_number, row = row_number)
            return(True)
        
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) == 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'Required Field', fg='red', padx = self.padx_variable)
            check_label.grid(column = column_number, row = row_number)
            return(False)

        else: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Invalid characters entered', fg='red')
            check_label.grid(column = column_number, row = row_number)
            return(False)
 
    def check_all_inputs (self):
        """Input Directory Check"""
        """ saved_fields_file_to_load Check"""
        try: 
            list(self.saved_fields_file_to_load)
            saved_fields_file_to_load_check = True
        except:
            saved_fields_file_to_load_check = False
            self.load_saved_fields_variable.set('Please select...')
            

        try: 
            list(self.chosen_query_directory)
            chosen_query_directory_check = True
        except:
            chosen_query_directory_check = False
            self.input_directory_variable.set('Please select...')
            
        
        """Logsheet Select Check"""
        try: 
            list(self.logfile_to_load)
            logfile_to_load_check = True
        except:
            logfile_to_load_check = False
            self.load_logsheet_variable.set('Please select...')
            

        """Number checks"""
        equilibration_time_variable_check = self.check_number_inputs(self.equilibration_time_variable , column_number=2, row_number=6)
        number_of_samples_variable_check = self.check_number_inputs(self.number_of_samples_variable ,column_number=2, row_number=8)
        no_of_thstds_variable_check = self.check_number_inputs(self.no_of_thstds_variable ,column_number=2, row_number=10)
        no_of_acstds_variable_check = self.check_number_inputs(self.no_of_acstds_variable ,column_number=2, row_number=12)
        no_of_blanks_variable_check = self.check_number_inputs(self.no_of_blanks_variable ,column_number=2, row_number=14)
        no_of_detectors_variable_check = self.check_number_inputs(self.no_of_detectors_variable ,column_number=2, row_number=15)
        adjustment_coefficient_variable_check = self.check_number_inputs(self.adjustment_coefficient_variable ,column_number=2, row_number=16)
        adjustment_coefficient_uncertainty_variable_check = self.check_number_inputs(self.adjustment_coefficient_uncertainty_variable ,column_number=2, row_number=17)
        
        """String checks"""
        # output_directory_variable_check = self.check_string_inputs(self.output_directory_variable, 2)
        # input_directory_text_check = self.check_string_inputs(self.input_directory_text, 0, 2)
        sample_type_name_variable_check = self.check_string_inputs(self.sample_type_name_variable, 7, 2)
        thstd_identifier_variable_check = self.check_string_inputs(self.thstd_identifier_variable, 9, 2)
        acstd_identifier_variable_check = self.check_string_inputs(self.acstd_identifier_variable, 11, 2)
        blank_identifier_variable_check = self.check_string_inputs(self.blank_identifier_variable, 13, 2)

        check_list = [chosen_query_directory_check,
                        logfile_to_load_check,
                        equilibration_time_variable_check,
                        number_of_samples_variable_check,
                        no_of_thstds_variable_check,
                        no_of_acstds_variable_check,
                        no_of_blanks_variable_check,
                        adjustment_coefficient_variable_check,
                        adjustment_coefficient_uncertainty_variable_check,
                        sample_type_name_variable_check,
                        thstd_identifier_variable_check,
                        acstd_identifier_variable_check,
                        blank_identifier_variable_check,
                        no_of_detectors_variable_check]
        
        # popupmsg(str(check_list))

        if False not in check_list:
            
            # self.save_previous_inputs_button = Button(text = "Save Field Inputs", command = lambda : self.save_previous_inputs())
            # self.save_previous_inputs_button.grid(column = 2, row = 3)
            self.run_button = Button(text="Continue", fg='green', command= lambda : self.create_new_entries())
            self.run_button.grid(column = 2, row = 18)
        
        if False in check_list:
            self.run_button = Button(text="Continue", fg='grey', command=lambda : popupmsg('Errors apparent'))
            self.run_button.grid(column = 2, row = 18)

    def save_previous_inputs(self):

        save_dict = {
            'Input_Directory':[self.chosen_query_directory],
            'Loaded_Fields_File': [self.saved_fields_file_to_load],
            'Logsheet_Filepath': [self.logfile_to_load],
            'DDMMYY_Format': [self.date_format_variable.get()],
            'sub_sample_variable':[self.subsample_check_variable.get()],
            'Spike_sensitivity_variable':[self.spike_sensitivity_scale.get()],
            'Equilibration_time':[self.equilibration_time_variable.get()],
            'sample_type_name':[self.sample_type_name_variable.get()],
            'number_of_samples':[self.number_of_samples_variable.get()],
            'thorium_228_identifier':[self.thstd_identifier_variable.get()],
            'number_of_thorium_stds':[self.no_of_thstds_variable.get()],
            'actinium_227_identifier':[self.acstd_identifier_variable.get()],
            'number_of_actinium_stds':[self.no_of_acstds_variable.get()],
            'blank_identifier':[self.blank_identifier_variable.get()],
            'number_of_blanks':[self.no_of_blanks_variable.get()],
            'number_of_detectors':[self.no_of_detectors_variable.get()],
            'adjustment_coefficient':[self.adjustment_coefficient_variable.get()],
            'adjustment_coefficient_uncertainty':[self.adjustment_coefficient_uncertainty_variable.get()],
            'th228_standard_manufacture_date_dict':[self.th228_standard_manufacture_date_dict],
            'th228_standard_start_activities_dict':[self.th228_standard_start_activity_dict],
            'ac227_standard_manufacture_date_dict':[self.ac227_standard_manufacture_date_dict],
            'ac227_standard_start_activities_dict':[self.ac227_standard_start_activity_dict],
            'blank_standard_names_list':[self.blank_standard_names_list],
            'detector_calibration_values_dict':[self.detector_dict]
        }
        save_df = pd.DataFrame.from_dict(save_dict, orient = 'columns')
        save_df.to_csv(os.path.join(self.chosen_query_directory,'radecc_reader_entries_'+time.strftime("%H%M%S_%Y-%m-%d")+'.csv'))
        print ('Saved')
        
        return()

    def create_new_entries(self):
        # window_2 = Tk()
        # window_2.title('RaDeCC Reader')
        # label = Label(window_2, text = 'This is window 2')
        # label.grid()
        extra_padding = 10
        ###### Load Button ##################################################################
        self.load_saved_fields_button = Button(text="Load Saved Entries", command= lambda: self.load_new_entries() )
        self.load_saved_fields_button.grid(column = 4, row = 0)
        #####################################################################################
        self.th228_entries_start_row = 1
        self.th228_standard_name_label = Label(text = 'Thorium_228 Standard Name:', fg = 'black', padx = self.padx_variable)
        self.th228_standard_name_label.grid(column = 4, row = self.th228_entries_start_row)
        '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        self.th228_standard_name_widget_list = self.make_entry_widget_list( column_number = 4, start_row = 1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'String')
        # print('###############',type(self.th228_standard_name_widget_list[0].get()))
        
        self.th228_standard_manufacture_date_label = Label(text = 'Manufacture Date:', fg = 'black', padx = self.padx_variable+extra_padding+3)
        self.th228_standard_manufacture_date_label.grid(column = 5, row = self.th228_entries_start_row)
        '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        self.th228_standard_manufacture_date_widget_list = self.make_entry_widget_list(column_number = 5, start_row = 1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'String')
        
        self.th228_standard_start_activity_label = Label(text = 'Start Activity (dpm):', fg = 'black', padx = self.padx_variable+extra_padding)
        self.th228_standard_start_activity_label.grid(column = 6, row = self.th228_entries_start_row)
        '''Create a list of [[entry_widget, entry_widget_variable],...]'''
        self.th228_standard_start_activity_widget_list = self.make_entry_widget_list(column_number = 6, start_row = 1, number_of_widgets =  self.no_of_thstds_variable.get(), var_type = 'Double')
        
        self.ac227_entries_start_row = self.no_of_thstds_variable.get()+1
        
        self.ac227_standard_name_label = Label(text = 'Actinium-227 Standard Name:', fg = 'black', padx = self.padx_variable+extra_padding)
        self.ac227_standard_name_label.grid(column = 4, row = self.ac227_entries_start_row)
        self.ac227_standard_name_widget_list = self.make_entry_widget_list(column_number = 4, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'String')
        
        self.ac227_standard_manufacture_date_label = Label(text = 'Manufacture Date:', fg = 'black', padx = self.padx_variable+extra_padding+3)
        self.ac227_standard_manufacture_date_label.grid(column = 5, row = self.no_of_thstds_variable.get()+1)
        self.ac227_standard_manufacture_date_widget_list = self.make_entry_widget_list(column_number = 5, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'String')
        
        self.ac227_standard_start_activity_label = Label(text = 'Start Activity (dpm):', fg = 'black', padx = self.padx_variable+extra_padding)
        self.ac227_standard_start_activity_label.grid(column = 6, row = self.no_of_thstds_variable.get()+1)
        self.ac227_standard_start_activity_widget_list = self.make_entry_widget_list(column_number = 6, start_row = self.ac227_entries_start_row+1, number_of_widgets =  self.no_of_acstds_variable.get(), var_type = 'Double')
        
        self.blank_entries_start_row = self.ac227_entries_start_row+self.no_of_acstds_variable.get()+1
        self.blank_standard_name_label = Label(text = 'Blank Standard Name:', fg = 'black', padx = self.padx_variable+extra_padding)
        self.blank_standard_name_label.grid(column = 4, row = self.blank_entries_start_row)
        self.blank_standard_name_widget_list = self.make_entry_widget_list(column_number = 4, start_row = self.blank_entries_start_row+1, number_of_widgets =  self.no_of_blanks_variable.get(), var_type = 'String')

        self.detector_entries_start_row = self.blank_entries_start_row+self.no_of_blanks_variable.get()+1
        self.detector_name_label = Label(text = 'Detector Name:', fg = 'black', padx = self.padx_variable+extra_padding+6)
        self.detector_name_label.grid(column = 4, row = self.detector_entries_start_row)
        self.detector_name_widget_list = self.make_entry_widget_list(column_number = 4, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'String')

        self.detector_calibration_values_label = Label(text = '226Ra Calibration Value:', fg = 'black', padx = self.padx_variable)
        self.detector_calibration_values_label.grid(column = 5, row = self.detector_entries_start_row)
        self.detector_calibration_values_widget_list = self.make_entry_widget_list(column_number = 5, start_row = self.detector_entries_start_row+1, number_of_widgets =  self.no_of_detectors_variable.get(), var_type = 'Double')



        ###### Check Inputs Button No.2 ##################################################################
        self.check_inputs = Button(text="Check Inputs", fg='green', 
                                    command= lambda: self.check_all_new_entries())
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
            # variable_list.append(StringVar())
            entry_list.append( Entry(textvariable = variable_list[-1], width = 21))
            entry_list[-1].grid(column = column_number, row = i)
            widget_list.append([entry_list[-1],variable_list[-1]])

        return(widget_list)
    
    def check_widget_list_set (self, list_of_name_widgets, list_of_date_widgets, column_number, row_number):
        check_list = []
        name_check_list = []
        for i in range(len(list_of_name_widgets)):
                name_check_list.append(self.check_string_inputs(string_variable = list_of_name_widgets[i][1], row_number = row_number, column_number = column_number))
        name_check_boolean = all(name_check_list)
        date_check_boolean = self.date_string_list_check(list_of_date_widgets, row_number = row_number+1, column_number = column_number)

        return(all([name_check_boolean, date_check_boolean]))

    def date_string_list_check (self, date_list_to_check, column_number, row_number):
        
        if  'N/A' not in date_list_to_check:
            check_list = []
            for i in range(len(date_list_to_check)):
            
                if '/' in date_list_to_check[i][1].get():
                    try:
                        pd.to_datetime(date_list_to_check[i][1].get())
                        check_list.append(True)
                    except:
                        check_list.append(False)
                else:
                    check_list.append(False)
        
            if all(check_list) == True:
                check_label = Label(text = 'OK', fg='green', padx = self.padx_variable+5)
                check_label.grid(column = column_number, row = row_number)
                return(True)
            else:
                check_label = Label(text = 'Date Error', fg='red', padx = self.padx_variable)
                check_label.grid(column = column_number, row = row_number)
                return(False)
        if 'N/A' in date_list_to_check:
            return(True)
        # if :
        #     check_label = Label(text = '    ', padx = self.padx_variable)
        #     check_label.grid(column = column_number, row = row_number)
        #     return(True)

    def check_all_new_entries (self):

        """Check Thorium-228 standard Entries"""
        th228_standard_entries_boolean = self.check_widget_list_set(self.th228_standard_name_widget_list, self.th228_standard_manufacture_date_widget_list, 
                                                                                column_number = 7, row_number = 1)
        """Check Actinium-227 standard Entries"""
        ac227_standard_entries_boolean = self.check_widget_list_set(self.ac227_standard_name_widget_list, self.ac227_standard_manufacture_date_widget_list, 
                                                                                column_number = 7, row_number = self.ac227_entries_start_row+1)
        """Check Blank Entries"""
        blank_entries_boolean = self.check_widget_list_set(self.blank_standard_name_widget_list, 'N/A', 
                                                                                column_number = 7, row_number = self.blank_entries_start_row+1)
        """Detector Entries"""
        detector_names_boolean_list = []
        for i in range(len(self.detector_name_widget_list)):
            detector_names_boolean_list.append(self.check_string_inputs(string_variable = self.detector_name_widget_list[i][1], 
                                                                                row_number = self.detector_entries_start_row+1, column_number = 7))

        all_new_entries_boolean = all([th228_standard_entries_boolean, ac227_standard_entries_boolean,blank_entries_boolean,detector_names_boolean_list])

        if all_new_entries_boolean is True:
            
            self.th228_standard_manufacture_date_dict = dict(zip([x[1].get() for x in self.th228_standard_name_widget_list], [x[1].get() for x in self.th228_standard_manufacture_date_widget_list]))
            self.th228_standard_start_activity_dict = dict(zip([x[1].get() for x in self.th228_standard_name_widget_list], [x[1].get() for x in self.th228_standard_start_activity_widget_list]))
            
            self.ac227_standard_manufacture_date_dict = dict(zip([x[1].get() for x in self.ac227_standard_name_widget_list], [x[1].get() for x in self.ac227_standard_manufacture_date_widget_list]))
            self.ac227_standard_start_activity_dict = dict(zip([x[1].get() for x in self.ac227_standard_name_widget_list], [x[1].get() for x in self.ac227_standard_start_activity_widget_list]))
            
            self.blank_standard_names_list = [x[1].get() for x in self.blank_standard_name_widget_list]

            self.detector_dict = dict(zip([x[1].get() for x in self.detector_name_widget_list], [x[1].get() for x in self.detector_calibration_values_widget_list]))
            
            ###### Save Inputs Button No.2 ##################################################################
            self.save_previous_inputs_button_2 = Button(text = "Save Field Inputs", command = lambda : self.save_previous_inputs())
            self.save_previous_inputs_button_2.grid(column = 7, row = self.detector_entries_start_row+self.no_of_detectors_variable.get()+1)
            #################################################################################################
            print('yay.')



        if all_new_entries_boolean is False:
            print('nay.', [th228_standard_entries_boolean, ac227_standard_entries_boolean,blank_entries_boolean,detector_names_boolean_list])

    def load_new_entries (self):
        df = self.saved_fields_file_to_load_as_df
        '''load th228_fields'''
        th228_standard_names_list = list(literal_eval(df.th228_standard_manufacture_date_dict[0]).keys())
        th228_standard_manufacture_date_list = list(literal_eval(df.th228_standard_manufacture_date_dict[0]).values())
        th228_standard_start_activity_list = list(literal_eval(df.th228_standard_start_activities_dict[0]).values())

        for i in range(len(self.th228_standard_name_widget_list)):
            self.th228_standard_name_widget_list[i][1].set(th228_standard_names_list[i])
            self.th228_standard_manufacture_date_widget_list[i][1].set(th228_standard_manufacture_date_list[i])
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

        for i in range(len(detector_names_list)):
            self.detector_name_widget_list[i][1].set(detector_names_list[i])
            self.detector_calibration_values_widget_list[i][1].set(detector_calibration_values_list[i])
        


def run_GUI():
    window_1 = Tk()
    window_1.title('RaDeCC Reader')
    app = App(window_1)
    #print (app.equilibration_time_variable.get())
    window_1.mainloop()
    # root.destroy()
    return(app.equilibration_time_variable.get())

print (run_GUI())



