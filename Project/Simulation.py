from graphics import *
import utils
import time
import math
import random

DEBUG = False

#--Useful Comment Formats--#

    # Function
    #Inputs:
    #Returns:
    #Description:

    ####-WIP FUNCTION-###

#-----------------------------
#NAME Class
#-----------------------------

#-----------------------------
#massBody Class
#-----------------------------

class massBody:
    def __init__(self, name, mass, startCoord, startVel, size, color):
        self.name = name
        self.mass = mass
        self.pos = [startCoord[0], startCoord[1]]
        self.vel = [startVel[0], startVel[1]]
        self.size = size
        self.color = color
        self.icon = Circle(Point(self.pos[0],self.pos[1]), self.size)
        self.icon.setFill(self.color)
        self.icon.setOutline(self.color)

    #calcForces Function
    #Inputs: A list of massed entities within the system
    #Returns: The total force vector on the object
    #Description: Takes a list of all objects in the system and calculates the sum of the gravitational force vectors between this object and all others.

    def calcForces(self, systemEntities):
        sumXForces = list()
        sumYForces = list()
        for entity in systemEntities:
            #print("There are entities!")
            if entity != self:
                #print("There are entities other than myself!")
                distance = utils.distanceCalc(self.pos,entity.pos)
                force = utils.gravityCalc(self.mass,entity.mass,distance)
                dirVector = utils.dirVectCalc(self.pos,entity.pos)
                forceVector = utils.vectorBreakdown(force,dirVector)
                sumXForces.append(forceVector[0])
                sumYForces.append(forceVector[1])


        sumX = 0
        sumY = 0
        for i in range(len(sumXForces)):
#            force = [force[0] + sumXForces[i],force[1] + sumYForces[i]]
            sumX = sumX + sumXForces[i]
            sumY = sumY + sumYForces[i]

        #print("x-component Force:" + str(sumX) + " y-component Force: " + str(sumY))
        return([sumX, sumY])

    #calcAccel Function
    #Inputs: A vector sum of all forces acting on this object
    #Returns: The acceleration vector this object experiences
    #Description: Calculates the acceleration vector of this object based on its mass and the external forces acting upon it.

    def calcAccel(self, sumForces):
        accelX = sumForces[0]/self.mass
        accelY = sumForces[1]/self.mass
        return([accelX, accelY])

    #updateVel Function
    #Inputs: An acceleration vector
    #Returns: Nothing
    #Description: Updates this objects' velocity vector based on an acceleration vector.

    def updateVel(self, acceleration):
        self.vel[0] = self.vel[0] + acceleration[0]
        self.vel[1] = self.vel[1] + acceleration[1]

    #updatePos Function
    #Inputs: Nothing
    #Returns: Nothing
    #Description: Updates this objects' position based on its velocity vector.

    def updatePos(self):
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]

    #findMostInfluentialBody Function
    #Inputs: A list of massBody entities in the system.
    #Returns: The body that exerts the most force on this body.
    #Description: Calculates the greatest magnitude of force on this body and then returns the associated body. Returns None if there are no bodies acting on this body.

    def findMostInfluentialBody(self, systemEntities):
        greatestForce = [0, None]
        for entity in systemEntities:
            if entity != self:
                distance = utils.distanceCalc(self.pos,entity.pos)
                force = utils.gravityCalc(self.mass,entity.mass,distance)
                if force > greatestForce[0]:
                    if DEBUG:
                        if greatestForce[1] != None:
                            print(entity.name + "'s force on this body is: " + str(force) + " Which is greater than " + greatestForce[1].name + "'s force of: " + str(greatestForce[0]))
                        else:
                            print("There is no greatest force yet.")
                    greatestForce[0] = force
                    greatestForce[1] = entity

        return(greatestForce[1])

    #calculateOrbitVel Function
    #Inputs: A body around which this body should orbit, and an orbit type.
    #Returns: An initial velocity required to orbit the specified body.
    #Description: Calculates and returns the initial velocity required to orbit the specified body.

    def calculateOrbitVel(self, orbitBody, orbitType):
        vel = [0,0]
        if orbitType == "none":
            return(vel)
        G = 6.67 * math.pow(10,-11)
        distance = utils.distanceCalc(self.pos,orbitBody.pos)
        forceDirVector = utils.dirVectCalc(self.pos,orbitBody.pos)
        velDirVector = [forceDirVector[1], forceDirVector[0] * -1]

        if orbitType == "circular":
            velMagnitude = math.sqrt((G * orbitBody.mass)/distance)
            vel = utils.vectorBreakdown(velMagnitude,velDirVector)

        return(vel)

    #simTick Function
    #Inputs: None
    #Returns: None
    #Description: A series of functions that occur every tick of the simulation.

    def simTick(self, simulation):
        if self.name != "Star":
            if DEBUG:
                print(self.name)
            forces = self.calcForces(simulation.simulationEntities)
            if DEBUG:
                print("Force vector: " + str(forces))
            acceleration = self.calcAccel(forces)
            if DEBUG:
                print("Acceleration vector: " + str(acceleration))
            self.updateVel(acceleration)
            if DEBUG:
                print("Velocity vector: " + str(self.vel))
            self.updatePos()

            if DEBUG:
                print("Position: " + str(self.pos))
            #simulation.window.moveBody(self)
#        self.calculateCollision()  -- Possible addition?

#-----------------------------
#simWindow Class
#-----------------------------

class simWindow:
    def __init__(self, xDim, yDim, color):
        self.xDim = xDim
        self.yDim = yDim
        self.color = color
        self.window = None

    # launchWindow Function
    #Inputs: Nothing
    #Returns: Nothing
    #Description: Launches the simulation window.

    def launchWindow(self):
        self.window = GraphWin("Simulation",self.xDim,self.yDim)
        self.window.setBackground(self.color)

    #drawBody Function
    #Inputs: A body to draw
    #Returns: Nothing
    #Description: Draws a body to the screen.

    def drawBody(self, body):
        body.icon.draw(self.window)

    #moveBody Function
    #Inputs: A body to move
    #Returns: Nothing
    #Description: Moves a pre-existing body on the screen by its velocity.

    def moveBody(self, body):
        body.icon.move(body.vel[0],body.vel[1])

    #eraseBody Function
    #Inputs: A body to erase
    #Returns: Nothing
    #Description: Erases a body from the screen.

    def eraseBody(self, body):
        body.icon.undraw()

#-----------------------------
#Simulation Class
#-----------------------------

class simulation:
    def __init__(self):
        self.tick = 0
        self.window = simWindow(1000,1000,"black")
        self.simulationEntities = list()
        self.vectorEntities = list()

    #addBody Function
    #Inputs: A Name, mass, starting position, starting velocity, size and color of a massBody object
    #Returns: Nothing
    #Description: Adds a massBody object to the simulation and draws it in its initial location.

    def addBody(self, name, mass, startPos, orbitType, size, color):
        newBody = massBody(name, mass,startPos,[0,0], size, color)
        self.simulationEntities.append(newBody)
        print("-----------**-----------")
        print("Finding orbital starting values for " + (newBody.name))
        orbitBody = newBody.findMostInfluentialBody(self.simulationEntities)
        if orbitBody != None:
            print(newBody.name + " is orbiting " + orbitBody.name)
            startingVel = newBody.calculateOrbitVel(orbitBody,orbitType)
            print("Starting velocity is: " + str(startingVel))
            newBody.vel = [startingVel[0] + orbitBody.vel[0], startingVel[1] + orbitBody.vel[1]]
            print("Summed Velocity is: " + str(newBody.vel))
        self.window.drawBody(newBody)


    #removeBody Function
    #Inputs: A massBody object to be removed
    #Returns: Nothing
    #Description: Removes a massBody from the simulation and erases it from the window.

    def removeBody(self,body):
        self.window.eraseBody(body)
        self.simulationEntities.remove(body)

    #simTick Function
    #Inputs: Nothing
    #Returns: Nothing
    #Description: A series of commands to run at every tick of the simulation.

    def simTick(self):
        self.tick = self.tick + 1
        for entity in self.simulationEntities:
            entity.simTick(self)
            if ((self.tick % 10 == 0) and (self.tick <= 100000)) or ((self.tick >= 100000) and (self.tick <= 10000000000) and (self.tick % 10000 == 0)) or (self.tick >= 10000000000) :
                entity.icon.undraw()
                entity.icon = Circle(Point(entity.pos[0],entity.pos[1]), entity.size)
                entity.icon.setFill(entity.color)
                entity.icon.setOutline(entity.color)
                entity.icon.draw(self.window.window)

        if self.tick % 1000 == 0:
            print(str(self.tick) + " Simulation Ticks have Ocurred")

    #scatterBodies Function
    #Inputs: A number of bodies to scatter, a style of scattering (), a range within which to scatter the bodies, a center of the range required for certain scattering types, a center of the system around which to scatter the bodies, a range of mass, size and color values to assign the scattered bodies, and an orbit type to calculate for each of the scattered bodies.
    #Returns: Nothing
    #Description: Creates a large collection of massBody objects, scatters them over an area, assigns a range of properties and gives initial orbital paths.

    def scatterBodies(self, numBodies, scatterType, spreadRange, rangeCenter, systemCenter, massRange, sizeRange, colorRange, orbitType, nameBase):

        if scatterType == "orbit":
            randomRange = list()
            for i in range(numBodies * random.randint(1,3)):
                randomRange.append(i)

            randomSample = random.sample(randomRange,numBodies)
            for i in range(numBodies):
                angle = randomSample[i] * ((2 * math.pi) / numBodies)
                distance = random.randint(spreadRange[0],spreadRange[1])
                newPoint = utils.getPointFromAngle(distance, angle, systemCenter)
                self.addBody((nameBase + str(i)), random.randint(massRange[0], massRange[1]), newPoint, orbitType, random.randint(sizeRange[0], sizeRange[1]), random.choice(colorRange))

    def drawVectorArrows(self):
        for entity in self.simulationEntities:
            p1 = Point(entity.pos[0], entity.pos[1])
            point2 = utils.getPointFromVector(entity.pos, entity.vel)
            p2 = Point(point2[0],point2[1])
            newLine = Line(p1,p2)
            newLine.setArrow("last")
            newLine.setFill("white")
            newLine.draw(self.window.window)
            self.vectorEntities.append(newLine)

    def eraseVectorArrows(self):
        for arrow in self.vectorEntities:
            arrow.undraw()

def main():

    simulating = True
    tickDelay = 0.0001
    #numBodies = 20
    #test = range(numBodies * random.randint(1,3))
    #for n in test:
    #    print(n)

    sim = simulation()

    sim.window.launchWindow()

    sim.addBody("Star", (1000000000000), [500,500], "none", 20, "yellow")
    sim.addBody("Planet", 7000000000, utils.getPointFromAngle(400,math.radians(315),[500,500]), "circular", 7, "green")
    #sim.addBody("Moon1", 150000, [500,925], "circular", 4, "white")
    #sim.addBody("Moon2", 100000, [500,935], "circular", 3, "green")
    #sim.addBody("Moon2", 9000, [500,941], [0.45,0], 1, "red")

    sim.scatterBodies(50, "orbit", [320,480], 400, [500,500], [100,500], [1,2], ["grey", "brown", "white", "red"], "circular", "Asteroid")

    #sim.drawVectorArrows()

    #time.sleep(10)

    #sim.eraseVectorArrows()

    while simulating:
        if DEBUG:
            print("-------------------------------------------------------")
        sim.simTick()
        #time.sleep(tickDelay)


    sim.window.window.getMouse()
    sim.window.window.close()



main()
