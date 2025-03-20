import random, math
import pandas as pd
import numpy as np
import streamlit as st
import time

placeholder = st.empty()
text = st.empty()

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
    

if 'SS' not in st.session_state:
    st.session_state['SS'] = 1

if st.session_state['SS'] == 1:
    
    #VARIABLES-------------------------------------------

    #defining variables
    st.session_state["timeP"] = 0 #variable keeping track of number of interations. This variable increases by one every time the program runs through the while loop.
    st.session_state["particleCount"] = 0 #variable to keep track of number of particles
    
    #border
    st.session_state["Bx"] = 30 #length of area of scatter plot x
    st.session_state["By"] = 10 #height of area of scatter plot y
    
    #control variables
    st.session_state["initialSpeed"] = 0.5 #initial speed the particle travels at
    st.session_state["newParticles"] = 6 #number of particles that are added per time frame
    st.session_state["energyLoss"] = 0.7 #amount of energy lost when colliding with edge
    st.session_state["repulsiveDistance"] = 0.5
    st.session_state["repulsiveStrength"] = 0.05
    st.session_state["objectStrength"] =  0.05 * st.session_state["initialSpeed"] * 4
    st.session_state["objectDistance"] = 1

    #analysis tools
    st.session_state["forcex"] = 0
    st.session_state["forcey"] = 0
    
    #defining particles
    st.session_state["p"] = [] #object list for air particle objects
    st.session_state["ob"] = [] #object list for object particle objects

    #plotting lists
    st.session_state["plotx"] = []
    st.session_state["ploty"] = []
    st.session_state["its"] = 50
    
    #OBJECT DEFINITION-----------------------------------------------------------------------------------------------
    st.session_state["objCount"] = 0 #keeps track of number of object particles. Stays constant
    # for h in range(32):
    #     st.session_state["ob"].append(object(10+(h/16), 5+(h/16), 0, 0))
    #     st.session_state["ob"].append(object(10+(h/4), 5-(h/20), 0, 0))
    #     st.session_state["objCount"] += 2
    
    st.session_state['SS'] = 2
    st.rerun()

elif st.session_state['SS'] == 2: #-----------------------------------------------------------------------------------------------------------------------
    # SETTING VARIABLES AND LIST TO 0
        
    pltx = []
    pltx.append(0)
    pltx.append(st.session_state["Bx"])
    plty = []
    plty.append(0)
    plty.append(st.session_state["By"])
    deleteList = []

    st.session_state["timeP"] += 1  # add one to time variable every time we go through the loop

    # Add particles every increment of this condition. If initial speed is higher,
    # more frequent new particles to simulate constant density
    if st.session_state["timeP"] % 5 == 0:   #int(2 / st.session_state["initialSpeed"])
        #st.write("NEW PARTICLES")
        for i in range(st.session_state["newParticles"]):
            # create a new particle with initial x velocity and initial random vertical position
            st.session_state["p"].append(particle(0, random.randint(0, st.session_state["By"] - 1) + random.random(), st.session_state["initialSpeed"], 0))
            st.session_state["particleCount"] += 1
        

    # LOOPING PARTICLES-----------------------------------------------------------------------------------------------------------------------------------------
    for i in range(st.session_state["particleCount"]):

        # UPDATE POSITIONS
        st.session_state["p"][i].x += st.session_state["p"][i].Vx
        st.session_state["p"][i].y += st.session_state["p"][i].Vy

        # Border collision
        if st.session_state["p"][i].y < 0:
            st.session_state["p"][i].y = 0
            st.session_state["p"][i].Vy *= -st.session_state["energyLoss"]
        elif st.session_state["p"][i].y > st.session_state["By"]:
            st.session_state["p"][i].y = st.session_state["By"]
            st.session_state["p"][i].Vy *= -st.session_state["energyLoss"]

        if st.session_state["p"][i].x < 0:
            st.session_state["p"][i].x = 0
            st.session_state["p"][i].Vx *= -st.session_state["energyLoss"]
        elif st.session_state["p"][i].x > st.session_state["Bx"]:
            deleteList.append(i)

        # REPULSIVE FORCE FROM OTHER PARTICLES
        for j in range(st.session_state["particleCount"]):
            if i != j:
                # Distance variable stores numerical value of distance between two particles
                distance = ((st.session_state["p"][i].x - st.session_state["p"][j].x) ** 2 + (st.session_state["p"][i].y - st.session_state["p"][j].y) ** 2) ** 0.5
                if distance < st.session_state["repulsiveDistance"]:
                    # Find the angle
                    if st.session_state["p"][j].x - st.session_state["p"][i].x != 0:
                        angle = math.atan((st.session_state["p"][j].y - st.session_state["p"][i].y) / (st.session_state["p"][j].x - st.session_state["p"][i].x))
                    else:
                        angle = 90

                    # Change velocity of particle[i]
                    if st.session_state["p"][i].x <= st.session_state["p"][j].x:
                        if distance != 0:
                                st.session_state["p"][i].Vx += -math.cos(angle) * (st.session_state["repulsiveDistance"] / distance) * st.session_state["repulsiveStrength"]
                                st.session_state["p"][i].Vy += -math.sin(angle) * (st.session_state["repulsiveDistance"] / distance) * st.session_state["repulsiveStrength"]
                    elif st.session_state["p"][i].x >= st.session_state["p"][j].x:
                        if distance != 0:
                                st.session_state["p"][i].Vx += math.cos(angle) * (st.session_state["repulsiveDistance"] / distance) * st.session_state["repulsiveStrength"]
                                st.session_state["p"][i].Vy += math.sin(angle) * (st.session_state["repulsiveDistance"] / distance) * st.session_state["repulsiveStrength"]


            # REPULSIVE FORCE FROM objects
            for j in range(len(st.session_state["ob"])):

                #if in range
                distance = ((st.session_state["p"][i].x - st.session_state["ob"][j].x)**2 + (st.session_state["p"][i].y - st.session_state["ob"][j].y)**2)**0.5
                if distance < st.session_state["objectDistance"]:

                    #find the angle
                    if st.session_state["ob"][j].x - st.session_state["p"][i].x != 0:
                        angle = math.atan((st.session_state["ob"][j].y - st.session_state["p"][i].y)/(st.session_state["ob"][j].x - st.session_state["p"][i].x))
                    else:
                        angle = 90
                    
                    #chnage velocity
                    if st.session_state["p"][i].x < st.session_state["ob"][j].x:
                        st.session_state["p"][i].Vx += -math.cos(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["p"][i].Vy += -math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcex"] += math.cos(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcey"] += math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                    elif st.session_state["p"][i].x > st.session_state["ob"][j].x:
                        st.session_state["p"][i].Vx += math.cos(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["p"][i].Vy += math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcex"] += -math.cos(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcey"] += -math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                    elif st.session_state["p"][i].y > st.session_state["ob"][j].y:
                        st.session_state["p"][i].Vy += math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcey"] += -math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                    else:
                        st.session_state["p"][i].Vy += -math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                        st.session_state["forcey"] += math.sin(angle) * (distance/st.session_state["objectDistance"]) * st.session_state["objectStrength"]
                    



        

        #ADD PLOTS
        pltx.append(st.session_state["p"][i].x)
        plty.append(st.session_state["p"][i].y)

        
    #DELETE REQUIRED OBJECTS
    for j in range(len(deleteList)):
            del st.session_state["p"][deleteList[j]]
            st.session_state["particleCount"] -= 1


    for j in range(len(st.session_state["ob"])):
            pltx.append(st.session_state["ob"][j].x)
            plty.append(st.session_state["ob"][j].y)

    st.session_state["timeP"] += 1
    #PLOTTING


    st.session_state["plotx"].append(pltx)
    st.session_state["ploty"].append(plty)

    
    placeholder.write(st.session_state["timeP"])

    if st.session_state["timeP"] > st.session_state["its"]+2:
                st.session_state['SS'] = 3
                st.session_state["timeP"] = 0

    st.button("rerun")
                
elif st.session_state['SS'] == 3: #---------------------------------------------------------------------------------------------------------------------------------------
        if st.session_state["timeP"] < st.session_state["its"]:
                st.session_state["timeP"] += 1
                df = pd.DataFrame({
                    'x': st.session_state["plotx"][st.session_state["timeP"]-1],
                    'y': st.session_state["ploty"][st.session_state["timeP"]-1],
                })
                
                with placeholder.container():
                        st.scatter_chart(data = df, x = 'x', y = 'y', width = 700, height = 400)
                        # st.write(st.session_state["timeP"])
                        # st.write(st.session_state["plotx"][st.session_state["timeP"]-1])
                        # st.write( st.session_state["ploty"][st.session_state["timeP"]-1])
                time.sleep(0.1)
                st.rerun()
        else:
                st.write("Over")
            
        

