from tkinter import *
import math
import time
import threading

#region Main Section
app = Tk()
app.title('Rust Furnace Calculator')
app.iconbitmap('resources/Rust.ico')
app.configure(background='#33393B')
app.resizable(False, False)
#endregion

#region Variables
metalOreBoxContent = ''
metalOre = 0
sulfurOre = 0
hqOre = 0
charcoalTotal = 0
woodNeeded = 0
woodHqCalc = 10 / 12
woodMetalCalc = 5 / 12
woodSulfurCalc = 2.5 / 12
extra = 0
extraCheck = 0
choice = ""
seconds = 0
minutes = 0
restart = ""
stackSize = 0
stackSizeApprox = ""
stackSizeApproxHigh = 0
split = ""
splitSize = 0
totalSeconds = 0
secondsTimer = 0
minutesTimer = 0
timer = ""
woodTotalNeeded = 0
pausing = "False"
#endregion

#region Commands

def resetCommand():
    global pausing
    global resetting
    global totalSeconds
    global secondsTimer
    global minutesTimer
    resetting = 'y'
    pausing = "False"
    errorLabel.grid_forget()
    furnacesBox.delete(0, END)
    furnacesBox.insert(END, "1")
    metalOreBox.delete(0, END)
    sulfurOreBox.delete(0, END)
    hqOreBox.delete(0, END)
    stackSizeBox.config(state=NORMAL)
    stackSizeBox.delete(0, END)
    stackSizeBox.config(state=DISABLED)
    woodRequiredPFBox.config(state=NORMAL)
    woodRequiredPFBox.delete(0, END)
    woodRequiredPFBox.config(state=DISABLED)
    woodRequiredBox.config(state=NORMAL)
    woodRequiredBox.delete(0, END)
    woodRequiredBox.config(state=DISABLED)
    charcoalBox.config(state=NORMAL)
    charcoalBox.delete(0, END)
    charcoalBox.config(state=DISABLED)
    timeBox.config(state=NORMAL)
    timeBox.delete(0, END)
    timeBox.config(state=DISABLED)
    startTimer.config(state=NORMAL)
    pauseTimer.grid_forget()
    startTimer.config(state=NORMAL)
    startTimer.grid(row=4, column=1, sticky=S, pady=(10,0), padx=5)
    totalSeconds = 0
    secondsTimer = 0
    minutesTimer = 0

def resetOutput():
    global totalSeconds
    global secondsTimer
    global minutesTimer
    stackSizeBox.config(state=NORMAL)
    stackSizeBox.delete(0, END)
    stackSizeBox.config(state=DISABLED)
    woodRequiredPFBox.config(state=NORMAL)
    woodRequiredPFBox.delete(0, END)
    woodRequiredPFBox.config(state=DISABLED)
    woodRequiredBox.config(state=NORMAL)
    woodRequiredBox.delete(0, END)
    woodRequiredBox.config(state=DISABLED)
    charcoalBox.config(state=NORMAL)
    charcoalBox.delete(0, END)
    charcoalBox.config(state=DISABLED)
    timeBox.config(state=NORMAL)
    timeBox.delete(0, END)
    timeBox.config(state=DISABLED)
    totalSeconds = 0
    secondsTimer = 0
    minutesTimer = 0

def calculateCommand():
    global resetting
    resetting = 'y'
    resetOutput()
    errorLabel.grid_forget()
    startTimer.config(state=NORMAL)
    if metalOreBox.get() != '' and sulfurOreBox.get() != '':
        errorLabel.config(text="There was an error. Check your inputs.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    elif metalOreBox.get() != '' and hqOreBox.get() != '':
        errorLabel.config(text="There was an error. Check your inputs.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    elif sulfurOreBox.get() != '' and hqOreBox.get() != '':
        errorLabel.config(text="There was an error. Check your inputs.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    elif metalOreBox.get() != '' and sulfurOreBox.get() == '' and hqOreBox.get() == '':
        metalCommand()
    elif metalOreBox.get() == '' and sulfurOreBox.get() != '' and hqOreBox.get() == '':
        sulfurCommand()
    elif metalOreBox.get() == '' and sulfurOreBox.get() == '' and hqOreBox.get() != '':
        hqCommand()

def timerCommand():
    global secondsTimer
    global totalSeconds
    global minutesTimer
    global resetting
    global pausing
    resetting = 'n'
    timeBoxInsert = ""
    startTimer.config(state=DISABLED)
    for i in range(totalSeconds, -1, -1):
        while pausing == "True":
            time.sleep(0.1)
        while secondsTimer > 60:
            minutesTimer += 1
            secondsTimer -= 60
        if secondsTimer >0 and stackSizeBox.get() != '' and resetting != 'y':
            if (secondsTimer == 60):
                tempMin = minutesTimer + 1
                tempSec = 0
                timeBoxInsert = "%02dm %02ds" % (tempMin, tempSec)
                timeBox.config(state=NORMAL)
                timeBox.delete(0, END)
                timeBox.insert(END, timeBoxInsert)
                timeBox.config(state=DISABLED)
            else:
                timeBoxInsert = "%02dm %02ds" % (minutesTimer, secondsTimer)
                timeBox.config(state=NORMAL)
                timeBox.delete(0, END)
                timeBox.insert(END, timeBoxInsert)
                timeBox.config(state=DISABLED)
            secondsTimer -= 1
            if (minutesTimer > 0 and secondsTimer == 0):
                minutesTimer -= 1
                secondsTimer += 60
            app.update()
            time.sleep(1)
        elif stackSizeBox.get() == '':
            timeBox.config(state=NORMAL)
            timeBox.delete(0, END)
            timeBox.config(state=DISABLED)
            secondsTimer = 0
            totalSeconds = 0
            minutesTimer = 0
            app.update_idletasks()
            startTimer.config(state=NORMAL)
        elif resetting == 'y':
            app.update_idletasks()
            x.join()
            startTimer.config(state=NORMAL)
        else:
            timeBox.config(state=NORMAL)
            timeBox.delete(0, END)
            timeBox.insert(END, "Smelting Complete!")
            timeBox.config(state=DISABLED)
            app.update_idletasks()
            startTimer.config(state=NORMAL)

def metalCommand():
    global secondsTimer
    global totalSeconds
    global charcoalTotal
    seconds = 0
    minutes = 0
    metalOreCheck = int(metalOreBox.get()) / int(furnacesBox.get())

    extra = metalOreCheck / 12
    extraCheck = int(extra)
    woodNeeded = metalOreCheck * woodMetalCalc
    woodNeeded = math.ceil(woodNeeded)
    if extra == extraCheck and extra >= 1.0:
        woodNeeded = woodNeeded
        stackSize = math.floor(metalOreCheck / 12)
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSize)
        stackSizeBox.config(state=DISABLED)
    elif extra < 1.0:
        woodNeeded = 5
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, "<1")
        stackSizeBox.config(state=DISABLED)
    else:
        woodNeeded += 5
        stackSize = metalOreCheck / 12
        stackSizeApprox = math.floor(stackSize)
        stackSizeApproxHigh = stackSizeApprox + 1
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSizeApprox)
        stackSizeBox.insert(END, " - ")
        stackSizeBox.insert(END, stackSizeApproxHigh)
        stackSizeBox.config(state=DISABLED)
    charcoalTotal = math.ceil(woodNeeded * 0.75 * int(furnacesBox.get()))
    charcoalBox.config(state=NORMAL)
    charcoalBox.insert(END, charcoalTotal)
    charcoalBox.config(state=DISABLED)
    seconds = woodNeeded * 2
    secondsTimer = seconds
    totalSeconds = int(seconds)
    while seconds >= 60:
        minutes += 1
        seconds -= 60
    if metalOreCheck > 3000:
        errorLabel.config(text="You are smelting too much. This will cause overflow.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    woodTotalNeeded = woodNeeded * int(furnacesBox.get())
    woodRequiredPFBox.config(state=NORMAL)
    woodRequiredPFBox.insert(END, woodNeeded)
    woodRequiredPFBox.config(state=DISABLED)
    woodRequiredBox.config(state=NORMAL)
    woodRequiredBox.insert(END, woodTotalNeeded)
    woodRequiredBox.config(state=DISABLED)
    timeBox.config(state=NORMAL)
    timeBox.insert(END, format(minutes, '02d'))
    timeBox.insert(END, "m ")
    timeBox.insert(END, format(seconds, '02d'))
    timeBox.insert(END, "s")
    timeBox.config(state=DISABLED)
    return secondsTimer, totalSeconds

def sulfurCommand():
    global secondsTimer
    global totalSeconds
    global charcoalTotal
    seconds = 0
    minutes = 0
    sulfurOreCheck = int(sulfurOreBox.get()) / int(furnacesBox.get())

    extra = sulfurOreCheck / 12
    extraCheck = int(extra)
    woodNeeded = sulfurOreCheck * woodSulfurCalc
    woodNeeded = math.ceil(woodNeeded)
    if extra == extraCheck and extra >= 1.0:
        woodNeeded = woodNeeded
        stackSize = math.floor(sulfurOreCheck / 12)
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSize)
        stackSizeBox.config(state=DISABLED)
    elif extra < 1.0:
        woodNeeded = 5
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, "<1")
        stackSizeBox.config(state=DISABLED)
    else:
        woodNeeded += 5
        stackSize = sulfurOreCheck / 12
        stackSizeApprox = math.floor(stackSize)
        stackSizeApproxHigh = stackSizeApprox + 1
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSizeApprox)
        stackSizeBox.insert(END, " - ")
        stackSizeBox.insert(END, stackSizeApproxHigh)
        stackSizeBox.config(state=DISABLED)
    charcoalTotal = math.ceil(woodNeeded * 0.75 * int(furnacesBox.get()))
    charcoalBox.config(state=NORMAL)
    charcoalBox.insert(END, charcoalTotal)
    charcoalBox.config(state=DISABLED)
    seconds = woodNeeded * 2
    secondsTimer = seconds
    totalSeconds = int(seconds)
    while seconds >= 60:
        minutes += 1
        seconds -= 60
    if sulfurOreCheck > 3960:
        errorLabel.config(text="You are smelting too much. This will cause overflow.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    woodTotalNeeded = woodNeeded * int(furnacesBox.get())
    woodRequiredPFBox.config(state=NORMAL)
    woodRequiredPFBox.insert(END, woodNeeded)
    woodRequiredPFBox.config(state=DISABLED)
    woodRequiredBox.config(state=NORMAL)
    woodRequiredBox.insert(END, woodTotalNeeded)
    woodRequiredBox.config(state=DISABLED)
    timeBox.config(state=NORMAL)
    timeBox.insert(END, format(minutes, '02d'))
    timeBox.insert(END, "m ")
    timeBox.insert(END, format(seconds, '02d'))
    timeBox.insert(END, "s")
    timeBox.config(state=DISABLED)

def hqCommand():
    global secondsTimer
    global totalSeconds
    global charcoalTotal
    seconds = 0
    minutes = 0
    hqOreCheck = int(hqOreBox.get()) / int(furnacesBox.get())

    extra = hqOreCheck / 12
    extraCheck = int(extra)
    woodNeeded = hqOreCheck * woodHqCalc
    woodNeeded = math.ceil(woodNeeded)
    if extra == extraCheck and extra >= 1.0:
        woodNeeded = woodNeeded
        stackSize = math.floor(hqOreCheck / 12)
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSize)
        stackSizeBox.config(state=DISABLED)
    elif extra < 1.0:
        woodNeeded = 5
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, "<1")
        stackSizeBox.config(state=DISABLED)
    else:
        woodNeeded += 5
        stackSize = hqOreCheck / 12
        stackSizeApprox = math.floor(stackSize)
        stackSizeApproxHigh = stackSizeApprox + 1
        stackSizeBox.config(state=NORMAL)
        stackSizeBox.insert(END, stackSizeApprox)
        stackSizeBox.insert(END, " - ")
        stackSizeBox.insert(END, stackSizeApproxHigh)
        stackSizeBox.config(state=DISABLED)
    charcoalTotal = math.ceil(woodNeeded * 0.75 * int(furnacesBox.get()))
    charcoalBox.config(state=NORMAL)
    charcoalBox.insert(END, charcoalTotal)
    charcoalBox.config(state=DISABLED)
    seconds = woodNeeded * 2
    secondsTimer = seconds
    totalSeconds = int(seconds)
    while seconds >= 60:
        minutes += 1
        seconds -= 60
    if hqOreCheck > 1800:
        errorLabel.config(text="You are smelting too much. This will cause overflow.")
        errorLabel.grid(row = 9, column = 0, columnspan = 3 , sticky = S, pady = (0, 3))
    woodTotalNeeded = woodNeeded * int(furnacesBox.get())
    woodRequiredPFBox.config(state=NORMAL)
    woodRequiredPFBox.insert(END, woodNeeded)
    woodRequiredPFBox.config(state=DISABLED)
    woodRequiredBox.config(state=NORMAL)
    woodRequiredBox.insert(END, woodTotalNeeded)
    woodRequiredBox.config(state=DISABLED)
    timeBox.config(state=NORMAL)
    timeBox.insert(END, format(minutes, '02d'))
    timeBox.insert(END, "m ")
    timeBox.insert(END, format(seconds, '02d'))
    timeBox.insert(END, "s")
    timeBox.config(state=DISABLED)

def maxMetalCommand():
    tempFurnace = int(furnacesBox.get())
    resetCommand()
    furnacesBox.delete(0, END)
    furnacesBox.insert(END, tempFurnace)
    maxMetalCalc = 3000 * tempFurnace
    metalOreBox.insert(END, maxMetalCalc)
    metalCommand()

def maxSulfurCommand():
    tempFurnace = int(furnacesBox.get())
    resetCommand()
    furnacesBox.delete(0, END)
    furnacesBox.insert(END, tempFurnace)
    maxSulfurCalc = 3960 * tempFurnace
    sulfurOreBox.insert(END, maxSulfurCalc)
    sulfurCommand()

def maxHQMCommand():
    tempFurnace = int(furnacesBox.get())
    resetCommand()
    furnacesBox.delete(0, END)
    furnacesBox.insert(END, tempFurnace)
    maxHQMCalc = 1800 * tempFurnace
    hqOreBox.insert(END, maxHQMCalc)
    hqCommand()

def threadingTimer():
    global pausing
    if pausing == "True":
        pausing = "False"
        startTimer.grid_forget()
        pauseTimer.grid(row=4, column=1, sticky=S, pady=(10,0), padx=5)
    else:
        startTimer.grid_forget()
        pauseTimer.grid(row=4, column=1, sticky=S, pady=(10,0), padx=5)
        x = threading.Thread(target=timerCommand)
        x.start()

def pauseTimerCommand():
    global pausing
    pausing = "True"
    pauseTimer.grid_forget()
    startTimer.config(state=NORMAL)
    startTimer.grid(row=4, column=1, sticky=S, pady=(10,0), padx=5)


#endregion

#region Labels
#Inputs
furnacesLabel = Label(app, bg='#33393B', fg='white', text="Furnaces", justify=CENTER)
metalOreLabel = Label(app, bg='#33393B', fg='white', text="Total Metal", justify=CENTER)
sulfurOreLabel = Label(app, bg='#33393B', fg='white', text="Total Sulfur", justify=CENTER)
hqOreLabel = Label(app, bg='#33393B', fg='white', text="Total HQM", justify=CENTER)

#Outputs
stackSizeLabel = Label(app, bg='#33393B', fg='white', text="Stack Size", justify=CENTER)
woodRequiredPFLabel = Label(app, bg='#33393B', fg='white', text="Wood Per Furnace", justify=CENTER)
woodRequiredLabel = Label(app, bg='#33393B', fg='white', text="Wood Total", justify=CENTER)
charcoalLabel = Label(app, bg='#33393B', fg='white', text="Charcoal", justify=CENTER)
timeLabel = Label(app, bg='#33393B', fg='white', text="Time to Complete", justify=CENTER)


#Info
errorLabel = Label(app, bg='#33393B', fg='white', text='', justify=CENTER)

#Bind Labels
metalOreLabel.bind("<Button-1>", lambda event: maxMetalCommand())
sulfurOreLabel.bind("<Button-1>", lambda event: maxSulfurCommand())
hqOreLabel.bind("<Button-1>", lambda event: maxHQMCommand())

#endregion

#region Place Labels
#Inputs
furnacesLabel.grid(row = 0, column = 0, sticky = S, pady = (10, 3))
metalOreLabel.grid(row = 2, column = 0, sticky = S, pady = (10, 3))
sulfurOreLabel.grid(row = 4, column = 0, sticky = S, pady = (10, 3))
hqOreLabel.grid(row = 6, column = 0, sticky = S, pady = (10, 3))

#Outputs
stackSizeLabel.grid(row = 0, column = 2, sticky = S, pady = (10, 3))
woodRequiredPFLabel.grid(row = 2, column = 2, sticky = S, pady = (10, 3))
woodRequiredLabel.grid(row = 4, column = 2, sticky = S, pady = (10, 3))
charcoalLabel.grid(row = 6, column = 2, sticky = S, pady = (10, 3))
timeLabel.grid(row = 6, column = 1, sticky = S, pady = (10, 3))

#endregion

#region Text Boxes
#Inputs
furnacesBox = Entry(app, bg='#1B1F20', highlightbackground="#525C5F", fg='white', justify=CENTER)
metalOreBox = Entry(app, bg='#1B1F20', highlightbackground="#525C5F", fg='white', justify=CENTER)
sulfurOreBox = Entry(app, bg='#1B1F20', highlightbackground="#525C5F", fg='white', justify=CENTER)
hqOreBox = Entry(app, bg='#1B1F20', highlightbackground="#525C5F", fg='white', justify=CENTER)

#Outputs
stackSizeBox = Entry(app, highlightbackground="#525C5F", justify=CENTER, disabledforeground="white", disabledbackground="#1B1F20", state=DISABLED)
woodRequiredPFBox = Entry(app, highlightbackground="#525C5F", justify=CENTER, disabledforeground="white", disabledbackground="#1B1F20", state=DISABLED)
woodRequiredBox = Entry(app, highlightbackground="#525C5F", justify=CENTER, disabledforeground="white", disabledbackground="#1B1F20", state=DISABLED)
charcoalBox = Entry(app, highlightbackground="#525C5F", justify=CENTER, disabledforeground="white", disabledbackground="#1B1F20", state=DISABLED)
timeBox = Entry(app, highlightbackground="#525C5F", justify=CENTER, disabledforeground="white", disabledbackground="#1B1F20", state=DISABLED)

#Prefill Text Boxes
furnacesBox.insert(END, "1")

#Bind Text Boxes
furnacesBox.bind("<Return>", lambda event: calculateCommand())
metalOreBox.bind("<Return>", lambda event: calculateCommand())
sulfurOreBox.bind("<Return>", lambda event: calculateCommand())
hqOreBox.bind("<Return>", lambda event: calculateCommand())

#endregion

#region Place Text Boxes
#Inputs
furnacesBox.grid(row = 1, column = 0, sticky = N, padx = 10)
metalOreBox.grid(row = 3, column = 0, sticky = N, padx = 10)
sulfurOreBox.grid(row = 5, column = 0, sticky = N, padx = 10)
hqOreBox.grid(row = 7, column = 0, sticky = N, padx = 10)

#Outputs
stackSizeBox.grid(row = 1, column = 2, sticky = N, padx = 10)
woodRequiredPFBox.grid(row = 3, column = 2, sticky = N, padx = 10)
woodRequiredBox.grid(row = 5, column = 2, sticky = N, padx = 10)
charcoalBox.grid(row = 7, column = 2, sticky = N, padx = 10)
timeBox.grid(row = 7, column = 1, sticky = N, padx = 10)

#endregion

#region Buttons
calculate = Button(app, bg='#33393B', activebackground='#1B1F20', relief=RIDGE, highlightbackground="#525C5F", fg='white', text="Calculate", command=calculateCommand)
startTimer = Button(app, bg='#33393B', activebackground='#1B1F20', relief=RIDGE, highlightbackground="#525C5F", fg='white', text="Start Timer", command=threadingTimer)
pauseTimer = Button(app, bg='#33393B', activebackground='#1B1F20', relief=RIDGE, highlightbackground="#525C5F", fg='white', text="Pause Timer", command=pauseTimerCommand)
reset = Button(app, bg='#33393B', activebackground='#1B1F20', relief=RIDGE, highlightbackground="#525C5F", fg='white', text="Reset", command=resetCommand)
#endregion

#region Placing Buttons
calculate.grid(row=2, column=1, sticky=N, pady=(10,0), padx=5)
startTimer.grid(row=4, column=1, sticky=S, pady=(10,0), padx=5)
reset.grid(row=8, column=1, sticky=S, padx=5, pady=(10,10))
#endregion

#Program Loop
app.mainloop()