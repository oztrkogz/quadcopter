class PID:
    #PID Values Initialization
    def __init__(self, kp, kd, ki, initErrord, initIntegrator, satMin, satMax):
        self.integrator = initIntegrator
        self.errord = initErrord
        self.satMax = satMax
        self.satMin = satMin
        self.kp = kp
        self.kd = kd
        self.ki = ki

    def controller(self, reference, feedback):
        error = reference - feedback
        derivator = (error - self.errord)
        integrator = (error + self.integrator)
        self.errord = error
        #Integral WindUp Prevention
        if(integrator<self.satMin):
            self.integrator = self.satMin
        elif(integrator >= self.satMin and integrator <= self.satMax):
            self.integrator = integrator
        elif(integrator > self.satMax):
            self.integrator = self.satMax
        #Controller Output Saturation
        self.output = self.kp*error + self.kd*derivator + self.ki*integrator
        if(self.output < self.satMin):
            self.output = self.satMin
        elif(self.output > self.satMax):
            self.output = self.satMax
        return self.output
