from math import sqrt, cos, gamma
from scipy import integrate
from functools import lru_cache

def f(x):
    return cos(x)

def weight(x):
    return 1/sqrt(x)

def func(x):
    return f(x)*weight(x)

def F(a, b):
    return integrate.quad(lambda x: f(x)*weight(x), a, b)[0]


def coeffs(nodes, a, b):
    n = len(nodes)
    res = []

    for k in range(n):
        def A(x):
            p = 1
            for i in range(n):
                if i == k:
                    continue
                p *= (x - nodes[i])/(nodes[k] - nodes[i])
            return p * weight(x)
        res.append(integrate.quad(A, a, b)[0])
    return res


def mid_rectangles(f, a, b):
    return (b-a)*f(((a+b)/2))
 

def interpol(table, a, b):
    nodes, Y = zip(*table)
    A = coeffs(nodes, a, b)
    S = 0
    for k, _ in enumerate(nodes):
        S += Y[k]*A[k]
    return S

def gauss(f, a, b):
    x1, x2 = [-1/sqrt(3), 1/sqrt(3)]
    S = lambda x: (a+b)/2 + (b-a)/2*x
    return (b-a)/2*(f(S(x1))+f(S(x2)))

def nast(f, weight, a, b):
    def m (k):
        return integrate.quad(lambda x:weight(x) * x**k,a,b)[0]
    a2=(m(2)*m(2)-m(3)*m(1))/(m(1)*m(1)-m(2)*m(0))
    a1=(-m(2)-a2*m(0))/m(1)

    D = a1*a1-4*a2
    x1=(-a1+sqrt(D))/2
    x2=(-a1-sqrt(D))/2

    A1=(m(1)-x2*m(0))/(x1-x2)
    A2=(m(1)-x1*m(0))/(x2-x1)

    return f(x1)*A1+f(x2)*A2

print ('Приближенное вычисление интегралов')
print('Вариант 2 ∫cos(x)/√x dx')

a = 0 # float(input ('a = ')) # 0
b = 1 # float(input ('b = ')) # 1
nodes = [0.25, 0.75] # map(float, input('узлы через пробел').split(' ')) # [0.25, 0.75]
table = list(map(lambda node: (node, f(node)), nodes))

for (x,y) in table:
    print('f(%f)=%f' % (x, y))
J = F(a,b)
J1 = mid_rectangles(func, a, b)
J2 = interpol(table, a, b)
J3 = gauss(func, a, b)
J4 = nast(f, weight, a, b)
print('Формула средних прямоугольников %f, r=%f' % (J1, abs(J1-J)))
print('Интерполяционная формула %f, r=%f' % (J2, abs(J2-J)))
print('Формула Гаусса %f, r=%f' % (J3, abs(J3-J)))
print('Формула Н.А.C.Т. %f, r=%f' % (J4, abs(J4-J)))
