import numpy
import math

    # Function
    #Inputs:
    #Returns:
    #Description:

def distanceCalc(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    distance = math.sqrt(pow(dx, 2) + pow(dy, 2))
    return(distance)

    # Function
    #Inputs:
    #Returns:
    #Description:

def gravityCalc(mass1, mass2, distance):
    G = 6.67 * math.pow(10,-11)
    F = (G * mass1 * mass2) / (distance * distance)
    print("Force, as calculated: " + str(F))
    return(F)

    # Function
    #Inputs:
    #Returns:
    #Description:

def dirVectCalc(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    magnitude = math.sqrt(pow(dx, 2) + pow(dy, 2))

    dirVector = [dx/magnitude,dy/magnitude]

    print("Calculated Directional Vector: " + str(dirVector))

    return(dirVector)

    # Function
    #Inputs:
    #Returns:
    #Description:

def vectorBreakdown(magnitude, dirVector):
    dx = magnitude * dirVector[0]
    dy = magnitude * dirVector[1]
    return([dx,dy])
