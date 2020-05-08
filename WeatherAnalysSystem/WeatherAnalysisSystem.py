import csv
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

storage = list()
temperature = list()
time = list()

def readCSVFile(file,data):
    with open(file, newline="") as cfile:
        temp = csv.reader(cfile, delimiter = ";")
        for row in temp:
            data.append(row)
    data[0][0] = data[0][0].replace("ï»¿","")

def makeGraph(fig):
    fig.write_html('first_figure.html', auto_open=True) 

def displayInterval(fig,date,date2):
    
    correctFormat(date)
    correctFormat(date2)
    
    d1 = datetime(int(date[0:4]),int(date[5:7]),int(date[8:]))
    d2 = datetime(int(date2[0:4]),int(date2[5:7]),int(date2[8:]))
    tempDate = ""
    lastDate = date
    temp = 0

    if(d1 > d2):
        temp = date
        date = date2
        date2 = temp
        temp = d1
        d1 = d2
        d2 = temp


    for i in range(len(storage)):

        tempDate = datetime(int(storage[i][0][0:4]),int(storage[i][0][5:7]),int(storage[i][0][8:]))
            
        if(tempDate >= d1 and tempDate <= d2):
            time.append(storage[i][1][0:2])
            

        
    for i in range(len(storage)):

        tempDate = datetime(int(storage[i][0][0:4]),int(storage[i][0][5:7]),int(storage[i][0][8:]))
        
        if(tempDate >= d1 and tempDate <= d2):
            date = storage[i][0]

            if(date != lastDate):
                fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=lastDate ))
                lastDate = date
                temperature.clear()

            if(date == lastDate):
                temperature.append(storage[i][2])

    fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=lastDate))

def displayDay(fig,date):
    
    correctFormat(date)

    for i in range(len(storage)):
        if(storage[i][0] == date):
            temperature.append(storage[i][2])

    for i in range(len(storage)):
        if(storage[i][0] == date):
            time.append(storage[i][1][0:2])

    fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=date ))

def menu():

    date = ""
    date2 = ""
    fig = go.Figure()
    answear = -1
    readCSVFile("smhi-opendata_1_65090_20200507_045303.csv",storage)
    valid = False
    target = 0

    print("\nWelcome\nPress 0 to put in a date for a specific day for a specific year")
    print("Press 1 for chosing a specific interval")
    print("Press 2 for chosing a specific month")
    print("Press 3 to exit")
    print("Press 4 to choose a specific day in a week of a month")
    print("Press 5 to generate sunshine report for a certain day")

    while (answear != -2):

        try:
            answear = int(input("\nEnter choice:"))
        except:
            print("Invalid input")

        try:
            
            valid = True

            if answear == 0:
                print("\nInput a date in format xxxx-xx-xx")
                print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                date = input("Type in a date:")
                displayDay(fig,date)
                
            elif answear == 1:
                print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                print("\nInput a date in format xxxx-xx-xx")
                date = input("Type in a date:")
                date2 = input("Type in a second date:")
                displayInterval(fig,date,date2)
            
            elif answear == 2:
                print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                print("\nInput a date in format xxxx-xx")
                date = input("Type in a date:")
                displayMonth(fig,date,date2)

            elif answear == 3:
                answear = -2
                valid = False

            elif answear == 4:
                print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                print("\nInput a date in format xxxx-xx")
                date = input("Type in a date:")
                target = int(input("Type in a day where 0 is monday and 6 is sunday:"))
                displayWeek(fig,date,date2,target)

            elif answear == 5:
                sunshine = list()
                readCSVFile("sol.csv",sunshine)
                print("Available date in range",sunshine[0][0],"to",sunshine[len(sunshine)-1][0])
                print("\nInput a date in format xxxx-xx-xx")
                date = input("Type in a date:")
                createSunshineReport(date,sunshine)
                print("Done!")
                valid = False

            else:
                print("\nInvalid input")
                valid = False
                answear = -1
           

        except:
            print("Invalid date try again")
            valid = False
            answear = -1
        
        if valid:
            makeGraph(fig)
            fig = go.Figure()
              
def displayMonth(fig,date,date2):

    correctFormat(date)

    date2 = date
    date += "-01"
    biggest = ""
    

    for i in range(len(storage)):
        if(storage[i][0][0:7] == date[0:7]):
            biggest = storage[i][0][8:]

    date2 += "-"+biggest
    displayInterval(fig,date,date2)

def correctFormat(date):

    lines = 0
    numbers = 0

    for letters in date:

        if "-" == letters: 
            lines +=1
        
        try:
            int(letters)
            numbers+=1

        except:
            if letters != "-":
                raise ValueError("Wrong format")
    
    if  lines < 1 and numbers < 6:
        raise ValueError("Wrong format")

def createSunshineReport(date,sunshine):
    sun = 0.0

    for i in range(len(sunshine)):
       if(sunshine[i][0] == date):
           sun += float(sunshine[i][2])/(60**2)
    
    sun = sun/23.0

    with open("SunshineReport","w") as f:
        print(10,"SunshineReport",file = f)
  

def displayWeek(fig,date,date2,target):

    correctFormat(date)

    date2 = date
    date += "-01"
    biggest = ""

    for i in range(len(storage)):
        if(storage[i][0][0:7] == date[0:7]):
            biggest = storage[i][0][8:]

    date2 += "-"+biggest

    d1 = datetime(int(date[0:4]),int(date[5:7]),int(date[8:]))
    d2 = datetime(int(date2[0:4]),int(date2[5:7]),int(date2[8:]))
    tempDate = ""
    lastDate = date
    temp = 0

    if(d1 > d2):
        temp = date
        date = date2
        date2 = temp
        temp = d1
        d1 = d2
        d2 = temp


    for i in range(len(storage)):
        
        tempDate = datetime(int(storage[i][0][0:4]),int(storage[i][0][5:7]),int(storage[i][0][8:]))
            
        if(tempDate >= d1 and tempDate <= d2 and tempDate.weekday() == target):
            time.append(storage[i][1][0:2])
            

        
    for i in range(len(storage)):

        tempDate = datetime(int(storage[i][0][0:4]),int(storage[i][0][5:7]),int(storage[i][0][8:]))
        
        if(tempDate >= d1 and tempDate <= d2 and tempDate.weekday() == target):
            date = storage[i][0]

            if(date != lastDate):
                fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=lastDate ))
                lastDate = date
                temperature.clear()

            if(date == lastDate):
                temperature.append(storage[i][2])

    fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=lastDate))




menu()