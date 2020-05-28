from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
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

        ###### Select Saved file Button ##################################################################
        self.load_saved_fields_button = Button(text="Load Saved Entries", command= lambda: self.find_saved_fields_file(1,0) )
        self.load_saved_fields_button.grid(column = 0, row = 0)
        ######################################################################################
        ###### Choose Input Directory Button ########################################################
        self.input_directory_button = Button(
            master, text="Choose Input Directory...", bg='blue', command=self.find_directory)
        self.input_directory_button.grid(column = 0, row = 1)
        ######################################################################################
        ###### Select Logsheet Button ##################################################################
        self.load_logsheet = Button(text="Select Logsheet File", command= lambda: self.find_logfile(1,2))
        self.load_logsheet.grid(column = 0, row = 2)
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
        # print (list(self.saved_fields_file_to_load_as_df.columns))
        self.saved_fields_file_to_load_label = Label(text = self.saved_fields_file_to_load)
        self.saved_fields_file_to_load_label.grid(column = column_number, row = row_number)
        """Set self.variables from saved_fields_file_to_load_as_df"""
        self.chosen_query_directory = self.saved_fields_file_to_load_as_df.Input_Directory[0]
        self.input_directory_text = Label(text = self.chosen_query_directory)
        self.input_directory_text.grid(column = 1, row = 1)

        self.logfile_to_load = self.saved_fields_file_to_load_as_df.Logsheet_Filepath[0]
        self.logfile_to_load_label = Label(text = self.logfile_to_load)
        self.logfile_to_load_label.grid(column = 1, row = 2)

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
        
    def check_number_inputs(self, number_variable, row_number):
        
        try:
            number_variable.get()
            check_label = Label(text = 'OK', fg='green', padx = 100)
            check_label.grid(column = 2, row = row_number)
            return(True)
        except TclError: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Number Required', fg='red')
            check_label.grid(column = 2, row = row_number)
            return(False)

    def check_string_inputs(self, string_variable, row_number, column_number):
        allowed_chars = list('ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz0123456789_')
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) != 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'OK', fg='green', padx = 100)
            check_label.grid(column = column_number, row = row_number)
            return(True)
        
        if  len(set(allowed_chars+list(string_variable.get()))) == 61 and len(list(string_variable.get())) == 0 :
            # print (len(set(allowed_chars+list(string_variable.get()))))
            check_label = Label(text = 'Required Field', fg='red', padx = 100)
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
            self.saved_fields_file_to_load_text = Label(text = 'Please select', fg = 'red')
            self.saved_fields_file_to_load_text.grid(column = 1, row = 0)

        try: 
            list(self.chosen_query_directory)
            chosen_query_directory_check = True
        except:
            chosen_query_directory_check = False
            self.input_directory_text = Label(text = 'Please select', fg = 'red')
            self.input_directory_text.grid(column = 1, row = 1)
        
        """Logsheet Select Check"""
        try: 
            list(self.logfile_to_load)
            logfile_to_load_check = True
        except:
            logfile_to_load_check = False
            self.logfile_to_load_text = Label(text = 'Please select', fg = 'red')
            self.logfile_to_load_text.grid(column = 1, row = 2)

        """Number checks"""
        equilibration_time_variable_check = self.check_number_inputs(self.equilibration_time_variable , 6)
        number_of_samples_variable_check = self.check_number_inputs(self.number_of_samples_variable , 8)
        no_of_thstds_variable_check = self.check_number_inputs(self.no_of_thstds_variable , 10)
        no_of_acstds_variable_check = self.check_number_inputs(self.no_of_acstds_variable , 12)
        no_of_blanks_variable_check = self.check_number_inputs(self.no_of_blanks_variable , 14)
        no_of_detectors_variable_check = self.check_number_inputs(self.no_of_detectors_variable , 15)
        adjustment_coefficient_variable_check = self.check_number_inputs(self.adjustment_coefficient_variable , 16)
        adjustment_coefficient_uncertainty_variable_check = self.check_number_inputs(self.adjustment_coefficient_uncertainty_variable , 17)
        
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
            
            self.save_previous_inputs_button = Button(text = "Save Field Inputs", command = lambda : self.save_previous_inputs())
            self.save_previous_inputs_button.grid(column = 2, row = 3)
            self.run_button = Button(text="Run RaDeCC Reader", fg='green', command= lambda : self.open_window_2())
            self.run_button.grid(column = 2, row = 18)
        
        if False in check_list:
            self.run_button = Button(text="Run RaDeCC Reader", fg='grey', command=lambda : popupmsg('Errors apparent'))
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
            'adjustment_coefficient_uncertainty':[self.adjustment_coefficient_uncertainty_variable.get()]
        }
        save_df = pd.DataFrame.from_dict(save_dict, orient = 'columns')
        save_df.to_csv(os.path.join(self.chosen_query_directory,'radecc_reader_entries_'+time.strftime("%H%M%S_%Y-%m-%d")+'.csv'))
        print ('Saved')
        
        return()
    def open_window_2(self):
        window_2 = Tk()
        label = Label(window_2, text = 'This is window 2')
        label.grid()

# popup = Tk()
# popup.wm_title('RaDeCC Reader')
# label = ttk.Label(popup, text= "Welcome to RaDeCC Reader\nWritten by Sean Selzer")
# label.grid(column = 0, row = 0)
# B1 = ttk.Button(popup, text='Continue', command = popup.destroy)
# B1.grid(column = 1, row = 0)
# popup.mainloop()

def run_GUI():
    window_1 = Tk()
    window_1.title('RaDeCC Reader')
    app = App(window_1)
    #print (app.equilibration_time_variable.get())
    window_1.mainloop()
    # root.destroy()
    return(app.equilibration_time_variable.get())

print (run_GUI())



