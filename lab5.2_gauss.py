from math import sqrt, cos,sin,factorial, pi
from scipy import integrate
from scipy import linalg
from scipy.optimize import root_scalar
from functools import lru_cache
from sympy import Symbol,Interval, lambdify, expand, simplify,diff, integrate as symIntegrate
import numpy as np
from sympy import Poly, roots, degree


IS_DEBUG = True

def separate(f, a, b, n):
    res = []
    h = (b - a) / n
    x1 = a
    x2 = x1 + h
    y1 = f(x1)

    while x2 <= b:
        y2 = f(x2)
        if y1 * y2 <= 0:
            res.append( (x1, x2) )
        (x1, x2) = (x2, x1 + h)
        y1 = y2
    return res

def secant(f, a, b, e):
    x = b
    x_prev = a
    steps = 0
    while abs(x - x_prev) >= e:
        steps += 1
        tmp = x
        x = x - (x - x_prev) * f(x) / (f(x) - f(x_prev)) 
        x_prev = tmp
    return x

@lru_cache
def P(n):
  if n == 0:
    return lambda x: 1
  if n == 1:
    return lambda x: x
  return lambda x: (2 * n - 1) / n * P(n - 1)(x) * x \
    - (n - 1) / n * P(n - 2)(x)


def get_nodes(n):
  polynomial = P(n)
  intervals = separate(polynomial, -1, 1, n * 2)
  roots = map(lambda interval: secant(polynomial, interval[0], interval[1], 1e-12), intervals)
  return list(roots)

def get_coefficients(nodes):
  count = len(nodes)
  coefficients = map(lambda x: 2 * (1 - x ** 2) / (count ** 2 * P(count - 1)(x) ** 2), nodes)
  return list(coefficients)

print("Вычисление интегралов при помощи КФ Гаусса")
print("Вариант 2 f(x) = 1/√︀(1+x^2)(4+3x^2)")
input_f = input("Введите другую функцию f или нажмите enter: ")
if input_f:
    f = eval("lambda x: " + input_f)
else: 
    f = lambda x: 1/(sqrt((1+x**2)*(4+3*x**2)))

a = float(input("a = "))
b = float(input("b = "))
n = int(input("n = "))

nodes = get_nodes(n)
print("---------------------")
print("Узлы и к. КФ Гаусса")

coeffs = get_coefficients(nodes)
for node, A in zip(nodes, coeffs):
    print(node, "↔", A)

S = 0
print("---------------------")
print("Узлы и к. КФ подобной КФ Гаусса")
for node, A in zip(nodes, coeffs):
    node1 = (b-a)/2*node + (b+a)/2
    print(node1, "↔", A)
    S+=A*f(node1)
S *= (b-a)/2
J_exact = integrate.quad(f, a, b)[0]
print("---------------------")
print("J=%.12f точно=%0.12f погрешность=%.12f" % ( S, J_exact, abs(J_exact-S)))


