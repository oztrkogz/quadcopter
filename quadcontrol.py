import os.path
import time
import math
from PID import PID
from MotorSystem import MotorSystem
import matplotlib
import matplotlib.pyplot as plt

#Time
times = 0
sampling = 0.01

#Mass
mass = 0.65

#Gravity
gravity = 9.81

#Aerodynamic force and moment constants
KF = 3.13*(10**(-5))
KM = 7.5*(10**(-7))

#Saturation Constants
RPM_MAX = 9000
OHMEGA_MAX = 0.9*RPM_MAX*0.10466  #rad/sec
OHMEGA_HOVER = math.sqrt((mass*gravity)/(4*KF))
U1_MAX = 0.722 #KF*4*(OHMEGA_MAX**2) - 2*mass*gravity
U1_MIN = -0.722
U2_MAX = 0.5
U4_MAX = KM*2*(OHMEGA_HOVER**2)
PHITHETA_MAX = 0.4 #radians

#Inertia
Ixx = 7.5*(10**(-3))
Iyy = 7.5*(10**(-3))
Izz = 1.3*(10**(-2))

#Rotor Inertia
Jr = 6*(10**(-5))

#Axel Length
l = 0.23

#Inertia Variables
a1 = (Iyy - Izz)/Ixx
a2 = Jr/Ixx
a3 = (Izz - Ixx)/Iyy
a4 = Jr/Iyy
a5 = (Ixx - Iyy)/Izz
b1 = l/Ixx
b2 = l/Iyy
b3 = 1/Izz

#PID Parameters
X_KP = 45
X_KD = 5
X_KI = 0
Y_KP = 25
Y_KD = 45
Y_KI = 0
Z_KP = 0.25
Z_KD = 0.45
Z_KI = 0
PHI_KP = 8
PHI_KD = 46
PHI_KI = 0
THETA_KP = 8
THETA_KD = 46
THETA_KI = 0
PSI_KP = 0.25
PSI_KD = 9
PSI_KI = 0

#Initial Values
force_U1 = 1

#Angle and Position Dictionary Declerations
curangles = {}
refangles = {}
curposition = {}
refposition = {}
curcoordinates = {}
refcoordinates = {}

def readCurposition():
    file = open('curposition','r')
    curposstr = file.read().split(',')
    curposition["x"] = float(curposstr[0])
    curposition["y"] = float(curposstr[1])
    curposition["z"] = float(curposstr[2])
    file.close()
    return curposition

def readRefposition():
    file = open('refposition','r')
    refposstr = file.read().split(',')
    refposition["x"] = float(refposstr[0])
    refposition["y"] = float(refposstr[1])
    refposition["z"] = float(refposstr[2])
    file.close()
    return refposition

#Angles Dictionaries
curangles["phi"] = 0
curangles["theta"] = 0
curangles["psi"] =0
curangles["phid"] = 0
curangles["thetad"] = 0
curangles["psid"] = 0

#Position Dictionaries
curposition = readCurposition()
curposition["xd"] = 0
curposition["yd"] = 0
curposition["zd"] = 0
curposition["xdd"] = 0
curposition["ydd"] = 0
curposition["zdd"] = 0

#Graphic Arrays
outarray = []
timearray = []


#Creating PID Objects
xPID = PID(X_KP, X_KD, X_KI, 0, 0, -PHITHETA_MAX, PHITHETA_MAX)
yPID = PID(Y_KP, Y_KD, Y_KI, 0, 0, -PHITHETA_MAX, PHITHETA_MAX)
zPID = PID(Z_KP, Z_KD, Z_KI, 0, 0, U1_MIN, U1_MAX)
phiPID = PID(PHI_KP, PHI_KD, PHI_KI, 0, 0, -U2_MAX, U2_MAX)
thetaPID = PID(THETA_KP, THETA_KD, THETA_KI, 0, 0, -U2_MAX, U2_MAX)
psiPID = PID(PSI_KP, PSI_KD, PSI_KI, 0, 0, -U4_MAX, U4_MAX)

#Ohmegas Dictionaries
refohmegas = {}
curohmegas = {}

#Reference Ohmega Definition Method
def refOhmegas(U1, U2, U3, U4):
    refohmegas["OHM1"] = math.sqrt(U1/(4*KF) + U3/(2*KF) + U4/(4*KM))
    refohmegas["OHM2"] = math.sqrt(U1/(4*KF) - U2/(2*KF) - U4/(4*KM))
    refohmegas["OHM3"] = math.sqrt(U1/(4*KF) - U3/(2*KF) + U4/(4*KM))
    refohmegas["OHM4"] = math.sqrt(U1/(4*KF) + U2/(2*KF) - U4/(4*KM))
    return refohmegas


#Creating MotorSystem Objects
#motorSystem1 = MotorSystem(0, 0, 0, 0, -OHMEGA_MAX, OHMEGA_MAX)
#motorSystem2 = MotorSystem(0, 0, 0, 0, -OHMEGA_MAX, OHMEGA_MAX)
#motorSystem3 = MotorSystem(0, 0, 0, 0, -OHMEGA_MAX, OHMEGA_MAX)
#motorSystem4 = MotorSystem(0, 0, 0, 0, -OHMEGA_MAX, OHMEGA_MAX)

#Distance Calculation
refposition = readRefposition()
curposition = readCurposition()

refangles["psi"] = 0#math.atan2((refposition["x"]-curposition["x"]), (refposition["y"]-curposition["y"]))

print refangles["psi"]

zaccelduration = 1
zdistance = refposition["z"] - curposition["z"]
if zdistance < 0:
    zaccel = 1
    zconstspeed = 1
    zconstspeedduration = abs((zdistance + zaccel * zaccelduration**2) / zconstspeed)
elif zdistance > 0:
    zaccel = -1
    zconstspeed = -1
    zconstspeedduration = abs((zdistance + zaccel * zaccelduration**2) / zconstspeed)
else:
    zaccel = 0
    zconstspeed = 0
    zconstspeedduration = 0
refposition["z"] = curposition["z"]


xaccelduration = 1
xdistance = refposition["x"] - curposition["x"]
if xdistance < 0:
    xaccel = -1
    xconstspeed = -1
    xconstspeedduration = abs((xdistance - xaccel * xaccelduration**2) / xconstspeed)
elif xdistance > 0:
    xaccel = 1
    xconstspeed = 1
    xconstspeedduration = abs((xdistance - xaccel * xaccelduration**2) / xconstspeed)
else:
    xaccel = 0
    xconstspeed = 0
    xconstspeedduration = 0
refposition["x"] = curposition["x"]


yaccelduration = 1
ydistance = refposition["y"] - curposition["y"]
if ydistance < 0:
    yaccel = -1
    yconstspeed = -1
    yconstspeedduration = abs((ydistance - yaccel * yaccelduration**2) / yconstspeed)
elif ydistance > 0:
    yaccel = 1
    yconstspeed = 1
    yconstspeedduration = abs((ydistance - yaccel * yaccelduration**2) / yconstspeed)
else:
    yaccel = 0
    yconstspeed = 0
    yconstspeedduration = 0
refposition["y"] = curposition["y"]


#LOOOOOOOOOOOOOOOOOOOOOOOOOOP
while True:
    try:
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        print "Time: %f" %(times)
        curposition = readCurposition()
        print "Reference Position:\tx:%f\ty:%f\tz:%f" %(refposition["x"], refposition["y"], refposition["z"])
        print "Current Position:\tx:%f\ty:%f\tz:%f" %(curposition["x"], curposition["y"], curposition["z"])


        if (times < zaccelduration):
            refposition["zd"] = zaccel * times
        elif (times >= zaccelduration) and (times<zaccelduration+zconstspeedduration):
            refposition["zd"] = zconstspeed
        elif (times >= (zaccelduration+zconstspeedduration)) and times <= (zaccelduration*2 + zconstspeedduration):
            refposition["zd"] = zconstspeed - zaccel * (times - zaccelduration - zconstspeedduration)
        else:
            refposition["zd"] = 0
        refposition["z"] = refposition["z"] - refposition["zd"]*sampling

        if (times < xaccelduration):
            refposition["xd"] = xaccel * times
        elif (times >= xaccelduration) and (times<xaccelduration+xconstspeedduration):
            refposition["xd"] = xconstspeed
        elif (times >= (xaccelduration+xconstspeedduration)) and times <= (xaccelduration*2 + xconstspeedduration):
            refposition["xd"] = xconstspeed - xaccel * (times - (xaccelduration + xconstspeedduration))
        else:
            refposition["xd"] = 0
        refposition["x"] = refposition["x"] + refposition["xd"]*sampling

        if (times < yaccelduration):
            refposition["yd"] = yaccel * times
        elif (times >= yaccelduration) and (times<yaccelduration+yconstspeedduration):
            refposition["yd"] = yconstspeed
        elif (times >= (yaccelduration+yconstspeedduration)) and times <= (yaccelduration*2 + yconstspeedduration):
            refposition["yd"] = yconstspeed - yaccel * (times - (yaccelduration + yconstspeedduration))
        else:
            refposition["yd"] = 0
        refposition["y"] = refposition["y"] + refposition["yd"]*sampling

        print "---------------------------------------------"
        print "Reference Speed:\tX:%f\tY:%f\tZ:%f" %(refposition["xd"], refposition["yd"], refposition["zd"])
        print "Current Speed:\t\tX:%f\tY:%f\tZ:%f" %(curposition["xd"], curposition["yd"], curposition["zd"])


        #Position Controller
        refangles["phi"] = 0.3 #(mass/force_U1)*(-xPID.controller(refposition["x"], curposition["x"])*math.sin(curangles["psi"])+yPID.controller(refposition["y"], curposition["y"])*math.cos(curangles["psi"]))
        #if times>15:
        #    refangles["phi"] = 0.3
        #else:
        #    refangles["phi"] = 0
        refangles["theta"] = 0 #(mass/force_U1)*(-xPID.controller(refposition["x"], curposition["x"])*math.cos(curangles["psi"])-yPID.controller(refposition["y"], curposition["y"])*math.sin(curangles["psi"]))
        #if times>15:
        #    refangles["theta"] = 0.3
        #else:
        #    refangles["theta"] = 0
    
        print "---------------------------------------------"
        print "Reference Angles:\tPhi:%f\tTheta:%f\t\tPsi:%f" %(refangles["phi"], refangles["theta"], refangles["psi"])
        print "Current Angles:\t\tPhi:%f\tTheta:%f\t\tPsi:%f" %(curangles["phi"], curangles["theta"], curangles["psi"])
        print "---------------------------------------------"

        #Attitude and Heading Controllers
        U1 = zPID.controller(refposition["z"], curposition["z"]) + mass*gravity
        U2 = phiPID.controller(refangles["phi"], curangles["phi"])
        U3 = thetaPID.controller(refangles["theta"], curangles["theta"])
        U4 = psiPID.controller(refangles["psi"], curangles["psi"])
        print "U Values U1:%f, U2:%f, U3:%f, U4:%f" %(U1, U2, U3, U4)
        print "---------------------------------------------"
        #Determining Reference Ohmegas
        refohmegas = refOhmegas(U1, U2, U3, U4)
        print "Reference Ohmegas:\tOHM1:%f\tOHM2:%f\tOHM3:%f\tOHM4:%f" %(refohmegas["OHM1"], refohmegas["OHM2"], refohmegas["OHM3"], refohmegas["OHM4"])

        #Predicting Current Ohmegas
        curohmegas["OHM1"] = refohmegas["OHM1"] #motorSystem1.out(refohmegas["OHM1"])
        curohmegas["OHM2"] = refohmegas["OHM2"] #motorSystem2.out(refohmegas["OHM2"])
        curohmegas["OHM3"] = refohmegas["OHM3"] #motorSystem3.out(refohmegas["OHM3"])
        curohmegas["OHM4"] = refohmegas["OHM4"] #motorSystem4.out(refohmegas["OHM4"])
        print "Current Ohmegas:\tOHM1:%f\tOHM2:%f\tOHM3:%f\tOHM4:%f" %(curohmegas["OHM1"], curohmegas["OHM2"], curohmegas["OHM3"], curohmegas["OHM4"])
        print "---------------------------------------------"
        #Determining U Forces
        force_U1 = KF*(((curohmegas["OHM1"])**2)+((curohmegas["OHM2"])**2)+((curohmegas["OHM3"])**2)+((curohmegas["OHM4"])**2))
        force_U2 = KF*(-((curohmegas["OHM2"])**2)+((curohmegas["OHM4"])**2))
        force_U3 = KF*(((curohmegas["OHM1"])**2)-((curohmegas["OHM3"])**2))
        force_U4 = KM*(((curohmegas["OHM1"])**2)-((curohmegas["OHM2"])**2)+((curohmegas["OHM3"])**2)-((curohmegas["OHM4"])**2))
        force_Urel = -(curohmegas["OHM1"])+(curohmegas["OHM2"])-(curohmegas["OHM3"])+(curohmegas["OHM4"])
        print "U Forces:\tU1:%f\tU2:%f\tU3:%f\tU4:%f\tUrel:%f" %(force_U1, force_U2, force_U3, force_U4, force_Urel)
        print "---------------------------------------------"
        #Quadrotor Dynamics
        curangles["phidd"] = b1*force_U2 - a2*(curangles["thetad"])*force_Urel + a1*(curangles["psid"])*(curangles["thetad"])
        curangles["thetadd"] = b2*force_U3 + a4*(curangles["phid"])*force_Urel + a3*(curangles["phid"])*(curangles["psid"])
        curangles["psidd"] = b3*force_U4 + a5*(curangles["phid"])*(curangles["thetad"])
    
        curangles["phid"] = curangles["phid"] + curangles["phidd"]*sampling
        curangles["thetad"] = curangles["thetad"] + curangles["thetadd"]*sampling
        curangles["psid"] = curangles["psid"] + curangles["psidd"]*sampling

        curangles["phi"] = curangles["phi"] + curangles["phid"]*sampling
        curangles["theta"] = curangles["theta"] + curangles["thetad"]*sampling
        curangles["psi"] = curangles["psi"] + curangles["psid"]*sampling

        curposition["xdd"] = -(force_U1/mass)*(math.sin(curangles["phi"])*math.sin(curangles["psi"])+math.cos(curangles["phi"])*math.cos(curangles["psi"])*math.sin(curangles["theta"]))
        curposition["ydd"] = -(force_U1/mass)*(math.cos(curangles["phi"])*math.sin(curangles["psi"])*math.sin(curangles["theta"])-math.cos(curangles["psi"])*math.sin(curangles["theta"]))
        curposition["zdd"] = gravity - (force_U1/mass)*(math.cos(curangles["phi"])*math.cos(curangles["theta"]))
        print "Accelerations:\tX:%f\tY:%f\tZ:%f" %(curposition["xdd"], curposition["ydd"], curposition["zdd"])

        curposition["xd"] = curposition["xd"] + curposition["xdd"]*sampling
        curposition["yd"] = curposition["yd"] + curposition["ydd"]*sampling
        curposition["zd"] = curposition["zd"] + curposition["zdd"]*sampling

        curposition["x"] = curposition["x"] + curposition["xd"]*sampling
        curposition["y"] = curposition["y"] + curposition["yd"]*sampling
        curposition["z"] = curposition["z"] - curposition["zd"]*sampling

        file = open('curposition', 'w')
        file.write(str(float("{0:.6f}".format(curposition["x"])))+","+str(float("{0:.6f}".format(curposition["y"])))+","+str(float("{0:.6f}".format(curposition["z"]))))
        file.close()
        times = times + sampling
        timearray.append(times)
        outarray.append(U1)
        time.sleep(sampling)
    except KeyboardInterrupt:
        plt.plot(timearray,outarray)
        plt.xlabel("Time[s]")
        plt.ylabel("Altitude Control Signal")
        plt.title("Altitude Position Trapezoid Integral Reference Control Signal")
        plt.grid(True)
        plt.savefig("realtest.png")
        plt.show()
        raise

