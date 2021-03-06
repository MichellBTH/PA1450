import csv
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

storage = list()
temperature = list()
time = list()
rainfall = list()
sunshine = list()


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

def displayDay(fig,date,data):
    
    correctFormat(date)

    for i in range(len(data)):
        if(data[i][0] == date):
            temperature.append(data[i][2])

    for i in range(len(data)):
        if(data[i][0] == date):
            time.append(data[i][1][0:2])

    fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=date ))

def menu():

    date = ""
    date2 = ""
    fig = go.Figure()
    fig.update_layout(title ="Temperature", xaxis_title="Time(h)", yaxis_title="Temperature") 
    answear = -1
    readCSVFile("smhi-opendata_1_65090_20200507_045303.csv",storage)
    readCSVFile("sol.csv",sunshine)
    readCSVFile("nederbörd.csv",rainfall)
    valid = False
    target = 0

    print("\nWelcome\nPress 0 to put in a date for a specific day for a specific year")
    print("Press 1 for chosing a specific interval")
    print("Press 2 for chosing a specific month")
    print("Press 3 to choose a specific day in a week of a month")
    print("Press 4 to generate sunshine report for a certain day")
    print("Press 5 to generate rainfall report for a certain day ")
    print("Press 6 to exit")

    while (answear != -2):

        try:
            answear = int(input("\nEnter choice:"))
        except:
            print("Invalid input")

        try:
            
            valid = True

            if answear == 0:
                data =""
                print("What type of data?")
                print("Avalable data types: temprature, sunshine, rainfall")
                data = input("Type in type:")

                while(data != "temprature" and data != "sunshine" and data != "rainfall"):
                    print("Invalid type")
                    data = input("Type in type:")


                if data == "temprature":
                    print("\nInput a date in format xxxx-xx-xx")
                    print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                    date = input("Type in a date:")
                    fig.update_layout(title ="Temperature", xaxis_title="Time(h)", yaxis_title="Temperature") 
                    displayDay(fig,date,storage)
                 
                elif data == "sunshine":
                    print("\nInput a date in format xxxx-xx-xx")
                    print("Available date in range",sunshine[0][0],"to",sunshine[len(sunshine)-1][0])
                    date = input("Type in a date:")
                    fig.update_layout(title ="sunshine", xaxis_title="Time(h)", yaxis_title="Sunshine amount of hour in seconds") 
                    displayDay(fig,date,sunshine)
                     
                elif data == "rainfall":
                    print("\nInput a date in format xxxx-xx-xx")
                    print("Available date in range",rainfall[0][0],"to",rainfall[len(rainfall)-1][0])
                    date = input("Type in a date:") 
                    fig.update_layout(title ="rainfall", xaxis_title="Time(h)", yaxis_title="Amount of rainfall") 
                    displayDay(fig,date,rainfall)

                
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

            elif answear == 6:
                answear = -2
                valid = False

            elif answear == 3:
                print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
                print("\nInput a date in format xxxx-xx")
                date = input("Type in a date:")
                target = int(input("Type in a day where 0 is monday and 6 is sunday:"))
                displayWeek(fig,date,date2,target)

            elif answear == 4:

               
                print("Available date in range",sunshine[0][0],"to",sunshine[len(sunshine)-1][0])
                print("\nInput a date in format xxxx-xx-xx")
                date = input("Type in a date:")
                createSunshineReport(date,sunshine)
                print("Done!")
                valid = False

            elif answear == 5:
                
                print("Available date in range",rainfall[0][0],"to",rainfall[len(rainfall)-1][0])
                print("\nInput a date in format xxxx-xx-xx")
                date = input("Type in a date:")
                createRainfallReport(date,rainfall)
                print("Done!")
                valid = False


            else:
                print("\nInvalid input")
                valid = False
                answear = -1
           

        except ValueError("Wrong format"):
            print("Invalid date try again")
            valid = False
            answear = -1
        
        if valid:
            makeGraph(fig)
            fig = go.Figure()
            fig.update_layout(title ="Temperature", xaxis_title="Time(h)", yaxis_title="Temperature") 
              
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
    
    sun = sun/24.0
    sun = sun*100

    with open("SunshineReport","w") as f:
        print("Repport of how much sun there was during the whole day in karlskrona",file=f)
        for i in sunshine:
            if(i[0] == date):
                print(", ".join(i),file=f)
        print("It was sunny "+str(sun)+"%"+" of the day",file = f)

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

def createRainfallReport(date,rainData):
    rain = 0.0

    for i in rainData:
        if(i[0] == date and float(i[2]) > 0):
            rain += 1
   
    rain /= 24
    rain *= 100

    with open("RainfallRepport","w") as f:
        print("Report of how much rain there was during the whole day in karlskrona",file=f)
        for i in rainData:
            if(i[0] == date):
                print(", ".join(i),file=f)
  
        print("It rained "+str(rain)+"%"+" of the day",file=f)
            

menu()