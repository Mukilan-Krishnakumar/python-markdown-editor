import os,markdown,webbrowser
from tkinter import *
from tkinter import filedialog
from sys import platform
from tkhtmlview import HTMLLabel

def FrameSetup():                           #This program sets up the SaveFrame & Textbox
    global SaveFrame,TextBox                #FrameSetup cannot host the butttons because they are being packed individually according to the function's needs
    SaveFrame = Frame(root)
    TextBox = Text(root, height=40, width=40)
  
def mainDisplay():                          #This function sets up the main screen
    global MainFrame,NewWindow              
    MainFrame = Frame(root)                 #MainFrame is the frame in which buttons are hosted
    MainFrame.grid()                        #.grid() places the widget in grid system
    New = Button(MainFrame,text="New",command = newButton) # New Button opens new file
    Open = Button(MainFrame,text="Open",command = openButton) # Open Button opens existing file
    New.grid(row=0,column = 0)
    Open.grid(row=1,column = 0)
    NewWindow = Toplevel()                  #This toplevel opens a new window for markdown editor
    NewWindow.title("Markdown Editor")
    FrameSetup()

def markdownViewer(fileName):               #This function shows the markdown editor
    global NewWindow
    NewWindow.destroy()                     #This destroys the previous toplevel
    with open(fileName,'r') as f:
        text = f.read()
        html = markdown.markdown(text,extensions=['wikilinks']) #This line converts the markdown in file to html
    NewWindow = Toplevel()                         #This is the new toplevel
    html_label = HTMLLabel(NewWindow, html=html)   #This line opens shows the html rendered in new toplevel
    html_label.grid(sticky = "NSEW")               #NSEW extends the label to all quadrants i.e., North South East West

def newButton():                                   #This function is called whenever New Button is clicked
    global SaveFrame,TextBox
    save_button = Button(SaveFrame,text = "Save",command = save)        # Initialization of Save Button
    saveAs_button = Button(SaveFrame,text = "Save As",command = saveAs) # Initialization of Save As Button
    quitButton = Button(SaveFrame,text = "Quit",command = QuitButton)   # Initialization of Quit Button
    MainFrame.destroy()                                                 # Destroys the MainFrame i.e., removes New and Open Button
    root.title("New")
    SaveFrame.grid(row = 0,column = 0,sticky = "NS")                    # First Initialization of SaveFrame
    TextBox.grid(row = 0,column = 1,rowspan = 2)                        # First Initialization of TextBox
    save_button.pack()                                                  # Packing of Buttons
    saveAs_button.pack()
    quitButton.pack()

def openButton():                                                       # This function is called whenever Open Button is clicked
    global SaveFrame,TextBox,openFileName,data                          
    MainFrame.destroy()
    openSave_button = Button(SaveFrame,text = "Save",command = lambda : openSave()) # Initialization of Save Button
    saveAs_button = Button(SaveFrame,text = "Save As",command = saveAs)             # Initialization of Save As Button
    quitButton = Button(SaveFrame,text = "Quit",command = QuitButton)               # Initialization of Quit Button
    root.title("Open")
    f = filedialog.askopenfilename(filetypes = data, defaultextension = data)       # This line opens filedialog and asks the user to open file
    openFileName = f                                                                # openFileName contains the name of current file
    OpenFile = open(str(f),'r+')                                                    # Opens file for reading and writing
    markdownViewer(str(f))                                                          
    text = OpenFile.read()
    TextBox.delete('1.0', END)                                                      # Previous text in TextBox is deleted 
    TextBox.insert('1.0',text)                                                      # Text from our file is added into TextBox
    NewWindow.title(str(f))
    SaveFrame.grid(row = 0,column = 0,sticky = "NS")
    openSave_button.pack()
    saveAs_button.pack()
    quitButton.pack()
    TextBox.grid(row = 0,column = 1,rowspan = 2)

def save():                                                                             # This function is called whenever Save button from New Tab is clicked
    global SaveFrame,TextBox,data,UntitledCounter,cwd       
    textInFile = TextBox.get("1.0",END)                                                 # Text from our text box is added into a variable called textInFile
    if platform == "win64" or platform == "win32":                                      # This line checks if the operating system is windows and adds the pathname for saving the file
        nameofFile = str(cwd) + "\\Untitled " + str(UntitledCounter) + ".txt"  # Untitled Counter is used to save the text
    else:
        nameofFile = str(cwd) + "/Untitled " + str(UntitledCounter) + ".txt"    # Pathname for saving the file 
    currentFile = open(nameofFile,'w')
    if textInFile == "\n":                                                              # If user wants to save an empty file 
        currentFile.write(" ")                                                          # Empty file is saved
    else:
        currentFile.write(textInFile) #This 1.0 denotes read from line 1 first character
    currentFile.close()
    markdownViewer(str(currentFile.name))
    NewWindow.title(str(currentFile.name))
    UntitledCounter += 1                                                                # Increments UntitledCounter

def saveAs():                                                           # This function is called whenever Save As button from Open Tab is clicked
    global SaveFrame,TextBox,data
    f = filedialog.asksaveasfile(filetypes = data, defaultextension = data)
    textInFile = TextBox.get("1.0",END)
    fileboi = open(str(f.name),'w')
    fileboi.write(textInFile) #This 1.0 denotes read from line 1 first character
    fileboi.close()
    markdownViewer(str(f.name))

def openSave():                                                         # This function is called whenever Save button from Open Tab is clicked
    global SaveFrame,TextBox,openFileName                                                                               
    textInFile = TextBox.get("1.0",END)
    currentFile = open(str(openFileName),'w')                           # opening of file with write mode
    currentFile.write(textInFile) #This 1.0 denotes read from line 1 first character
    currentFile.close()
    markdownViewer(str(openFileName))

def QuitButton():                           #This function is called whenever Quit Button is called
    global SaveFrame,TextBox,NewWindow
    NewWindow.destroy()                     # All the previous frames are destroyed
    SaveFrame.destroy()
    TextBox.destroy()
    mainDisplay()                           # MainFrame is created with New and Open Button

cwd = os.getcwd()                           # Gets the current working directory, useful in storing file and calling file
root = Tk()                                 # Main window on which our program runs
root.title("Editor")                        # Our program header is called "Editor"
UntitledCounter = 1                         # Keeps track of number of untitled files
openFileName = ""                           # Global variable called to know the currently open file name
data = [('Text(*.txt)', '*.txt'),('Markdown(*.md)', '*.md')]    # Supported datatypes in program stored in global variable
SaveFrame = Frame(root)                     # Frame for hosting Save,Save As,Quit button
TextBox = Text(root, height=40, width=40)   # Main TextBox 
MainFrame = Frame(root)                     
MainFrame.grid()
mainDisplay()


root.mainloop()
# Every GUI is a loop. It loops so it knows what is happening in the program.
