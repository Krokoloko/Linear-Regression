import numpy as np
import csv
import sys
import math
import matplotlib.pyplot as plt
import savReaderWriter as sv

#Maak er een functie van. 'Check'
#Vertaal de wiskunde met het voorbeeld van code.
#Powerpoint presentatie


#De waardes van x
years = []
#De waardes van y
suicides = []

requested = False

list_request = input("Welcome to my linear regression application!\nDo you want to see the list of countries you can analyse from? (y/n)")

countries = []

#opening the csv file
csvFile = open("master.csv","r")

read = csv.reader(csvFile)

#Fetching the data of the country from the master.csv
if list_request.casefold().replace(" ","") == "y":
    header = True
    for row in read:
        if header:
            header = False
        else:
            if row[0] not in countries:
                countries.append(row[0])
                print(row[0])

country_request = input("What country do you want to analyse? \n")


if country_request.count(" ") is not 0:
    print("The requested country : \'" + country_request + "\' contains a whitespace.")
    print("If the name of the country contains whitespace, please replace it with a \'_\'.")
    print("Terminating program...")
    sys.exit(0)

#String formatting to identify the country.
country = country_request.replace("_"," ").casefold().title()

header = True
yearsIndex = 1
suicidesIndex = 4


#Fetching the data of the country from the master.csv
for row in read:
    if header:
        header = False
    else:
        if row[0] == country:
            if int(row[yearsIndex]) not in years:
                years.append(int(row[yearsIndex]))
                suicides.append(int(row[suicidesIndex]))
            else:
                suicides[years.index(int(row[yearsIndex]))] = int(suicides[years.index(int(row[yearsIndex]))]) + int(row[suicidesIndex])
#If there are no records of the requested country.
if len(years) is 0:
    print("We couldn\'t find anything of the country " + country)
    print("Terminating program...")
    sys.exit(0)
csvFile.close()


#Returns the y values of the linear regression
def linear_regression(targetX,targetY):
    n = len(targetX)
    sumX = sum(targetX)/n
    sumY = sum(targetY)/n
    numerator = denominator = 0

    #This is where the linear function is being calculated
    for i in range(n):
        numerator += (targetX[i] - sumX) * (targetY[i] - sumY)
        denominator += (targetX[i] - sumX) ** 2

    slope = numerator/denominator
    yIntercept = sumY-(sumX*slope)

    regression = np.zeros(n)
    for i in range(n):
        regression[i] = (slope*targetX[i]) + yIntercept

    return lambda x: (slope*x)+yIntercept



x = np.array(years)
y = np.array(suicides)

linearFuncion = linear_regression(x, y)

regression = linear_regression(x, y)(x)

def step(slope,y_int,points_x,points_y,learningRate):
    y_int_gradient = 0
    slope_gradient = 0
    n = float(len(points_x))
    for i in range(0,len(points_x)):
        x = points_x[i]
        y = points_y[i]
        y_int_gradient += -(2/n) * (y - ((slope * x) + y_int))
        slope_gradient += -(2/n) * x * (y - ((slope * x) + y_int))
    new_y_int = y_int - (learningRate * y_int_gradient)
    new_slope = slope - (learningRate * slope_gradient)
    return [new_slope,new_y_int]

def gradient_descent(learningRate,points_x, points_y,start_slope,start_y_int,num_iter):
    lr = learningRate
    slope = start_slope
    y_int = start_y_int
    for i in range(num_iter):
        slope, y_int = step(slope, y_int, np.array(points_x), np.array(points_y), lr)
    return [slope, y_int]

learned = gradient_descent(0.0001, x, y, 0, 0, 100)
# print(learned)

#Drawing visualisation of the correlation and the regression.
plt.scatter(x,y)
# # plt.plot(x,y,c="red")
plt.plot(x,regression,c="green")
plt.xlabel('year')
plt.ylabel('people')
plt.title('Suicide rate of ' + country)
plt.show()
