class MotorSystem:
    def __init__(self, ykd, ykdd, xkd, xkdd, satMin, satMax):
        self.ykd = ykd
        self.ykdd = ykdd
        self.xkd = xkd
        self.xkdd = xkdd
        self.yk = 0
        self.satMin = satMin
        self.satMax = satMax

    def out(self, xkd):
        self.yk = 0.9454*self.ykd - 0*self.ykdd + 0.05113*xkd + 0*self.xkdd
        if(self.yk < self.satMin):
            self.yk = self.satMin
        elif(self.yk > self.satMax):
            self.yk = self.satMax
        self.ykdd = self.ykd
        self.ykd = self.yk
        self.xkdd = xkd
        return self.yk
