import eel
import scripts.retrieveData as rd
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog


eel.init('web')

@eel.expose
def helloPy():
    return "Hello from Python"

@eel.expose
def autocheckMe():
    rd.init()
    return(rd.returnData())

@eel.expose
def fileLocationSub():
    root = Tk()
    root.title("Autograder")
    root.geometry("1x1")
    
    folderName = tkFileDialog.askdirectory()
    root.withdraw()   
    rd.setSubDir(folderName)

    return folderName

@eel.expose
def fileLocationTest():
    root = Tk()
    root.title("Autograder")
    root.geometry("1x1")
    
    folderName = tkFileDialog.askdirectory()
    root.withdraw()   
    rd.setTestDir(folderName)

    return folderName


eel.start('index.html', size=(1000,600))
