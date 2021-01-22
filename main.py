#imports
import csv
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from unidecode import unidecode
from pprint import pprint

#creation of global variables

#hold data from a csv and turn into a dictionary
statsdict = {}
teamDict = {}

#a list of user inputted players
inputPlayers = []

#linear regression objects to be changed later
ppg = LinearRegression()
wins = LinearRegression()

#function that gets data from csv files and filters them
def playerDict():

    #import file and create dictionary - used for player names
    stats = "data2.csv"

    #open up the data2 file
    with open(stats,'r') as csvfile:
        statsreader = csv.reader(csvfile)
        for row in statsreader:

        #put each name into the dictionary
            namedata = row[1]
            name = unidecode(namedata)

            #create a variable for each value
            fg = float(row[5])
            fga = float(row[6])
            ft = float(row[11])
            fta = float(row[12])
            orb = float(row[16])
            drb = float(row[17])
            ast = float(row[19])
            stl = float(row[20])
            blk = float(row[21])
            tov = float(row[14])
            pf = float(row[15])
            pts = float(row[22])
        
            #calculate game score
            gmsc = (pts * 1.0) + (fg * 0.4) + (fga * (-0.7)) + ((fta - ft) * (-0.4)) + (orb * 0.7) + (drb * 0.3) + (stl * 1.0) + (ast * 0.7) + (blk * 0.7) + (pf * (-0.4)) + (tov * (-1.0))

            #round game score and then put into dictionary
            gmsc = round(gmsc, 2)
            statsdict[name] = [gmsc]

    #open up the salary file
    salaries = "salary.csv"
    with open(salaries,'r') as csvfile:
        salaryreader = csv.reader(csvfile)
        for row in salaryreader:
            #put players' salries into dictionary
            #ensures players are already in the dictionary
            if(row[1][0 : -1] in statsdict):
                salary = row[2]
                #turn salary from a formatted string into an int
                salary = salary[1 : -1]
                salary = salary.replace(",", "")
                salary = int(salary)
                statsdict[row[1][0 : -1]].append(salary)

    positions = "data.csv"
    #open the data file, which contains the players positions
    with open(positions, 'r') as csvfile:
        posreader = csv.reader(csvfile)
        #for each player, add their position
        for row in posreader:
            playername = row[1]
            playername = playername[ : playername.index('\\')]
            #some players had special characters in names
            #unidecode changes special characters into basic ones
            playername = unidecode(playername)
            statsdict[playername].append(row[2])

    #file with data about all teams in the 18-19 regular season
    team = "teamStats.csv"
    with open(team, 'r') as csvfile:
        teamreader = csv.reader(csvfile)
        for row in teamreader:
            #create a team dictionary and with lists as values
            teamDict[row[1]] = []
            
            #gets values from each team
            fg = float(row[4])
            fga = float(row[5])
            ft = float(row[13])
            fta = float(row[14])
            orb = float(row[16])
            drb = float(row[17])
            ast = float(row[19])
            stl = float(row[20])
            blk = float(row[21])
            tov = float(row[22])
            pf = float(row[23])
            pts = float(row[24])
            salary = int(row[25])
            wins = int(row[26])

            #gmsc = (pts * 1.0) + (fg * 0.4) + (fga * (-0.7)) + ((fta - ft) * (-0.4)) + (orb * 0.7) + (drb * 0.3) + (stl * 1.0) + (ast * 0.7) + (blk * 0.7) + (pf * (-0.4)) + (tov * (-1.0))
            #gmsc = round(gmsc, 2)

            teamDict[row[1]].append(pts) #averge points
            teamDict[row[1]].append(salary) #money spent on players
            teamDict[row[1]].append(wins)  #total wins in season
            
#Linear Regression for predicting points per game based on total cost.
def trainPPG():
    
    #calls function to ensure the csv files have been processed
    playerDict()

    #creates two lists of data
    ppgar = []
    salar = []

    #add data to lists from dictionary
    for key in teamDict:
        ppgar.append(teamDict[key][0])
        salar.append(teamDict[key][1])

    #creation of two variables used for linear regression
    x = np.array(salar).reshape((-1,1))
    y = np.array(ppgar)

    ppg.fit(x,y)
    slope = ppg.coef_
    yint = ppg.intercept_

    #print("y = " + str(slope[0]*1000000) + "x + " + str(yint))

#Linear regression model for predicting the number of wins based on total cost of a team.
def trainWins():
    
    #process csv files
    playerDict()

    #create two lists for data
    salar = []
    winar = []
    
    #add data to list from dictionary
    for key in teamDict:
        salar.append(teamDict[key][1])
        winar.append(teamDict[key][2])

    #linear regression variables
    x = np.array(salar).reshape((-1,1))
    y = np.array(winar)

    wins.fit(x,y)

    slope = wins.coef_
    yint = wins.intercept_

    #print("y = " + str(slope[0] * 1000000) + "x + " + str(yint))

#final "main" method
#used to get user input
def generate():

    #calls our helper methods to process our data
    playerDict()
    trainPPG()
    trainWins()

    print("Welcome to Building Your Own NBA Team!")

    #initialize our cost to 0.
    cost = 0
    
    #boolean for tracking if user inputted team size is valid
    sizeAllowed = False

    #structure to ensure a valid team size is entered by user.
    while(sizeAllowed == False):

        #asks for team size
        size = input("Please enter the size (10 - 15) of your NBA team: ")

        #try-except to see if user entered a number
        try:

            size = int(size) #turns string into int

        except:

            #if the team size is invalid, give error message and repeat
            print("Please type a valid team size: ")
            continue

        if  size < 16 and size > 9: #checks that size is in range
            sizeAllowed = True
        else: #if not, warn user and ask again
            print("A team must have between 10 and 15 players")

    #loop to ask for players until team size is reached
    while(len(inputPlayers) < int(size)):

        #prompt for name
        name = input("Please enter the name of an NBA Player: ")
        #if the player is found in dictionary
        if name in statsdict:

            #if player is already in user inputted list
            if name in inputPlayers:

                #reject repeats and tell user
                print("You have already listed that player")

            else:

                #otherwise it is fine to add the player
                inputPlayers.append(name)
                #also add the players salary into the teams cost
                cost += int(statsdict[name][1])

        else:
            #if name is not in dictionary, tell user
            print("Invalid player name, try again")
            
    #Asks user for the name of their team
    team = input("Please enter your team name: ")
    print()

    #prints the team name and roster as entered
    print(team)
    for name in inputPlayers:
        print(name)
    print()

    costInt = cost
    #format the cost into a string with dollar signs and commas    
    cost = "$" + "{:,}".format(cost)
    print("The cost of this team is: ", cost)
    #format cost back into an int that can be used for multiplication
    cost = cost[1:].replace(",", "")

    #predicicting win total using regression model
    predictedWins = costInt * wins.coef_[0] + wins.intercept_
    predictedWins = math.floor(predictedWins)

    #cap of 82 wins
    if predictedWins > 82:
        predictedWins = 82

    #predicting ppg total using regression model
    predictedppg = costInt * ppg.coef_[0] + ppg.intercept_
    #predictedppg = predictedppg[0]
    #rounded to two decimal places
    predictedppg = round(predictedppg, 2)

    #Final print statement with all information about team.
    print("The " + team + " are predicted to score " + str(predictedppg) + " ppg and are predicted to win " + str(predictedWins) + " games in the regular season.")

#call on the function to ask for user input
generate()