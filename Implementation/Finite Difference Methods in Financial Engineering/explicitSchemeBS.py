L = 1
M = 1
T = 1

def IC(x, y):
    if x > y:
        return x
    return 0

def BC(x, y, t):
    return 1



# Creating a mesh
NX = 10
NY = 10
NT = 40
hx = L / NX
hy = L / NY
k = T / NT

a = hx * hx
b = hy * hy
lambda1 = k / a
lambda2 = k / b
factor = 1 - 2 * (lambda1 + lambda2)

class ExplicitScheme:

    def __init__(self, NX, NY, I, J, T, k, f):
        self.NX = NX
        self.NY = NY
        self.I = I
        self.J = J
        self.hx = I / NX
        self.hy = J / NY
        self.T = T
        self.k = k
        self.t = T / k
        self.f = f
        self.lambda1 = self.k / self.hx ** 2
        self.lambda2 = self.k / self.hy ** 2
        self.factor = 1 - 2 * self.lambda1 - 2 * self.lambda2
        self.XArr = [x * self.hx for x in range(NX+1)]
        self.YArr = [x * self.hy for x in range(NY+1)]
        self.U = [[0 for x in range(NY+1)] for y in range(NX+1)]

        # initial conditions
        for i in range(1, NX+1):
            for j in range(1, NY+1):
                self.U[i][j] = f(self.XArr[i], self.YArr[j])
        print(self.U)

        for i in range(0, NX+1):
            self.U[i][0] = 0
            self.U[NX][0] = 0
        
        for i in range(0, NY+1):
            self.U[0][i] = 0
            self.U[0][NY] = 0
        
        # Check constraints
        if 1 < 2 * (self.lambda1 + self.lambda2):
            print("ERROR!")
        if k > 1 / (2 * (self.hx ** (-2) + self.hy ** (-2))):
            print("ERROR!")

    def produce(self):
        U = self.U
        self.t += self.k
        for j in range(1, self.NY):
            for i in range(1, self.NX):
                self.U[i][j] = self.lambda1 * (self.U[i+1][j] + self.U[i-1][j]) + self.lambda2 * (self.U[i][j+1] + self.U[i][j-1]) - self.factor * self.U[i][j]
        print(U)
        self.U = U

    def isDone(self):
        return self.t >= self.T

def test():
    def f(x,y):
        return max(x - 5, 0)
    s = ExplicitScheme(10, 10, 10, 1, 1, 10, f)
    while not s.isDone():
        s.produce()
