import math
import sympy
from formatPoint import XYZ

def degToRad(deg):
    return deg * math.pi / 180.0 

def distanceBetweenTwoPoints(p1, p2):
    distance = pow((p2.x-p1.x)**2+(p2.y-p1.y)**2+(p2.z-p1.z)**2, 1/2)
    return distance

def arithmeticMean(values):
    tot = 0
    for value in values:
        tot += value
    return tot/len(values)

def quadraticMean(values):
    tot = 0
    for value in values:
        tot += pow(value, 2)
    mean = -pow(tot/len(values), 1/2)
    return mean

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def convertIntoGhz(value):
    frequency = value*10**-6
    return truncate(frequency, 3)

def localize(p1, r1, p2, r2, p3, r3):
    sympy.init_printing()
    x,y,z = sympy.symbols('x,y,z')
    sphere1 = sympy.Eq((x-p1.x)**2+(y-p1.y)**2+(z-p1.z)**2,r1**2)
    sphere2 = sympy.Eq((x-p2.x)**2+(y-p2.y)**2+(z-p2.z)**2,r2**2)
    sphere3 = sympy.Eq((x-p3.x)**2+(y-p3.y)**2+(z-p3.z)**2,r3**2)
    results = sympy.solve([sphere1,sphere2,sphere3],(x,y,z))

    coordinates = []
    if len(results) is not 0:
        for result in results:
            apprValue = []
            for i in range(3):
                if result[i].is_real:
                    apprCoord = result[i].evalf()
                    apprValue.append(truncate(apprCoord,3))
                else:
                    return
            coordinates.append(XYZ(apprValue[0], apprValue[1], apprValue[2]))
    else:
        return

    allX = []
    allY = []
    allZ = []
    for coordinate in coordinates:
        allX.append(coordinate.x)
        allY.append(coordinate.y)
        allZ.append(coordinate.z)
    meanPoint = XYZ(arithmeticMean(allX), arithmeticMean(allY), arithmeticMean(allZ))

    allDistanceFromMeanPoint = []
    for coordinate in coordinates:
        allDistanceFromMeanPoint.append(distanceBetweenTwoPoints(meanPoint, coordinate))
    radius = truncate(max(allDistanceFromMeanPoint),3)
   
    res = {
        'radius': radius,
        'meanPoint': meanPoint,
        'points': coordinates
    }
    return res
