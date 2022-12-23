from math import sqrt, cos,sin,factorial, pi
from scipy import integrate
from scipy import linalg
from scipy.optimize import root_scalar
from functools import lru_cache
from sympy import Symbol,Interval, lambdify, expand, simplify,diff, integrate as symIntegrate
import numpy as np
from sympy import Poly, roots, degree


IS_DEBUG = True

def meller(f, n, a, b):
    S = 0
    if IS_DEBUG:
        print("MELLER n=%d" % n)
    for k in range(n):
        x1 = cos(pi * (2*k - 1)/(2*n))
        print("Узел ", x1, 'Коэф pi /', n )
        S+=f(x1)
    S *= pi/n
    return S

n1,n2,n3 = map(int, input("n1 n2 n3 через пробел: ").split())

f = lambda x: cos(x)
j = integrate.quad(lambda x: f(x) / sqrt(1-x**2), -1, 1)[0]
j1 = (meller(f, n1, -1, 1))
j2 = (meller(f, n2, -1, 1))
j3 = (meller(f, n3, -1, 1))
print("точно=%.12f\nпри n=%d: %.12f погр. %.12f\nпри n=%d: %.12f погр. %.12f\nпри n=%d: %.12f погр. %.12f" % (
     j,
     n1, j1, abs(j-j1), n2, j2, abs(j-j2), n3, j3, abs(j-j3)))


# todo use real integral