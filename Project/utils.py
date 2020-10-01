import numpy
import math

DEBUG = False

    #distanceCalc Function
    #Inputs: Two positions in space
    #Returns: A scalar distance value
    #Description: Calculates the distance between two points.

def distanceCalc(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    distance = math.sqrt(pow(dx, 2) + pow(dy, 2))
    return(distance)

    #gravityCalc Function
    #Inputs: Two masses and the distance between them
    #Returns: A scalar force value
    #Description: Calculates the gravitational force felt by the first object due to the second.

def gravityCalc(mass1, mass2, distance):
    G = 6.67 * math.pow(10,-11)
    if distance == 0:
        distance = 1
    F = (G * mass1 * mass2) / (distance * distance)
    if DEBUG:
        print("Force, as calculated: " + str(F))
    return(F)

    #dirVectCalc Function
    #Inputs: two positions in space
    #Returns: A unit vector
    #Description: Calculates the directional unit vector from position 1 to position 2

def dirVectCalc(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    magnitude = math.sqrt(pow(dx, 2) + pow(dy, 2))

    dirVector = [dx/magnitude,dy/magnitude]

    if DEBUG:
        print("Calculated Directional Vector: " + str(dirVector))

    return(dirVector)

    #vectorBreakdown Function
    #Inputs: A magnitude and a directional unit vector
    #Returns: A vector
    #Description: Calculates a new vector given a magnitude and direction

def vectorBreakdown(magnitude, dirVector):
    dx = magnitude * dirVector[0]
    dy = magnitude * dirVector[1]
    return([dx,dy])

def getPointFromAngle(distance,angle,centerpoint):
    dx = math.cos(angle) * distance
    dy = math.sin(angle) * distance
    return([centerpoint[0] + dx, centerpoint[1] + dy])
