import csv
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

storage = list()
temperature = list()
time = list()
date = "2010-03-01" #remove
date2 = "2010-03-20" #remove
answear = 1 #remove


def readCSVFile(file):
    with open(file, newline="") as cfile:
        temp = csv.reader(cfile, delimiter = ";")
        for row in temp:
            storage.append(row)
    storage[0][0] = storage[0][0].replace("ï»¿","")

def makeGraph(fig):
    fig.write_html('first_figure.html', auto_open=True) 

def parseAnswear(answear,date,date2):

    fig = go.Figure()

    if(answear == 1):

        d1 = datetime(int(date[0:4]),int(date[5:7]),int(date[8:]))
        d2 = datetime(int(date2[0:4]),int(date2[5:7]),int(date2[8:]))
        counter = 0

        if(d1 < d2):
            day_count = (d2 - d1).days + 1

        else:
            day_count = (d1 - d2).days + 1
            temp = date
            date = date2
            date2 = temp


        for i in range(len(storage)):
            
            if(storage[i][0] == date or 23*day_count >= counter):
                time.append(storage[i][1][0:2])
                counter +=1

        counter = 0

        for i in range(len(storage)):

            if(storage[i][0] == date or 23*day_count >= counter ):
                temperature.append(storage[i][2])
                counter +=1

            if(counter%24 == 0 and counter != 0):
                fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name=storage[0][0] + storage[0][1] ))
                temperature.clear()
        

        fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", name="time" ))

    if(answear == 0):
        
        for i in range(len(storage)):
            if(storage[i][0] == date):
                temperature.append(storage[i][2])

        for i in range(len(storage)):
            if(storage[i][0] == date):
                time.append(storage[i][1][0:2])

        fig.add_trace(go.Scatter(x=time, y=temperature,mode="markers", text="Temperature" ))
    
    makeGraph(fig)

def menu():

    date = ""
    date2 = ""

    print("\nWelcome\nPress 0 to put in a date for a specific day for a specific year")
    print("Press 1 for chosing specific interval")
    while (len(date) != 10):

        answear = int(input("\nEnter choice:"))

        if(answear == 0):
            print("\nInput a date in format xxxx-xx-xx")
            print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
            date = input("Type in a date:")
            
        elif(answear == 1):
            print("Available date in range",storage[0][0],"to",storage[len(storage)-1][0])
            date = input("Type in a date:")
            date2 = input("Type in a second date:")

        elif(len(date) != 10):
            print("\nInvalid input")

        else:
            print("\nInvalid input")
        
    parseAnswear(answear,date,date2)



readCSVFile("smhi-opendata_1_65090_20200507_045303.csv")

parseAnswear(answear,date,date2)

