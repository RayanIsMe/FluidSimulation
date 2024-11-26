import random, math
import pandas as pd
import streamlit as st

#CLASS ------------------------------------
class particle:
    x, y, Vx, Vy = 0, 0, 0, 0
    def __init__(self, x, y, Vx, Vy):
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy

class object(particle):
    def __init__(self, x, y, Vx, Vy):
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy

#VARIABLES-------------------------------------------

#defining variables
time = 0 #variable keeping track of number of interations. This variable increases by one every time the program runs through the while loop.
particleCount = 0 #variable to keep track of number of particles

#border
Bx = 30 #length of area of scatter plot x
By = 10 #height of area of scatter plot y

#control variables
initspeed = 0.7 #initial speed the particle travels at
numberofparticlesnew = 6 #number of particles that are added per time frame
energylose = 0.7 #amount of energy lost when colliding with edge
repulsiveDistance = 0.5
repulsiveStrength = 0.05

#PLOTTING----------------------------------------------
pltx = []
plty = []

#defining particles
p = [] #object list for air particle objects
ob = [] #object list for object particle objects

#OBJECT DEFINITION-----------------------------------------------------------------------------------------------
objCount = 0 #keeps track of number of object particles. Stays constant
for h in range(64):
    ob.append(object(10+(h/32), 5+(h/16), 0, 0))
    ob.append(object(10+(h/8), 5-(h/20), 0, 0))
    objCount += 2

while True:  # LOOP STARTS
    # SETTING VARIABLES AND LIST TO 0
    pltx = []
    plty = []
    deleteList = []

    time += 1  # add one to time variable every time we go through the loop

    # Add particles every increment of this condition. If initial speed is higher,
    # more frequent new particles to simulate constant density
    if time % int(2 / initspeed) == 0:
        for i in range(numberofparticlesnew):
            # create a new particle with initial x velocity and initial random vertical position
            p.append(particle(0, random.randint(0, By - 1) + random.random(), initspeed, 0))
            particleCount += 1

    # LOOPING PARTICLES-------------------------------------------------------------------------
    for i in range(particleCount):

        # Border collision
        if p[i].y < 0:
            p[i].y = 0
            p[i].Vy *= -energylose
        elif p[i].y > By:
            p[i].y = By
            p[i].Vy *= -energylose

        if p[i].x < 0:
            p[i].x = 0
            p[i].Vx *= -energylose
        elif p[i].x > Bx:
            deleteList.append(i)

        # REPULSIVE FORCE FROM OTHER PARTICLES
        for j in range(particleCount):
            if i != j:
                # Distance variable stores numerical value of distance between two particles
                distance = ((p[i].x - p[j].x) ** 2 + (p[i].y - p[j].y) ** 2) ** 0.5
                if distance < repulsiveDistance:
                    # Find the angle
                    if p[j].x - p[i].x != 0:
                        angle = math.atan((p[j].y - p[i].y) / (p[j].x - p[i].x))
                    else:
                        angle = 90

                    # Change velocity of particle[i]
                    if p[i].x <= p[j].x:
                        p[i].Vx += -math.cos(angle) * (repulsiveDistance / distance) * repulsiveStrength
                        p[i].Vy += -math.sin(angle) * (repulsiveDistance / distance) * repulsiveStrength
                    elif p[i].x >= p[j].x:
                        p[i].Vx += math.cos(angle) * (repulsiveDistance / distance) * repulsiveStrength
                        p[i].Vy += math.sin(angle) * (repulsiveDistance / distance) * repulsiveStrength

            # UPDATE POSITIONS
            p[i].x += p[i].Vx
            p[i].y += p[i].Vy

            #ADD PLOTS
            pltx.append(p[i].x)
            plty.append(p[i].y)

        

        #DELETE REQUIRED OBJECTS
        for j in range(len(deleteList)):
            del p[deleteList[j]]
            n = n-1

        #PLOTTING
        pltxy = [pltx, plty]
        df = pd.DataFrame(pltxy)
        st.write(df)
        plotdata = st.DataFrame(data = df)
        st.scatter_chart(data = plotdata)
        

