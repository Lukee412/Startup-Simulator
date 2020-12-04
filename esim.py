import tkinter as tk
from tkinter import *
import tkinter.messagebox
from random import random
import time
import numpy as np
import pandas as pd
from PIL import ImageTk,Image
import matplotlib
matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import PyQt4
#from PyQt4 import QtGui    # or PySide

# Define useful parameters
DELAY = 2000
startingCash = 10000
#totalRevenue = 0
windowsize = 800
devStages = {"Ideation":30, "Validation":100, "MVP":600, "Beta":10000, "Full Release": 100000, "New Version":10000000} #Productivity Units
fundingStages = {"Friends&Family":100000,"Seed":1000000,"Series A":10000000,"Series B":30000000,"Series C":45000000} #Thousands of $
officeTypes = {"Garage":"images/garage.jpg","Clean Garage":"images/cleangarage.jpg","Small Office":"images/office1.jpg","Medium Office":"images/office2.jpg","Large Office":"images/office3.jpg", "Corporate Office":"images/office4.jpg"}
officeCosts = {"Garage":0,"Clean Garage":0,"Small Office":30,"Medium Office":500,"Large Office":5000, "Corporate Office":30000}
officeProductivity = {"Garage":0,"Clean Garage":1,"Small Office":3,"Medium Office":15,"Large Office":50, "Corporate Office":200}
employeeCaps = {"Garage":3,"Clean Garage":4,"Small Office":8,"Medium Office":30,"Large Office":150, "Corporate Office":2000}
possibleShocks = {0:"terrorist attack", 1:"natural disaster", 2:"political upheaval"}
initialRevenue = 0
initialCosts = 30
initialOutput = 4 #Productivity units per day
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"

BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'

class StartUpSim:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self): # Sets up key configurations
        self.window = Tk()
        self.window.title("StartUp Simulator")
        #self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
        #self.center(self.window)
        #self.window.eval('tk::PlaceWindow . center')
        self.scoreFrame = tk.Frame(self.window)
        self.scoreFrame.pack()
        self.graphicFrame = tk.Frame(self.window) # Turn into canvas?
        self.graphicFrame.pack(side="bottom")
        
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        #self.window.bind("<Button-1>", self.mouse_input)
        self.begin = False
        #Show start page
        self.startGame = False
        self.display_startPage()

    def play_again(self): # Runs all initialization functions
        #Reset all game parameters (days, cash)
        self.canvas.destroy()
        self.gameover = False
        self.databreachDate = int(120 + random() * 200)
        self.downturnDate = int(120 + random() * 200)
        self.lawsuitDate = int(self.databreachDate + 20 + random() * 50)
        self.viralDate = int(120 + random() * 100)
        self.currentDay = 0
        self.cash = startingCash
        self.stage = "Ideation"
        self.progress = 0
        self.dailyOutput = initialOutput
        self.totalRevenues = 0
        self.totalCosts = 0
        self.totalUsers = 0
        self.numCofounders = 0
        self.numEmployees = 0
        self.microflopRelease = 250
        self.dailyRevenue = [0]*730
        self.dailyCosts = [0]*730
        self.dailyUsers = [0]*730
        self.currentOffice = "Garage"
        self.fundingRound = "Friends&Family"
        self.isReleased = False
        self.hasJob = True
        self.fundraising = False
        self.inDownturn = False
        self.goingViral = False
        self.customerHelped = False
        self.equityStake = 100
        self.founderStake = 100
        self.fairValue = 0
        self.appName = "Unnamed App"
        self.appQuality = 0
        self.qualityOutput = .25
        self.appPublicity = 0
        self.publicityOutput = .25
        self.completedEvents = [False]*100
        self.customerFollowupDate = 10000
        self.fundingDate = 10000
        self.recoveryDate = 10000
        self.stopViralDate = 10000
        #Create display components
        self.initializeDisplay()
        self.begin_time = time.time()

    def initializeDisplay(self):
        #Populate topframe with score data grid
        self.dayLabel = tk.Label(self.scoreFrame, text="Day: " + str(self.currentDay), font='Helvetica 16 bold')
        self.dayLabel.grid(row=0,column=1)
        self.pauseButton = tk.Button(self.scoreFrame, text = "Pause", command = self.pause)
        self.pauseButton.grid(row=0,column=2)
        if self.hasJob:
            self.revenueLabel = tk.Label(self.scoreFrame, text="Job Income: " + str(round(self.dailyRevenue[self.currentDay])), font='Helvetica 10')
        else:
            self.revenueLabel = tk.Label(self.scoreFrame, text="Daily Revenue: " + str(round(self.dailyRevenue[self.currentDay])), font='Helvetica 10')        
        self.revenueLabel.grid(row=1,column=0)
        self.expenseLabel = tk.Label(self.scoreFrame, text="Daily Expenses: " + str(round(self.dailyCosts[self.currentDay],2)), font='Helvetica 10')
        self.expenseLabel.grid(row=1,column=1)
        self.cashflowLabel = tk.Label(self.scoreFrame, text="Daily Cash Flow: " + str(self.dailyRevenue[self.currentDay] - self.dailyCosts[self.currentDay]), font='Helvetica 10')
        self.cashflowLabel.grid(row=1,column=2)

        self.userLabel = tk.Label(self.scoreFrame, text="Daily Active Users: " + str(self.totalUsers), font='Helvetica 10')
        self.userLabel.grid(row=2,column=0)
        self.equityLabel = tk.Label(self.scoreFrame, text="Equity Stake: " + str(self.equityStake) + "%", font='Helvetica 10')
        self.equityLabel.grid(row=2,column=1)
        self.cashLabel = tk.Label(self.scoreFrame, text="Cash Balance: $" + str(self.cash), font='Helvetica 10')
        self.cashLabel.grid(row=2,column=2)
        self.actionsLabel = tk.Label(self.scoreFrame, text="Actions:", font='Helvetica 16 bold')
        self.actionsLabel.grid(row=3,column=1)
        self.fundraisingButton = tk.Button(self.scoreFrame,text="Raise Money",command=self.startFundraising, font='Helvetica 10')
        self.fundraisingButton.grid(row=4,column=0)
        if self.stage != "Ideation" and self.stage != "Validation" and self.fundraising == False:
            self.fundraisingButton['state'] = "normal"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Current Round: " + self.fundingRound, font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        elif self.fundraising == True:
            self.fundraisingButton['state'] = "disabled"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Currently fundraising!", font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        else:
            self.fundraisingButton['state'] = "disabled"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Too early to raise money.", font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        self.hireButton = tk.Button(self.scoreFrame,text="Hire an Employee",command=self.hireEmployee)
        self.hireButton.grid(row=4,column=1)
        if self.stage != "Ideation":
            self.hireButton['state'] = "normal"
            self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
            self.hireLabel.grid(row=5,column=1)
        else:
            self.hireButton['state'] = "disabled"
            self.hireLabel = tk.Label(self.scoreFrame, text="Too early to hire employees.", font='Helvetica 10')
            self.hireLabel.grid(row=5,column=1)
        self.upgradeButton = tk.Button(self.scoreFrame,text="Upgrade Office",command=self.upgradeOffice)
        self.upgradeButton.grid(row=4,column=2)
        if self.completedEvents[13] == True and self.currentOffice != "Corporate Office":
            self.upgradeButton['state'] = "normal"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="Current Office: " + self.currentOffice, font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        elif self.currentOffice == "Corporate Office":
            self.upgradeButton['state'] = "disabled"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="You have the largest office", font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        else:
            self.upgradeButton['state'] = "disabled"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="Too early to change offices.", font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        load = Image.open(officeTypes[self.currentOffice])
        load = load.resize((600, 500), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(load)
        self.officeLabel = tk.Label(self.graphicFrame, image = icon)
        self.officeLabel.image = icon
        #self.officeLabel.place(x=0,y=0,relwidth=1, relheight=1)
        self.officeLabel.pack()
        self.productLabel = tk.Label(self.graphicFrame, text=str(self.appName), font='Helvetica 16 bold')
        self.productLabel.pack()
        self.progressLabel = tk.Label(self.graphicFrame, text="Current Phase: " + self.stage + "      Phase Progress: " + str(round(100*(self.progress / devStages[self.stage]),1)) + "%", font='Helvetica 12')
        self.progressLabel.pack()
        self.scoreLabel = tk.Label(self.graphicFrame, text="App Quality Score: " + str(self.appQuality) + "      App Publicity Score: " + str(self.appPublicity),font='Helvetica 12')
        self.scoreLabel.pack()

    def reinitializeDisplay(self):
        #Populate topframe with score data grid
        self.dayLabel = tk.Label(self.scoreFrame, text="Day: " + str(self.currentDay), font='Helvetica 16 bold')
        self.dayLabel.grid(row=0,column=1)
        if self.hasJob:
            self.revenueLabel = tk.Label(self.scoreFrame, text="Job Income: " + self.money(self.dailyRevenue[self.currentDay]), font='Helvetica 10')
        else:
            self.revenueLabel = tk.Label(self.scoreFrame, text="Daily Revenue: " + self.money(self.dailyRevenue[self.currentDay]), font='Helvetica 10')
        self.revenueLabel.grid(row=1,column=0)
        self.expenseLabel = tk.Label(self.scoreFrame, text="Daily Expenses: " + self.money(self.dailyCosts[self.currentDay]), font='Helvetica 10')
        self.expenseLabel.grid(row=1,column=1)
        self.cashflowLabel = tk.Label(self.scoreFrame, text="Daily Cash Flow: " + self.money(self.dailyRevenue[self.currentDay] - self.dailyCosts[self.currentDay]), font='Helvetica 10')
        self.cashflowLabel.grid(row=1,column=2)

        self.userLabel = tk.Label(self.scoreFrame, text="Daily Active Users: " + str(round(self.totalUsers)), font='Helvetica 10')
        self.userLabel.grid(row=2,column=0)
        self.equityLabel = tk.Label(self.scoreFrame, text="Equity Stake: " + str(round(self.equityStake,2)) + "%", font='Helvetica 10')
        self.equityLabel.grid(row=2,column=1)
        self.cashLabel = tk.Label(self.scoreFrame, text="Cash Balance: " + self.money(self.cash), font='Helvetica 10')
        self.cashLabel.grid(row=2,column=2)
        if self.stage != "Ideation" and self.stage != "Validation" and self.fundraising == False:
            self.fundraisingButton['state'] = "normal"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Current Round: " + self.fundingRound, font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        elif self.fundraising == True:
            self.fundraisingButton['state'] = "disabled"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Currently fundraising!", font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        else:
            self.fundraisingButton['state'] = "disabled"
            self.fundraisingLabel = tk.Label(self.scoreFrame, text="Too early to raise money.", font='Helvetica 10')
            self.fundraisingLabel.grid(row=5,column=0)
        if self.stage != "Ideation" and employeeCaps[self.currentOffice] > self.numEmployees:
            self.hireButton['state'] = "normal"
            self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
            self.hireLabel.grid(row=5,column=1)
        elif employeeCaps[self.currentOffice] <= self.numEmployees:
            self.hireButton['state'] = "disabled"
            self.hireLabel = tk.Label(self.scoreFrame, text="Larger Office Needed.", font='Helvetica 10')
            self.hireLabel.grid(row=5,column=1)
        else:
            self.hireButton['state'] = "disabled"
            self.hireLabel = tk.Label(self.scoreFrame, text="Too early to hire employees.", font='Helvetica 10')
            self.hireLabel.grid(row=5,column=1)
        if self.completedEvents[13] == True and self.currentOffice != "Corporate Office":
            self.upgradeButton['state'] = "normal"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="Current Office: " + self.currentOffice, font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        elif self.currentOffice == "Corporate Office":
            self.upgradeButton['state'] = "disabled"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="You have the largest office", font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        else:
            self.upgradeButton['state'] = "disabled"
            self.upgradeLabel = tk.Label(self.scoreFrame, text="Too early to change offices.", font='Helvetica 10')
            self.upgradeLabel.grid(row=5,column=2)
        self.productLabel = tk.Label(self.graphicFrame, text=str(self.appName), font='Helvetica 16 bold')
        self.productLabel.pack()
        self.progressLabel = tk.Label(self.graphicFrame, text="Current Phase: " + self.stage + "      Phase Progress: " + str(round(100*(self.progress / devStages[self.stage]),1)) + "%", font='Helvetica 12')
        self.progressLabel.pack()
        self.scoreLabel = tk.Label(self.graphicFrame, text="App Quality Score: " + str(self.appQuality) + "      App Publicity Score: " + str(self.appPublicity),font='Helvetica 12')
        self.scoreLabel.pack()

    def mainloop(self):
        #print("entered main loop")
        while True:
            self.window.update()
            if self.begin:
                if self.cash > 0 and self.currentDay < self.microflopRelease and self.fairValue < 1000000000: 
                    print("Day " + str(self.currentDay))
                    self.window.after(DELAY, self.update_game(self.currentDay))
                elif self.cash <= 0:
                    print("Player ran out of cash.")
                    self.begin = False
                    self.gameover = True
                    self.display_gameover("cash")
                elif self.fairValue >= 1000000000:
                    self.begin = False
                    self.gameover = True
                    self.display_victory("unicorn", self.fairValue * (self.equityStake/100))
                else:
                    print("Player ran out of time.")
                    self.begin = False
                    self.gameover = True
                    self.display_gameover("days")
    

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_game(self, day):
        #calculate fair value
        self.valueCompany()
        # Calculate new users (based on game quality, press, random element)
        self.updateUsers(day)
        #Reduce product quality if employee coverage is insufficient
        #self.
        # Add revenues (based on users, price?)
        self.calculateRevenues(day)
        # Decrease costs
        self.calculateCosts(day)
        # Update display
        self.refreshDisplay()
        # Check for / run day-based events -> don't change progress!
        self.get_dayEvent(day)
        # Check for / run other events
        self.get_phaseEvent()
        # Update development % by adding productivity units
        self.developApp(day)
        # Increase day
        self.currentDay += 1

    def refreshDisplay(self):
        self.dayLabel.grid_forget()
        self.revenueLabel.grid_forget()
        self.expenseLabel.grid_forget()
        self.cashflowLabel.grid_forget()
        self.userLabel.grid_forget()
        self.equityLabel.grid_forget()
        self.cashLabel.grid_forget()
        self.fundraisingLabel.grid_forget()
        self.hireLabel.grid_forget()
        self.upgradeLabel.grid_forget()
        self.productLabel.pack_forget()
        self.progressLabel.pack_forget()
        self.scoreLabel.pack_forget()
        self.reinitializeDisplay()

    def calculateCosts(self,day):
        costs = initialCosts
        #Calculate stipend costs
        costs += 80 * self.numCofounders
        # Calculate salary costs
        costs += 200 * self.numEmployees
        #Add office costs
        costs += officeCosts[self.currentOffice]
        #Add variable costs
        if self.stage == "MVP":
            costs += self.totalUsers * .15
        elif self.stage == "Beta":
            costs += self.totalUsers * .25
        elif self.stage == "Full Release":
            costs += self.totalUsers * .275
        #Account for downturn
        if self.inDownturn:
            costs += costs * .1
        # Add to running costs total
        self.totalCosts += costs
        # Add to daily costs array
        self.dailyCosts[day] = costs
        # Subtract from cash balance
        self.cash -= costs

    def calculateRevenues(self,day):
        # Calculate based off of users, price
        revenues = initialRevenue
        if self.hasJob:
            revenues += 215
        # Add sales
        if self.stage == "MVP":
            revenues += self.totalUsers * .2
        elif self.stage == "Beta":
            revenues += self.totalUsers * .3
        elif self.stage == "Full Release":
            revenues += self.totalUsers * .35
        # Add to running revenue total
        self.totalRevenues += revenues
        # Add to daily revenue array
        self.dailyRevenue[day] += revenues
        # Add to cash balance
        self.cash += revenues

    def updateUsers(self,day):
        if self.isReleased:
            # Calculate based off of game quality, press, randomness
            userLoss = max(self.totalUsers * .1 * (random()) * (1 - (self.appQuality / 150)),0)
            newUsers = 5 + (self.appPublicity+10) * self.totalUsers * .003 * random() # can be negative!
            #print(userLoss)
            #print(newUsers)
            if self.inDownturn:
                userLoss = userLoss * 1.25
                newUsers = newUsers * .5
            if self.goingViral:
                newUsers = newUsers * 4 + 20
            # Add to total user count
            self.totalUsers -= userLoss 
            self.totalUsers += newUsers
            # Add to daily user array
            self.dailyUsers[day] = self.totalUsers

    def developApp(self,day):
        # Update productivity based off of employees
        # Update progress based off of daily productivity
        userOutput = self.dailyOutput
        if self.hasJob:
            userOutput = self.dailyOutput / 2
        if self.fundraising:
            userOutput = userOutput / 4
        founderMultiplier = 1
        if self.numCofounders == 1:
            founderMultiplier = 2.5
        elif self.numCofounders == 2:
            founderMultiplier = 3.5
        employeeOutput = self.numEmployees * 3
        officeBoost = officeProductivity[self.currentOffice]
        self.progress += userOutput * founderMultiplier + employeeOutput * (founderMultiplier/3) + officeBoost
        if (self.totalUsers / 1000) > self.numEmployees:
            self.appQuality -= self.qualityOutput + .25
        self.appQuality += self.qualityOutput
        self.appPublicity += self.publicityOutput
        if self.appQuality >= 75:
            self.appQuality -= .5
        if self.appPublicity > 75:
            self.appPublicity -= .5
        if self.appQuality > 100:
            self.appQuality = 100
        if self.appPublicity > 100:
            self.appPublicity = 100
        if self.appQuality < 0:
            self.appQuality = 0
        if self.appPublicity < 0:
            self.appPublicity = 0
        # Check if milestone has been hit
        if self.progress >= devStages[self.stage]:
            self.progress = 0
            self.advanceStage()

    def advanceStage(self):
        if self.stage == "Ideation":
            #Trigger an event
            self.stage = "Validation"
        elif self.stage == "Validation":
            #Trigger an event
            self.stage = "MVP" 
        elif self.stage == "MVP":
            #Trigger an event
            self.hireButton.grid_forget()
            self.hireButton = tk.Button(self.scoreFrame,text="Hire 5 Employees",command=self.hire5Employees)
            self.hireButton.grid(row=4,column=1)
            if self.isReleased==False:
                tk.messagebox.showinfo("App Release","The Beta app has been released. \n$10,000 has been deducted to pay for the launch.")
                self.cash -= 10000
                self.isReleased = True
            self.hasJob = False
            self.stage = "Beta" 
        elif self.stage == "Beta":
            tk.messagebox.showinfo("App Release","Version 1.0 of the app has been released. \n$100,000 has been deducted to pay for the launch.")
            self.cash -= 100000
            self.microflopRelease = 10000
            self.hireButton.grid_forget()
            self.hireButton = tk.Button(self.scoreFrame,text="Hire 25 Employees",command=self.hire25Employees)
            self.hireButton.grid(row=4,column=1)
            #Trigger an event
            self.stage = "Full Release" 
        elif self.stage == "Full Release":
            tk.messagebox.showinfo("App Release","A new version of the app has been released. \n$10,000,000 has been deducted to pay for the launch.")
            self.cash -= 10000000
            self.microflopRelease = 10000
            self.hireButton.grid_forget()
            self.hireButton = tk.Button(self.scoreFrame,text="Hire 100 Employees",command=self.hire100Employees)
            self.hireButton.grid(row=4,column=1)
            #Trigger an event
            self.stage = "New Version" 
        else:
            tk.messagebox.showinfo("App Release","The next version of the app has been released. \n$10,000,000 has been deducted to pay for the launch.")
            self.cash -= 10000000     
    
    def upgradeOffice(self):

        if self.currentOffice == "Clean Garage":
            self.currentOffice = "Small Office"
        elif self.currentOffice == "Small Office":
            self.currentOffice = "Medium Office"
        elif self.currentOffice == "Medium Office":
            self.currentOffice = "Large Office"
        elif self.currentOffice == "Large Office":
            self.currentOffice = "Corporate Office"
        else:
            print("This shouldn't have happened!") 
        self.officeLabel.pack_forget()
        load = Image.open(officeTypes[self.currentOffice])
        load = load.resize((600, 500), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(load)
        self.officeLabel = tk.Label(self.graphicFrame, image = icon)
        self.officeLabel.image = icon
        self.officeLabel.pack(side="top")
        self.refreshDisplay()

    def hireEmployee(self):
        self.numEmployees += 1
        self.hireLabel.grid_forget()
        self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
        self.hireLabel.grid(row=5,column=1)

    def hire5Employees(self):
        self.numEmployees += 5
        self.hireLabel.grid_forget()
        self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
        self.hireLabel.grid(row=5,column=1)

    def hire25Employees(self):
        self.numEmployees += 25
        self.hireLabel.grid_forget()
        self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
        self.hireLabel.grid(row=5,column=1)

    def hire100Employees(self):
        self.numEmployees += 100
        self.hireLabel.grid_forget()
        self.hireLabel = tk.Label(self.scoreFrame, text="Total Employees: " + str(self.numEmployees), font='Helvetica 10')
        self.hireLabel.grid(row=5,column=1)

    def valueCompany(self):
        netIncome = self.dailyRevenue[self.currentDay-1] - self.dailyCosts[self.currentDay-1]
        self.fairValue = netIncome * 600
    
    def startFundraising(self):
        #create window, say "fundraising takes 10 days, during which time"
        def option1():
            self.fundraising = True
            self.fundingDate = self.currentDay + int(random()*7 + 7)
            close()
            
        def option2():
            close()
        
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root) # Turn into canvas?
        promptFrame.pack()
        optionFrame = tk.Frame(root) # Turn into canvas?
        optionFrame.pack(side="bottom")
        b_prompt = tkinter.Label(promptFrame, text="Fundraising: " + self.fundingRound + """\n
        Raising a new round of investment will take 7-14 days, during which time your productivity will be severly diminished.
        \nWould you like to proceed with seeking investors?""")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Seek Investment',command=option1)
        b_1.grid(row=0,column=0)
        b_2 = tk.Button(optionFrame, text='Cancel',command=option2)
        b_2.grid(row=0,column=1)
        root.mainloop()

    def raiseMoney(self):
        
        valuation1 = max(self.dailyRevenue[self.currentDay-1] * 200 * 6,1000000)
        stake1 = max(min((100*round(fundingStages[self.fundingRound]/valuation1,3)),97),2)
        valuation2 =  max(self.dailyRevenue[self.currentDay-1] * 200 * 8,1250000)
        stake2 = max(min(100*round(fundingStages[self.fundingRound]*2/valuation2,3),99.5),3)
        
        def option1():
            self.fundraising = False
            self.cash += fundingStages[self.fundingRound]
            #self.equityStake -= (100 - (self.equityStake / 100)) * stake1
            self.equityStake = 100*((self.equityStake / 100) * (1 - (stake1/100)))
            close()
            
        def option2():
            self.fundraising = False
            self.cash += fundingStages[self.fundingRound] * 2
            #self.equityStake -= (self.equityStake / 100) * stake2
            self.equityStake = 100*((self.equityStake / 100) * (1 - (stake2/100)))
            close()

        def option3():
            self.fundraising = False
            root.quit()
            root.destroy()

        def close():
            if self.fundingRound == "Friends&Family":
                self.fundingRound = "Seed"
            elif self.fundingRound == "Seed":
                self.fundingRound = "Series A"
            elif self.fundingRound == "Series A":
                self.fundingRound = "Series B"
            elif self.fundingRound == "Series B":
                self.fundingRound = "Series C" 
            elif self.fundingRound == "Series C":
                self.fundingRound = "Series D"
            root.quit()
            root.destroy()
            
        root = tkinter.Tk()
        promptFrame = tk.Frame(root) # Turn into canvas?
        promptFrame.pack()
        optionFrame = tk.Frame(root) # Turn into canvas?
        optionFrame.pack(side="bottom")
        b_prompt = tkinter.Label(promptFrame, text="""You have recieved two offers:
        \nOffer 1: """ + self.money(fundingStages[self.fundingRound]) + " for "+ str(round(stake1,2)) + r'% of ' + self.appName + """
        \nOffer 2: """ + self.money(fundingStages[self.fundingRound] * 2) + " for "+ str(round(stake2,2)) + r'% of ' + self.appName)
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Take Offer 1',command=option1)
        b_1.grid(row=0,column=0)
        b_2 = tk.Button(optionFrame, text='Take Offer 2',command=option2)
        b_2.grid(row=0,column=1)
        b_2 = tk.Button(optionFrame, text='Take Neither',command=option3)
        b_2.grid(row=0,column=3)
        root.mainloop()


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_startPage(self):
        self.startPage = True
        self.canvas = Canvas(self.window, width=800, height=800)
        self.canvas.pack()
        size_of_board = 800
        gameover_text = "COMM 4680 Startup Simulator \n"
        self.canvas.create_text(
            size_of_board / 2,
            3.5 * size_of_board / 8,
            font="Helvetica 30 bold",
            fill="black",
            text=gameover_text,
        )
        gameover_text = "Press any key to begin \n"
        self.canvas.create_text(
            size_of_board / 2,
            4.5 * size_of_board / 8,
            font="cmr 20 bold",
            fill="gray",
            text=gameover_text,
        )

    
    def display_gameover(self, reason):
        #Show daily graph!
        self.graphicFrame.destroy()
        self.scoreFrame.destroy()
        #self.canvas.delete("all")
        windowwidth = 700
        windowheight = 300
        self.canvas = Canvas(self.window, width=windowwidth, height=windowheight)
        self.canvas.pack()
        if reason == 'cash':
            gameover_text = "Your business ran out of cash. \n"
        elif reason == 'days':
            gameover_text = "Microflop beat you to the market!"
        self.canvas.create_text(
            windowwidth / 2,
            1 * windowheight / 6,
            font="cmr 20 bold",
            fill="red",
            text=gameover_text,
        )
        score = self.money(self.totalRevenues)
        score_text = "Total Revenue: \n"
        self.canvas.create_text(
            windowwidth / 2,
            3 * windowheight / 6,
            font="cmr 20 bold",
            fill="black",
            text=score_text,
        )
        self.canvas.create_text(
            windowwidth / 2,
            3.5 * windowheight / 6,
            font="cmr 30 bold",
            fill="gray",
            text=score,
        )
        days_lasted = "Your business lasted " + str(self.currentDay) + ' days'
        self.canvas.create_text(
            windowwidth / 2,
            5 * windowheight / 6,
            font="cmr 20 bold",
            fill="black",
            text=days_lasted,
        )
        """
        score_text = "Press any button to play again \n"
        self.canvas.create_text(
            windowwidth / 2,
            14 * windowheight / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )"""
        figure = plt.Figure(figsize=(6,4), dpi=90)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self.window)
        self.chart = chart_type.get_tk_widget()
        self.chart.pack()
        data = {'Revenue':self.dailyRevenue[:self.currentDay],'Expenses':self.dailyCosts[:self.currentDay],'Users':self.dailyUsers[:self.currentDay]}
        df = pd.DataFrame(data,columns=['Revenue','Expenses','Users'])
        #df = df[['First Column','Second Column']].groupby('First Column').sum()
        df.plot(kind='line', legend=True, ax=ax)
        ax.set_title('Company Performance')
        self.playAgain = tk.Label(self.window, text = "Press any button to play again!",font="cmr 16 bold")
        self.playAgain.pack()
    
    def display_victory(self, reason, networth):
        self.graphicFrame.destroy()
        self.scoreFrame.destroy()


        windowwidth = 700
        windowheight = 300
        self.canvas = Canvas(self.window, width=windowwidth, height=windowheight)
        self.canvas.pack()
        

        self.canvas.create_text(
            windowwidth / 2,
            1 * windowheight / 6,
            font="cmr 30 bold",
            fill=Green_color,
            text="Congratulations!",
        )
        if reason == 'unicorn':
            victory_text = "You built a software unicorn! \n"
        elif reason == 'ipo':
            victory_text = "You successfully brought your company public!"
        elif reason == 'buyout':
            victory_text = 'You sold your company!'
        self.canvas.create_text(
            windowwidth / 2,
            2 * windowheight / 6,
            font="cmr 20 bold",
            fill=Green_color,
            text=victory_text,
        )
        self.canvas.create_text(
            windowwidth / 2,
            3 * windowheight / 6,
            font="cmr 16 bold",
            fill="gray",
            text="Your Final Net Worth:",
        )
        self.canvas.create_text(
            windowwidth / 2,
            3.5 * windowheight / 6,
            font="cmr 16 bold",
            fill=Green_color,
            text=self.money(networth),
        )
        ###
        offset = 120
        self.canvas.create_text(
            windowwidth / 3 - offset,
            5 * windowheight / 6,
            font="cmr 16 bold",
            fill="gray",
            text="Total Revenue",
        )
        self.canvas.create_text(
            2 * windowwidth / 3- offset,
            5 * windowheight / 6,
            font="cmr 16 bold",
            fill="gray",
            text="Total Users",
        )
        self.canvas.create_text(
            3 * windowwidth / 3- offset,
            5 * windowheight / 6,
            font="cmr 16 bold",
            fill="gray",
            text="Company Value",
        )
        self.canvas.create_text(
            windowwidth / 3 - offset,
            5.5 * windowheight / 6,
            font="cmr 16 bold",
            fill=Green_color,
            text=self.money(self.totalRevenues),
        )
        self.canvas.create_text(
            2 *windowwidth / 3 - offset,
            5.5 * windowheight / 6,
            font="cmr 16 bold",
            fill=Green_color,
            text=round(self.totalUsers),
        )
        self.canvas.create_text(
            3 * windowwidth / 3 - offset,
            5.5 * windowheight / 6,
            font="cmr 16 bold",
            fill=Green_color,
            text=self.money(self.fairValue),
        )

        figure = plt.Figure(figsize=(6,4), dpi=90)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self.window)
        self.chart = chart_type.get_tk_widget()
        self.chart.pack()
        data = {'Revenue':self.dailyRevenue[:self.currentDay],'Expenses':self.dailyCosts[:self.currentDay],'Users':self.dailyUsers[:self.currentDay]}
        df = pd.DataFrame(data,columns=['Revenue','Expenses','Users'])
        #df = df[['First Column','Second Column']].groupby('First Column').sum()
        df.plot(kind='line', legend=True, ax=ax)
        ax.set_title('Company Performance')
        self.playAgain = tk.Label(self.window, text = "Press any button to play again!",font="cmr 16 bold")
        self.playAgain.pack()

    def center(self,toplevel):
        # Tkinter way to find the screen resolution
        #toplevel = self.window
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.window.geometry("+%d+%d" % (x, y))
        #self.window.title("Centered!") 

    # ------------------------------------------------------------------
    # Day-Based Event Functions:
    # 
    # ------------------------------------------------------------------
    def intro(self): # Intro
        # Let's create a alert box with 'messagebox' function
        tk.messagebox.showinfo("Introduction", """      Welcome to the COMM 4680 Startup Simulator! \n \n
            The goal of this game is to launch, grow, and successfully exit a business before you run out of cash.
        \nYou’ll make important decisions along the way that will affect your chances of success; the hidden effects of these decisions are based upon in-class learnings, but there is no one correct way to play.
        \nYour final score will depend on how much equity you own upon exiting the business, as well as the total value of your business.
        \nI hope you’ll play through multiple times to see how different decisions might play out, as you try to build a software unicorn! """)
 
    def background(self): # Name App
        tk.messagebox.showinfo("Background Information", """The Scenario: \n 
        You recently graduated from a top public university with a computer science degree, but you are currently living in your parent’s home. After a few months at a mid-size tech company, you’ve decided that the corporate life is not for you. It’s time to start your own business.
        \nAll together, you can put together $10,000 in savings to fund your project. You’ll maintain your day job ($215 / day) while you try to come up with an idea.""")
    
    def microflopWarning(self): #Time to name your app
        tk.messagebox.showinfo("Microflop Competition", """You’ve just received a tip from a buddy at Microflop -- Apparently, they’re putting together an incredibly similar app. They only have a small team on the project, so it is currently expected to launch in 200 days.
The app is highly dependent on network effects, so if Microflop beats you to the market, your app will almost certainly flop.
        """)

        return "April"
    
    def buyout(self):
        def option1():
            self.begin = False
            self.gameover = True
            self.display_victory("buyout", offersize)
            close()
        
        def option2():
            close()
        
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root) # Turn into canvas?
        promptFrame.pack()
        optionFrame = tk.Frame(root) # Turn into canvas?
        optionFrame.pack(side="bottom")
        value2 = self.dailyRevenue[self.currentDay - 1] * 200 * 6
        offersize = max(round(self.fairValue * (self.equityStake / 100)), round(value2 * (self.equityStake / 100)))
        b_prompt = tkinter.Label(promptFrame, text="You've recieved an offer from Microflop to buy out your entire stake in " + self.appName + " for " + self.money(offersize) + "\nYou would cede all control of the company.")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Accept the offer',command=option1)
        b_1.grid(row=0,column=0)
        b_1a = tk.Label(optionFrame, text='Retire early. Game ends, victory conditions met.')
        b_1a.grid(row=0,column=1)
        b_2 = tk.Button(optionFrame, text='Reject the offer',command=option2)
        b_2.grid(row=1,column=0)
        b_2a = tk.Label(optionFrame, text='Microflop has no idea how big ' + self.appName + " will be.")
        b_2a.grid(row=1,column=1)
        root.mainloop()
    
    def ipo(self):
        def option1():
            self.begin = False
            self.gameover = True
            self.display_victory("ipo", self.fairValue * (self.equityStake / 100))
            close()
        
        def option2():
            close()
        
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root)
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        offersize = round(self.fairValue * (self.equityStake / 100))
        b_prompt = tkinter.Label(promptFrame, text="Your board has approached you about a potential IPO.")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Go Public',command=option1)
        b_1.grid(row=0,column=0)
        b_1a = tk.Label(optionFrame, text='Your shares become liquid. Game ends, victory conditions met.')
        b_1a.grid(row=0,column=1)
        b_2 = tk.Button(optionFrame, text='Stay Private',command=option2)
        b_2.grid(row=1,column=0)
        b_2a = tk.Label(optionFrame, text="It's too early.")
        b_2a.grid(row=1,column=1)
        root.mainloop()
        return "June"

    def lawsuit(self): 
        def option1():
            self.cash -= lawsuitSize
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root) # Turn into canvas?
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        lawsuitSize = round(self.totalUsers * (5 + random()*10))
        b_prompt = tkinter.Label(promptFrame, text="After a lengthy investigation, the EU has imposed a heavy " + self.money(lawsuitSize) + " penalty for your data mismanagement practices that resulted in the Day " + str(self.databreachDate) + " data breach.")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Pay fine',command=option1)
        b_1.pack()
        root.mainloop()

    def hiringWarning(self): 
        if self.numEmployees == 0:
            def option1():
                self.cash -= lawsuitSize
                close()
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root)
            optionFrame.pack(side="bottom")
            lawsuitSize = round(self.totalUsers * (5 + random()*10))
            b_prompt = tkinter.Label(promptFrame, text="""Remember to frequently hire employees!
            \nNot only do you need to beat Microflop to market, but users will start to become upset if you don't have enough employees to perform customer service""")
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
            b_1.pack()
            root.mainloop()

    def downturn(self):
        def option1():
            self.inDownturn = True
            self.recoveryDate = self.downturnDate + 30
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root)
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        shockType = possibleShocks[round(random()*2)]
        shockLength = 10 + random() * 30
        lawsuitSize = round(self.totalUsers * (5 + random()*10))
        b_prompt = tkinter.Label(promptFrame, text="""It's not always your fault.
        \nDue to a major """ + shockType + """, the economy has experienced a major shock.
        \nDemand will be diminished, and costs will be slightly raised for the next """+ str(round(shockLength)) + " days." )
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
        b_1.pack()
        root.mainloop()

    def recovery(self):
        def option1():
            self.inDownturn = False
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root)
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        b_prompt = tkinter.Label(promptFrame, text="""The economic shock has subsided.
        \nBusiness is back to normal.""")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
        b_1.pack()
        root.mainloop()

    def databreach(self):
        def option1():
            self.totalUsers -= breachSize / 3
            self.appPublicity -= 40
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root)
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        breachSize = round(self.totalUsers / (1 + 3 * random()))
        b_prompt = tkinter.Label(promptFrame, text="""You've been the victim of a major data breach.
        \nThe personal data of """ + str(breachSize) + " users has been compromised. Many of those users will not return.")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
        b_1.pack()
        root.mainloop()

    def goViral(self):
        def option1():
            self.goingViral = True
            self.endViralDate = self.viralDate + viralLength
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root)
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        viralLength = 5 + random() * 20
        lawsuitSize = round(self.totalUsers * (5 + random()*10))
        b_prompt = tkinter.Label(promptFrame, text="""Your app has gone viral!\nNew user adoption will skyrocket for the next couple weeks""")
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
        b_1.pack()
        root.mainloop()

    def endViral(self):
        self.goingViral = False

    def get_dayEvent(self,argument): #Day-based
        switcher = {
            1: self.intro,
            2: self.background,
            50: self.microflopWarning,
            60: self.hiringWarning,
            200: self.buyout,
            300: self.buyout,
            400: self.ipo,
            self.fundingDate: self.raiseMoney,
            self.lawsuitDate: self.lawsuit,
            self.downturnDate: self.downturn,
            self.databreachDate: self.databreach,
            self.viralDate: self.goViral,
            self.recoveryDate: self.recovery,
            self.stopViralDate: self.endViral,
            self.customerFollowupDate: self.customerFollowup
            #7: seven,
            #8: eight,
            #9: nine,
            #10: ten,
            #11: eleven,
            #12: twelve
        }
        # Get the function from switcher dictionary
        event = switcher.get(argument, lambda: "")
        # Execute the function
        event()
    
    
    # ------------------------------------------------------------------
    # Other Event Functions:
    # 
    # ------------------------------------------------------------------
    def get_phaseEvent(self):
        #if self.stage == "Ideation" and self.progress > 10:
        #    self.dayJob()
        if self.stage == "Validation" and self.progress == 0:
            self.ideaSelection()
        elif self.stage == "Validation" and self.progress > 5 and self.progress < 15:
            self.nameSelection()
        elif self.stage == "Validation" and self.progress > 15 and self.progress < 50:
            self.dayJob()
        elif self.stage == "Validation" and self.progress > 50:
            self.officeSelection()
        elif self.stage == "MVP" and self.progress == 0:
            self.teamSelection()
        elif self.stage == "Beta" and self.progress > 10 and self.progress < 50:
            self.angryCustomer()
        elif self.stage == "MVP" and self.progress > 300:
            self.earlyRelease()
        elif self.stage == "Full Release" and self.progress > 300:
            self.someEvent()

    def ideaSelection(self):
        eventID = 10
        if self.completedEvents[eventID] == False:
            def option1():
                #organic
                self.organic = True
                self.qualityOutput = .5
                close()
            
            def option2():
                #inorganic
                self.organic = False
                self.publicityOutput = .5
                close()
            
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""After doing some research and brainstorming, you've identified two promising ideas:\n
            Idea 1: Organic - You’ve identified a problem in your life that an app could easily solve. \nYou’re sure that you can effectively solve this problem, but it’s unclear how many people share this issue.
            \nIdea 2: Inorganic - You’ve identified a product niche isn’t being adequately addressed by current solutions. \nYou can’t entirely relate to this problem, but you know there’s a huge potential market.
            """)
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Organic Idea',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Increases product quality, may limit market size')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Inorganic Idea',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text='Increases market size, may hinder product quality.')
            b_2a.grid(row=1,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True
        #

    def nameSelection(self):
        eventID = 11
        if self.completedEvents[eventID] == False:
            def action():
                self.appName = b_input.get()
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            b_prompt = tkinter.Label(root, text='Select a name for your app! Choose something catchy:')
            b_prompt.pack()
            b_input = tk.Entry(root)
            b_input.pack()
            b_submit = tk.Button(root, text='Submit',command=action)
            b_submit.pack()
            root.mainloop()
        """self.productLabel.pack_forget()
        self.productLabel = tk.Label(self.graphicFrame, text=str(self.appName), font='Helvetica 16 bold')
        self.productLabel.pack()"""
        self.completedEvents[eventID] = True
        return 0

    def dayJob(self):
        eventID = 12
        if self.completedEvents[eventID] == False:
            def option1():
                #day job kept (for now)
                close()
            
            def option2():
                #go all-in
                self.hasJob = False
                close()
            
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""You work dreary 9am-5pm days for a medium-sized tech company, making roughly $1,500 per week. 
            \nShould you keep your job to help finance your business, or quit to spend all of your time on your business? """)
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Keep your day job',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Maintain income stream until app is launched')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Go All-In',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text='Lose income stream, dramatically increase productivity.')
            b_2a.grid(row=1,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True
        return 0

    def officeSelection(self):
        eventID = 13
        if self.completedEvents[eventID] == False:
            def option1():
                self.progress -= self.dailyOutput * 2
                self.currentOffice = "Clean Garage"
                close()
            
            def option2():
                self.currentOffice = "Small Office"
                close()
            
            def close():
                self.officeLabel.pack_forget()
                load = Image.open(officeTypes[self.currentOffice])
                load = load.resize((600, 500), Image.ANTIALIAS)
                icon = ImageTk.PhotoImage(load)
                self.officeLabel = tk.Label(self.graphicFrame, image = icon)
                self.officeLabel.image = icon
                self.officeLabel.pack(side="top")
                self.refreshDisplay()
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""You’re currently working out of your parent’s garage, which is quite dark and messy. \nYou wonder if you could be more productive if you rented out a small office space.""")
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Organize your garage',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Spend two days, slightly increase productivity')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Rent a small office',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text='Increase costs, increase productivity.')
            b_2a.grid(row=1,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True
        return 0

    def teamSelection(self):
        eventID = 14
        if self.completedEvents[eventID] == False:
            def option1():
                #go it alone
                close()
            
            def option2():
                #something else
                self.equityStake = 66.6
                self.numCofounders = 1
                self.qualityOutput += .25
                close()

            def option3():
                #something else
                self.equityStake = 50.0
                self.numCofounders = 2
                self.qualityOutput += .5
                close()
            
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""You’ve just finished validating your idea with your family and peers, and you’ve gotten some overwhelmingly positive feedback. 
            \nTwo of your smartest friends (both software engineers) are so interested that they’ve asked to join as co-founders. 
            \nYou’re fairly confident that you could build the app alone, but you know how important it is to bounce ideas off of others.\n""")
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Go it alone',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Keep all equity, diminish productivity and quality')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Start with 1 co-founder',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text='Grant co-founder 1/3 of business and a small stipend, increase productivity and quality.')
            b_2a.grid(row=1,column=1)
            b_3 = tk.Button(optionFrame, text='Start with 2 co-founders',command=option3)
            b_3.grid(row=2,column=0)
            b_3a = tk.Label(optionFrame, text='Grant each co-founder 1/4 of business and a small stipend, greatly increase productivity and quality.')
            b_3a.grid(row=2,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True
        return 0

    def earlyRelease(self):
        eventID = 15
        if self.completedEvents[eventID] == False:
            def option1():
                #do something
                self.hasJob = False
                self.isReleased = True
                self.cash -= 10000
                self.appPublicity -= 25
                self.appQuality += 5
                close()
            
            def option2():
                #something else
                close()
            
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""Your app is working, albeit with absolute minimum functionality. 
            \nYou’d love to start getting some user feedback, but you’re worried about receiving negative publicity due to how unfinished the product is.
            \nReleasing the App requires a $10,000 upfront investment
""")
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Release Early',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Release to your email list, asking for feedback.')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Wait',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text='Wait until Beta version to avoid negative publicity.')
            b_2a.grid(row=1,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True
        return 0

    def angryCustomer(self):
        eventID = 19
        if self.completedEvents[eventID] == False:
            def option1():
                #help the customer
                self.progress -= self.dailyOutput
                self.customerHelped = True
                self.customerFollowupDate = self.currentDay + 10
                close()
            
            def option2():
                #Ignore the customer
                self.customerHelped = False
                self.customerFollowupDate = self.currentDay + 10
                close()
            
            def close():
                root.quit()
                root.destroy()
            root = tkinter.Tk()
            promptFrame = tk.Frame(root) # Turn into canvas?
            promptFrame.pack()
            optionFrame = tk.Frame(root) # Turn into canvas?
            optionFrame.pack(side="bottom")
            b_prompt = tkinter.Label(promptFrame, text="""You've just recieved a very strongly-worded email from an angry early adopter.
            \nThe customer claims that an update for """ + self.appName + """ deleted his precious photograph files, and demands some kind of retribution.
            \nHow do you handle the situation?""")
            b_prompt.pack()
            b_1 = tk.Button(optionFrame, text='Help the Customer',command=option1)
            b_1.grid(row=0,column=0)
            b_1a = tk.Label(optionFrame, text='Spend a day on the phone with the customer, helping locate his files.')
            b_1a.grid(row=0,column=1)
            b_2 = tk.Button(optionFrame, text='Ignore the Customer',command=option2)
            b_2.grid(row=1,column=0)
            b_2a = tk.Label(optionFrame, text="The founder can't possibly waste his time on such a small, unscalable issue. ")
            b_2a.grid(row=1,column=1)
            root.mainloop()
        self.completedEvents[eventID] = True

    def customerFollowup(self):
        def option1():
            close()
        def close():
            root.quit()
            root.destroy()
        root = tkinter.Tk()
        promptFrame = tk.Frame(root) # Turn into canvas?
        promptFrame.pack()
        optionFrame = tk.Frame(root)
        optionFrame.pack(side="bottom")
        if self.customerHelped:
            promptText = """Remember that customer you helped out last week? He just sent out a blog post with 
            \neffusive praise for your incredible customer support. Good call!"""
            self.appPublicity += 10
        else:
            promptText = """Bad News -- Turns out, the customer that you ignored last week writes for TechCrunch, 
            \nand he just published a scathing artical about """ + self.appName + """. That's gonna hurt business."""
            self.appPublicity -= 20
        b_prompt = tkinter.Label(promptFrame, text=promptText)
        b_prompt.pack()
        b_1 = tk.Button(optionFrame, text='Acknowledge',command=option1)
        b_1.pack()
        root.mainloop()

    def someEvent(self):
        return 0
     
    def money(self,amount):
        return str("${:,.2f}".format(amount))

    def pause(self):
        self.begin = False
        self.pauseButton.grid_forget()
        self.pauseButton = tk.Button(self.scoreFrame, text = "Resume", command = self.resume)
        self.pauseButton.grid(row=0,column=2)

    def resume(self):
        self.begin = True
        self.pauseButton.grid_forget()
        self.pauseButton = tk.Button(self.scoreFrame, text = "Pause", command = self.pause)
        self.pauseButton.grid(row=0,column=2)

    def key_input(self, event):
            key_pressed = event.keysym
            # print(key_pressed)
            if self.startPage == True:
                self.begin = True
                self.startPage = False
                self.play_again()
            elif self.gameover == True:
                self.canvas.destroy()
                self.chart.destroy()
                self.playAgain.destroy()
                self.scoreFrame = tk.Frame(self.window)
                self.scoreFrame.pack()
                self.graphicFrame = tk.Frame(self.window) # Turn into canvas?
                self.graphicFrame.pack(side="bottom")
                self.begin = True
                self.play_again()
            self.last_key = key_pressed

class Mbox(object):

    root = None

    def __init__(self, msg, dict_key=None):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        tki = tkinter
        self.top = tki.Toplevel(Mbox.root)

        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        label = tki.Label(frm, text=msg)
        label.pack(padx=4, pady=4)

        caller_wants_an_entry = dict_key is not None

        if caller_wants_an_entry:
            self.entry = tki.Entry(frm)
            self.entry.pack(pady=4)

            b_submit = tki.Button(frm, text='Submit')
            b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            b_submit.pack()

        b_cancel = tki.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, this, dict_key):
        data = this.entry.get()
        if data:
            d, key = dict_key
            d[key] = data
            this.top.destroy()
            self.top.destroy()


game_instance = StartUpSim()
game_instance.mainloop()