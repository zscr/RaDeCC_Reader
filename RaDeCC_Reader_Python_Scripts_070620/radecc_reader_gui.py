from tkinter import *

class App:

    def __init__ (self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text = 'Quit', fg='red', command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Print", fg='green', command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.var = IntVar()
        c = Checkbutton(
            master, text="On/Off",
            variable=self.var,
            )
        c.pack()

    def cb(self, event):
        print ("variable is", self.var.get())
    
    def say_hi (self):
        if self.var.get() == 1:
            print('On')
        if self.var.get() == 0:
            print('Off')

root = Tk()
app = App(root)

root.mainloop()
#root.destroy()



