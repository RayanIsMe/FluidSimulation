import random, math

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

'''defining varaibles'''
time = 0 #variable keeping track of number of interations. This variable increases by one every time the program runs through the while loop.
particleCount = 0 #variable to keep track of number of particles

'''borders'''
Bx = 30 #length of area of scatter plot x
By = 10 #height of area of scatter plot y

'''control variables'''
initspeed = 0.7 #initial speed the particle travels at
numberofparticlesnew = 6 #number of particles that are added per time frame
energylose = 0.7 #amount of energy lost when colliding with edge
repulsiveDistance = 0.5

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

while True: #LOOP STARTS|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

  #SETTING VARIABLES AND LIST TO 0
  pltx = []
  plty = []
  deleteList = []

  time += 1 #add one to time variable every time we go through the loop

  if time%int(2/initspeed) == 0: #add particles every increment of this condition. If initial speed is higher, more frequent new particles to simulate constant density
    for i in range(numberofparticlesnew):
      p.append(particle(0, random.randint(0,By-1)+random.random(), initspeed, 0)) #create a new particle with initial x velocity and initial random vertical postition.
      particleCount += 1

#LOOPING PARTICLES-------------------------------------------------------------------------
for i in range(particleCount):

  #boarder collision
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

  #REPULSIVE FORCE FROM OTHER PARTICLES
  for j in range(particleCount):
    if i != j:
      distance = ((p[i].x - p[j].x)**2 + (p[i].y - p[j].y)**2)**0.5 #distance varaible stores numerical value of distance between two particles
      if distance < replusiveDistance:
          #find the angle
                if ob[j].x - p[i].x != 0:
                        angle = math.atan((ob[j].y - p[i].y)/(ob[j].x - p[i].x))
                else:
                    angle = 90
        
  

