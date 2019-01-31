from time import sleep
#import math
#import RPi.GPIO as GPIO
#import control
from PID import PID
from MotorSystem import MotorSystem
import matplotlib
import matplotlib.pyplot as plt

"""
#Simulation and Plotting Step Response
system = control.tf([1],[1, 2, 1])
pid = control.tf([0.1586, 0.4556, 0.4377], [1, 0])

time, yout = control.step_response(control.feedback(pid*system, 1, sign=-1), T=None, X0=0.0, input=None, output=None, transpose=False, return_x=False)
plt.plot(time, yout)
plt.xlabel("time")
plt.ylabel("output")
plt.title("Step Response")
plt.grid(True)
plt.savefig("test.png")
plt.show()
"""

sampling = 0.01
mypid = PID(2, 0.08, 0.12, 0, 0, -500, 500)
Gs = MotorSystem(0, 0, 0, 0, -80, 80)
outarray = []
timearray = []
controlarray = []
for i in range(0,80):
    controlarray.append(mypid.controller(1, Gs.yk))
    outarray.append(Gs.out(mypid.output))
    timearray.append(i*sampling)
    print("******************************")
    #print("Control Signal: ", controlarray[i])
    #print("Integrator: ", mypid.integrator)
    #print("******************************")
    print("System output: ", outarray[i])
    sleep(sampling)


plt.plot(timearray,outarray)
plt.xlabel("Time[s]")
plt.ylabel("Output")
plt.title("Discrete Time Motor System Step Output")
plt.grid(True)
plt.savefig("realtest.png")
plt.show()

