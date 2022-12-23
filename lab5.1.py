from math import sqrt, cos,sin
from scipy import integrate
from scipy import linalg
from scipy.optimize import root_scalar
from functools import lru_cache
from sympy import Symbol,Interval, expand, simplify, integrate as symIntegrate
import numpy as np
        # t = Symbol('t', real=True)
        # expr = t**(0.25)
        # for i in range(len(roots)):
        #     if i == k:
        #         continue
        #     expr *= (t - roots[i])/(roots[k] - roots[i])

        # S = (symIntegrate(expr, (t, a, b)))
        # nodes.append(
        #     (S, roots[k])
        # )

        
IS_DEBUG = True

def debug(*args, **vargs):
    if IS_DEBUG:
        print(*args, **vargs)



def weight(x):
    return x ** (1/4)

def func(x):
    return f(x)*weight(x)

def F(a, b):
    return integrate.quad(lambda x: f(x)*weight(x), a, b)[0]

def nast_coeffs(weight, n, a, b):
    @lru_cache
    def m (k):
        # for fixed weight x ^ 0.25
        ff = lambda x: x**(k+5/4)/(k+5/4)
        return ff(b) - ff(a)
        S = integrate.quad(lambda x:weight(x) * x**k,a,b)[0]
        debug("μ(%d) = %.05f" % (k,S))
        return S

    for k in range(0, 2*n):
        m(k)

    matrix = np.array([
        [m(n - k + row) for k in range(1, n + 1)] for row in range(0, n )
    ])
    B = np.array([-m(k) for k in range(n, 2*n)])
    A = linalg.solve(matrix, B)

    coeffs = [1, *A]
    debug ("ортогональный многочлен %s" % " + ".join(("%fx^%d" % (coeff, n - i) for i, coeff in enumerate(coeffs))))

    roots = list(map(lambda x: x.real, filter(lambda x: x.imag == 0 and a <= x <= b, np.roots(coeffs))))
    nodes = []
    for k in range(len(roots)):
        def A(x):
            p = 1
            for i in range(len(roots)):
                if i == k:
                    continue
                p *= (x - roots[i])/(roots[k] - roots[i])
            return p * weight(x)

        nodes.append(
            (integrate.quad(A, a, b)[0], roots[k])
        )
    return nodes

def nast(f, weight, n, a, b):
    nodes = nast_coeffs(weight, n, a, b)
    debug("узлы ", list(zip(*nodes))[1])
    return sum([f(x) * A for (A, x) in nodes])

print ('Приближенное вычисление интегралов')
print('Вариант 2 f(x) = sin(x), ρ(x) = x**0.25')
f_input = input("Введите другую функцию f(x) или нажмите enter: ")
if f_input.strip():
    f = eval("lambda x: " + f_input)
else:
    f = lambda x: sin(x)

print("Ввод пределов интегрирования")
a =  float(input ('a = ')) # 0
b =  float(input ('b = ')) # 1
n =  int(input ('n = '))

J = F(a,b)

J1 = nast(f, weight, n, a, b)
print('"Точно"  J=%.12f' % J)

print('Формула Н.А.C.Т. J=%.12f, фактическая погрешность %.12f' % (J1, abs(J1-J)))
# x**2+x+9