class HIBVP:
    def __init__(self):
        self.T = 0.0

    def a(self, x, t):
        return 1.0

    def F(self, x, t):
        return 2.0

    def g(self, t):
        return t

    def f(self, x):
        return x

class HFDM:

    def __init__(self):
        self.h = 0
        self.k = 0
        self.J = 0
        self.N = 0
        self.T = 0
        self.t = 0
        self.XArr = None
        self.VOld = None
        self.VNew = None
        self.m_h = None

    def HFDM(self, NX, NT, myIBVP):
        self.J = NX
        self.N = NT
        self.m_h =  myIBVP

        self.T = self.m_h.T
        self.t = 0.0
        self.h = 1.0 / self.J
        self.k = self.T / self.N

        self.XArr = [x * self.h for x in range(NX+1)]
        self.VOld = [self.m_h.f(self.XArr[x]) for x in range(NX+1)]
        self.VNew = self.VOld

    def result(self):
        self.t += self.k
        self.VNew[0] = self.m_h.g(self.t)
        tmp = 0
        for j in range(len(self.VNew)):
            tmp = self.k * self.m_h.a(self.XArr[j], self.t) / self.h
            self.VNew[j] = (self.VOld[j] + (tmp * self.VNew[j-1])
                            + (self.k * self.m_h.F(self.t,j))) / (1 + tmp)
        self.VOld = self.VNew
        return self.VNew

    def isDone(self):
        return self.t >= self.T

def test():
    b = HIBVP()
    b.T = 1
    aa = HFDM()
    aa.HFDM(10, 5, b)
    while not aa.isDone():
        print(aa.result())
        print(aa.t)
