from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd



def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Error")
    label = ttk.Label(popup, text= msg)
    label.grid(column = 0, row = 0)
    # B1 = ttk.Button(popup, text='Close', command = command_arg)
    # B1.grid(column = 1, row = 0)
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

        # frame = Frame(master)
        # frame.grid()


        ###### Check Inputs ##################################################################
        self.check_inputs = Button(text="Check Inputs", fg='green', command=self.check_inputs)
        self.check_inputs.grid(column = 2, row = 0)
        ######################################################################################
        
        # self.run_button = Button(text="Run", fg='grey', command=popupmsg('We are clear for take-off'))
        # self.run_button.grid(column = 2, row = 18)

        ###### Choose Input Directory ########################################################
        self.input_directory_button = Button(
            master, text="Choose Input Directory...", bg='blue', command=self.find_directory)
        self.input_directory_button.grid(column = 0, row = 0)
        
        ###### Enter output folder and filename ##############################################
        self.output_directory_variable = make_labelled_entry(StringVar(),'Output folder name:', 2)
        self.output_file_variable = make_labelled_entry(StringVar(),'Output summary file name:', 3)

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
            text = 'Tick if dataset contains sub-samples:'
        )
        self.subsample_check_label.grid(column = 0, row = 5, sticky=W)

        self.subsample_check_variable = IntVar()
        c = Checkbutton(
            master,
            variable=self.subsample_check_variable,
            )
        c.grid(column = 1, row = 5)

        ###### Spike_sensitivity ########################################################
        self.spike_sensitivity_label = Label(
            text = 'Spike sensitivity:'
        )
        self.spike_sensitivity_label.grid(column = 0, row = 6, sticky=W)
        self.spike_sensitivity_scale = Scale(master, from_=0, to=100, orient=HORIZONTAL)
        self.spike_sensitivity_scale.grid(column = 1, row = 6)

        ###### Equilibration time (minutes) ##############################################
        self.equilibration_time_variable = make_labelled_entry(IntVar(),'Equilibration time (minutes):', 7)
        
        ###### Enter sample type name ##############################################
        self.sample_type_name_variable = make_labelled_entry(StringVar(),'Sample type name:', 8)
        
        ###### Number of Samples ##############################################
        self.number_of_samples_variable = make_labelled_entry(IntVar(),'Number of Samples:', 9)

        ###### Thorium-228 Standard File Identifier ##############################################
        self.thstd_identifier_variable = make_labelled_entry(StringVar(),'Thorium-228 Standard File Identifier:', 10)

        ###### Number of Thorium-228 Standards ##############################################
        self.no_of_thstds_variable = make_labelled_entry(IntVar(),'Number of Thorium-228 Standards:', 11)
        
        ###### Actinium-227 Standard File Identifier ##############################################
        self.acstd_identifier_variable = make_labelled_entry(StringVar(),'Actinium-227 Standard File Identifier:', 12)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_acstds_variable = make_labelled_entry(IntVar(),'Number of Actinium-227 Standards:', 13)

        ###### Blank Standard File Identifier ##############################################
        self.acstd_identifier_variable = make_labelled_entry(StringVar(),'Blank Standard File Identifier:', 14)

        ###### Number of Actinium-227 Standards ##############################################
        self.no_of_blanks_variable = make_labelled_entry(IntVar(),'Number of Blank Standards:', 15)
    
        ###### Adjustment Coefficient ##############################################
        self.adjustment_coefficient_variable = make_labelled_entry(IntVar(),'Adjustment Coefficient:', 16)

        ###### Adjustment Coefficient Uncertainty ##############################################
        self.adjustment_coefficient_uncertainty_variable = make_labelled_entry(IntVar(),'Adjustment Coefficient Uncertainty:', 17)


    def find_directory(self):
    
        chosen_query_directory = fd.askdirectory(mustexist = True)
        print (chosen_query_directory)
        self.input_directory_text = Label(
            text = chosen_query_directory
        )
        self.input_directory_text.grid(column = 1, row = 0)

    def check_number_inputs(self, number_variable, row_number):
        
        try:
            number_variable.get()
            check_label = Label(text = 'Good', fg='green', padx = 100)
            check_label.grid(column = 2, row = row_number)
            return(True)
        except TclError: # if the conversion fails due to it containing letters
            check_label = Label(text = 'Number Required', fg='red')
            check_label.grid(column = 2, row = row_number)
            return(False)
 
    def check_inputs (self):
        
        equilibration_time_variable_check = self.check_number_inputs(self.equilibration_time_variable , 7)
        number_of_samples_variable_check = self.check_number_inputs(self.number_of_samples_variable , 9)
        no_of_thstds_variable_check = self.check_number_inputs(self.no_of_thstds_variable , 11)
        no_of_acstds_variable_check = self.check_number_inputs(self.no_of_acstds_variable , 13)
        no_of_blanks_variable_check = self.check_number_inputs(self.no_of_blanks_variable , 15)
        adjustment_coefficient_variable_check = self.check_number_inputs(self.adjustment_coefficient_variable , 16)
        adjustment_coefficient_uncertainty_variable_check = self.check_number_inputs(self.adjustment_coefficient_uncertainty_variable , 17)

        check_list = [equilibration_time_variable_check,
                        number_of_samples_variable_check,
                        no_of_thstds_variable_check,
                        no_of_acstds_variable_check,
                        no_of_blanks_variable_check,
                        adjustment_coefficient_variable_check,
                        adjustment_coefficient_uncertainty_variable_check]
        
        # popupmsg(str(check_list))

        if False not in check_list:
            self.run_button = Button(root, text="Run RaDeCC Reader", fg='green', command= lambda : print ('go'))
            self.run_button.grid(column = 2, row = 18)
        
        if False in check_list:
            self.run_button = Button(root, text="Run RaDeCC Reader", fg='grey', command=lambda : print ('Errors apparent'))
            self.run_button.grid(column = 2, row = 18)

             


# popup = Tk()
# popup.wm_title('RaDeCC Reader')
# label = ttk.Label(popup, text= "Welcome to RaDeCC Reader\nWritten by Sean Selzer")
# label.grid(column = 0, row = 0)
# B1 = ttk.Button(popup, text='Continue', command = popup.destroy)
# B1.grid(column = 1, row = 0)
# popup.mainloop()

root = Tk()
root.title('RaDeCC Reader')
app = App(root)


root.mainloop()
root.destroy()



