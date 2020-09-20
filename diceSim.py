
import random
from tkinter import *
import pandas as pd             #pip install matplotlib
import matplotlib.pyplot as plt #pip install pandas
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def makeCheck(skillLevel):
    total = 0
    for die in range(skillLevel):
        temp = random.randint(1,int(row1.myentry.get()))
        if temp>=int(row2.myentry.get()):
            total+=1
            if temp==int(row1.myentry.get()) and bool(row7.myentry.get()):
                total+=1
        if temp == 1 and bool(row8.myentry.get()):
            total-=1
    return max(0,total)

def calcResults():
    results = []
    for level in range(int(row3.myentry.get())):
        successes = []
        for index in range(int(row5.myentry.get())):
            successes.append(makeCheck(level))
        successes.sort()
        results.append(successes)
    return results

def percentPassed(results):
    percentByLevel = []
    for level in results:
        count = 0
        for check in level:
            if check>=int(row4.myentry.get()):
                count+=1
        percent = count/int(row5.myentry.get())
        percentByLevel.append(percent)
    return percentByLevel

def callback(sv):
    refreshData()
    refreshGraph1()
   
def refreshGraph1():
    global graph1,canvas,graph2
    graph1.clear()
    graph1.boxplot(df)
    graph2.clear()
    graph2.plot(data2,'bo')
    canvas.draw()

def refreshData():
    global data,df,data2
    data = calcResults()
    df = pd.DataFrame(data)
    df = df.transpose()
    data2 = percentPassed(data)
    df2 = pd.DataFrame(data2)

class varRow:
    def __init__(self,frame,label,default,func):
        self.myframe = Frame(frame)
        self.myframe.pack()
        self.mylabel = Label(self.myframe,text=label)
        self.mylabel.pack(side=LEFT)
        self.mysv = StringVar()
        self.mysv.trace("w", lambda name, index, mode, sv=self.mysv: callback(self.mysv))
        vcmd = (frame.register(func), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.myentry = Entry(self.myframe, textvariable=self.mysv, validate = 'key', validatecommand = vcmd)
        self.myentry.insert(0,default)
        self.myentry.pack(side=RIGHT)

def validInt(action, index, value_if_allowed,
                    prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False

def validBool(action, index, value_if_allowed,
                    prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
        try:
            bool(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False

window = Tk()
window.title("dice visualization")

leftcol = Frame(window)
leftcol.pack(side=LEFT)
row1 = varRow(leftcol,"sides on dice","10",validInt)
row2 = varRow(leftcol,"target number","7",validInt)
row3 = varRow(leftcol,"max skill level","15",validInt)
row4 = varRow(leftcol,"successes required","3",validInt)
row5 = varRow(leftcol,"sample sizes","100",validInt)
row7 = varRow(leftcol,"tens count twice","True",validBool)
row8 = varRow(leftcol,"ones subtract","True",validBool)

fig = Figure(figsize=(12,6),dpi=100)
graph1 = fig.add_subplot(121)
graph2 = fig.add_subplot(122)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

refreshData()
refreshGraph1()

toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

window.mainloop()


