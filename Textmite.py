import csv
from ntpath import basename
from tkinter import Tk, Menu, Label, Button, StringVar, filedialog, ttk, messagebox
from os import path, makedirs, pardir
from datetime import date

def version():
    return "0.0.1"

def replaceInstances(text, filename, filelist):
    global replacements
    replaced = 0
    for r in replacements:
        if (text.count(r[0]) > 0):
            replaced += 1
            text = text.replace(r[0], r[1])
    filelist.append("Made " + str(replaced) + " replacements in " + filename)
    return (text, filelist)

def saveSampleFile():
    sampleFile = filedialog.asksaveasfilename(defaultextension=".csv")
    try:
        with open(sampleFile, 'w') as csvfile:
            csvOut = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
            csvOut.writerows([["Current Text", "Replacement Text"]])
    except FileNotFoundError:
        return False
    
def openReplacements():
    global replacements
    replacementFile = filedialog.askopenfilename(initialdir=path.abspath('..'),
       filetypes =(("Text File", "*.csv"),("All Files","*.*")),
       title = "Select Files"
       )
    try:
        with open(replacementFile, 'r') as infile:
            reader = csv.reader(infile)
            replacements = list(reader)
            del replacements[0]
            messagebox.showinfo("Results", "Found " + str(len(replacements)) + " replacements to make")
        pickSources()
    except FileNotFoundError:
        return False

def openFiles():
    files = []
    rawFiles = filedialog.askopenfilenames(initialdir=path.abspath('..'),
       filetypes =(("Text File", "*.txt"),("All Files","*.*")),
       title = "Select Files"
       )
    files = window.tk.splitlist(rawFiles)
    fileList = []
    for f in files:
        try:
            with open(f, 'r+') as file:
                text, fileList = replaceInstances(file.read(), basename(f), fileList)
                file.seek(0)
                file.write(text)
                file.truncate()
        except IndentationError:
            print("No file exists")
    messagebox.showinfo("Results", "\n".join(fileList))

def pickSources():
    global labelText, button, sampleButton, srcButton, endButton
    labelText.set("Now choose the text files you wish to process.")
    button.pack_forget()
    sampleButton.pack_forget()
    srcButton.pack()
    endButton.pack()

replacements = []
window = Tk()
window.title("Textmite  |  v" + version())
labelText = StringVar()
labelText.set("Select the CSV file containing the replacements you wish to make. If you\ndon't have one, save the sample file and fill it out before continuing.")
label = Label(window, textvariable=labelText)
sampleButton = Button(window, text="Save Sample File", width=15, command=saveSampleFile)
button = Button(window, text="Import", width=15, command=openReplacements)
srcButton = Button(window, text="Pick Files", width=15, command=openFiles)
endButton = Button(window, text="Exit", width=15, command=window.destroy)
label.pack()
sampleButton.pack()
button.pack()
window.mainloop()