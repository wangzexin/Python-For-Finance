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

