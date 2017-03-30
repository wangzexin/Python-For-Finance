class HIBVP:
    def __init__(self):
        self.T = 0.0

    def a(self, x, y, t):
        return 1.0

    def F(self, x, y, t):
        return 2.0

    def g(self, x, y, t):
        return t

    def f(self, x, y):
        return x * y

class HFDM:

    def __init__(self):
        self.h1 = 0
        self.h2 = 0
        self.k = 0
        self.J1 = 0
        self.J2 = 0
        self.N = 0
        self.T = 0
        self.t = 0
        self.XArr = None
        self.YArr = None
        self.MOld = None
        self.MNew = None
        self.m_h = None

    def HFDM(self, NX, NY, NT, myIBVP):
        self.J1 = NX
        self.J2 = NY
        self.N = NT
        self.m_h =  myIBVP

        self.T = self.m_h.T
        self.t = 0.0
        self.h1 = 1.0 / self.J1
        self.h2 = 1.0 / self.J2
        self.k = self.T / self.N

        self.XArr = [x * self.h1 for x in range(NX+1)]
        self.YArr = [x * self.h2 for x in range(NY+1)]
        self.MOld = [[0 for y in range(NY+1)] for x in range(NX+1)]
        for i in range(NY):
            self.MOld[0][i] = self.m_h.g(0, self.YArr[i], self.t)
        for i in range(NX):
            self.MOld[i][0] = self.m_h.g(self.XArr[i], 0, self.t)
        for i in range(1, NX+1):
            for j in range(1, NY+1):
                self.MOld[i][j] = self.m_h.f(self.XArr[i], self.YArr[j])
        self.MNew = self.MOld

    def result(self):
        self.t += self.k
        tmp = 0
        for i in range(1, self.J2+1):
            for j in range(1, self.J1+1):
                tmp1 = self.m_h.a(self.XArr[j], self.YArr[i], self.t) * self.k / self.h1
                tmp2 = self.m_h.a(self.XArr[j], self.YArr[i], self.t) * self.k / self.h2
                factor = 1 + tmp1 + tmp2 + self.k * self.m_h.a(self.XArr[j], self.YArr[i], self.t + self.k)
                self.MNew[j][i] = self.MOld[j][i] + tmp1 * self.MNew[j-1][i] + tmp2 * self.MNew[j][i-1]\
                                  + (self.k * self.m_h.F(self.XArr[j], self.YArr[i], self.t))
                self.MNew[j][i] = self.MNew[j][i] / factor
        self.MOld = self.MNew
        return self.MNew

    def isDone(self):
        return self.t >= self.T

def test():
    b = HIBVP()
    b.T = 1
    aa = HFDM()
    aa.HFDM(5, 5, 5, b)
    while not aa.isDone():
        print(aa.result())
        print(aa.t)
