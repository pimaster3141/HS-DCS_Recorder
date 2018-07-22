# -*- coding: utf-8 -*-
"""
GUI for HS-DCS Module "Chales 1.0"

Created on Sat Jul 21 23:04:22 2018
@author: Alexander Ruesch, Jason Yang
"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog, simpledialog
from tkinter import ttk
import runner
import time
from datetime import timedelta
import os.path
from os.path import expanduser

class HSDCS():
    def __init__(self, master):
        # variables
        self.master = master
        self.tick = 500
        
        self.hasStarted = 0
        self.elapsedTime = 0
        self.startTime = 0
        
        self.fname = ''
        
        #start window
        master.title("Charles 1.0 (HS-DCS)")
        master.minsize(width=300, height=100)
        
        # *** MENU ***
        self.menu = Menu(master)
        master.config(menu=self.menu)
        # -------------------------------------------------------------------
        self.subMenu = Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.subMenu)
        self.subMenu.add_command(label="Exit",command=self.quit)

        # -------------------------------------------------------------------    
        
        # *** Toolbar ***
        self.toolbar = Frame(master)
        self.startButt = Button(self.toolbar, text="Start", command=self.start, state='disabled')
        self.startButt.pack(side=LEFT, padx=2, pady=2)
        self.stopButt =  Button(self.toolbar, text="Stop", command=self.stop, state='disabled')
        self.stopButt.pack(side=LEFT, padx=2, pady=2)
        self.saveasButt = Button(self.toolbar, text="Save as...", command=self.save_as, state='normal')
        self.saveasButt.pack(side=LEFT, padx=2, pady=2)
        self.Timer = Label(self.toolbar, text="00:00:00")
        self.Timer.pack(side=RIGHT, padx=4, pady=2)
        
        self.toolbar.pack(side=TOP, fill=X)


        # *** Saves ***
        self.saveOption = Frame(master)
        self.L1 = Label(self.saveOption, text="File Name")
        self.L1.pack(side=LEFT)
        self.textbox = Entry(self.saveOption, width = 30)
        self.textbox.pack(side=LEFT, fill=X, expand=NO)
        self.saveButt =  Button(self.saveOption, text="Save", command=self.save, state='normal')
        self.saveButt.pack(side=LEFT, padx=2, pady=2)
        
        self.saveOption.pack(side=TOP, fill=X)
        
        # *** Status Bar ***
        self.status = Label(master, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        master.after(self.tick,self.runExperiment)
        
        # *** Key Binding ***
        self.textbox.bind('<Return>', self.save)

        
#    def __del__(self):
      

    def quit(self):
        self.master.destroy()


    def save(self,event=None):
        if self.hasStarted == 0:
            home = os.path.dirname(os.path.realpath('.'))
            fname = self.textbox.get() 
            fname = home+os.sep+"data"+os.sep+fname
            
            fname, ext = os.path.splitext(fname)
            fname = fname + '.txt'
                
            if os.path.isfile(fname):       
                print("File already exists. Try again.")
            else:
                self.status['text']='File: ' + fname
                self.fname = fname
                self.startButt['state'] = 'normal'

    def save_as(self):
        if self.hasStarted == 0:
            fname = filedialog.asksaveasfilename(filetypes=[('text files', '.txt'),('all files', '.*')], defaultextension=".txt")
            if fname is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            else:
                fname, ext = os.path.splitext(fname)
                fname = fname + '.txt'
                
                self.fname = fname
                self.status['text']='File: ' + fname
                self.startButt['state']='normal'
            
    def start(self):
        if self.hasStarted == 0:
            self.filename = ''
            self.hasStarted = 1
            self.startButt['state'] = 'disabled'
            self.saveButt['state'] = 'disabled'
            self.saveasButt['state'] = 'disabled'
            self.textbox['state'] = 'disabled'
            self.elapsedTime = 0
            self.stopButt['state'] = 'normal'
            self.startTime = time.time()
            try:
#                runner.start(self.fname)
                runner.start(None,dummy=True)
            except: 
                self.status['text']='Unable to start DCS. Abort.'
                self.stopButt['state'] = 'disabled'
                self.startButt['state'] = 'normal'
                self.saveButt['state'] = 'normal'
                self.saveasButt['state'] = 'normal'
                self.textbox['state'] = 'normal'
                self.hasStarted = 0 
                
    def stop(self):
        if self.hasStarted == 1:
            runner.stop()
            self.stopButt['state'] = 'disabled'
            self.startButt['state'] = 'normal'
            self.saveButt['state'] = 'normal'
            self.saveasButt['state'] = 'normal'
            self.textbox['state'] = 'normal'
            self.hasStarted = 0
        
    def clock(self):
        self.elapsedTime = time.time() - self.startTime
        self.Timer['text'] = timedelta(seconds=int(self.elapsedTime))             

     #------- MAIN LOOP --------
    def runExperiment(self):
        if self.hasStarted: 
            self.clock()
        self.master.after(self.tick,self.runExperiment)
        
##########################################################################
# -------------------------- HELPER FUNC --------------------------------#
##########################################################################

#
#def serial_ports():
#    """ Lists serial port names
#
#        :raises EnvironmentError:
#            On unsupported or unknown platforms
#        :returns:
#            A list of the serial ports available on the system
#    """
#    if sys.platform.startswith('win'):
#        ports = ['COM%s' % (i + 1) for i in range(256)]
#    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#        # this excludes your current terminal "/dev/tty"
#        ports = glob.glob('/dev/tty[A-Za-z]*')
#    elif sys.platform.startswith('darwin'):
#        ports = glob.glob('/dev/tty.*')
#    else:
#        raise EnvironmentError('Unsupported platform')
#
#    result = []
#    for port in ports:
#        try:
#            s = serial.Serial(port)
#            s.close()
#            result.append(port)
#        except (OSError, serial.SerialException):
#            pass
#    return result


##########################################################################
# -------------------------- RUN PROGRAM --------------------------------#
##########################################################################

root = Tk()  
app = HSDCS(root)
root.mainloop()
del app

# code.interact(local=locals())