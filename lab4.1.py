from math import sqrt, cos
from scipy import integrate

def f(x):
    return cos(x)

def weight(x):
    return 1/sqrt(x)

def func(x):
    return f(x)*weight(x)

def F(a, b):
    return integrate.quad(lambda x: f(x)*weight(x), a, b)[0]


def interpol_coeffs(nodes, a, b):
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

    # for fixed nodes 1/4 and 3/4
    # A1 = lambda x: 1/6 * sqrt(x)*(4*x - 9) / (1/4 - 3/4)
    # A2 = lambda x: 1/6 * sqrt(x)*(4*x - 3) / (3/4 - 1/4)
    # return [A1(b) - A1(a), A2(b) - A2(a)]

    print ('A1 ', res[0])
    print ('A2 ', res[1])
    return res


def mid_rectangles(f, a, b):
    h = (b-a)/2
    return h*(f(a + h/2) + f(a + h/2 + h))
 

def interpol(table, a, b):
    nodes, Y = zip(*table)
    A = interpol_coeffs(nodes, a, b)
    S = 0
    for k, _ in enumerate(nodes):
        S += Y[k]*A[k]
    return S

def gauss(f, a, b):
    x1, x2 = [-1/sqrt(3), 1/sqrt(3)]
    S = lambda x: (a+b)/2 + (b-a)/2*x
    return (b-a)/2*(f(S(x1))+f(S(x2)))

def nast_coeffs(weight, a, b):
    def m (k):
        # for fixed weight 1/sqrt(x)
        ff = lambda x: x**(k+0.5)/(k+0.5)
        return ff(b) - ff(a)
        # return integrate.quad(lambda x:weight(x) * x**k,a,b)[0]
    
    a2=(m(2)*m(2)-m(3)*m(1))/(m(1)*m(1)-m(2)*m(0))
    a1=(-m(2)-a2*m(0))/m(1)

    D = a1*a1-4*a2
    x1=(-a1+sqrt(D))/2
    x2=(-a1-sqrt(D))/2

    A1=(m(1)-x2*m(0))/(x1-x2)
    A2=(m(1)-x1*m(0))/(x2-x1)  
    return (A1, x1), (A2, x2)

def nast(f, weight, a, b):
    (A1, x1), (A2, x2) = nast_coeffs(weight, a, b)

    return f(x1)*A1+f(x2)*A2

print ('Приближенное вычисление интегралов')
print('Вариант 2 J = ∫cos(x)/√x dx')

print("Ввод пределов интегрирования")
a =  float(input ('a = ')) # 0
b =  float(input ('b = ')) # 1
print('(только для интерполяционной формулы)')
nodes = map(float, input('узлы через пробел: ').split(' ')) # [0.25, 0.75]
table = list(map(lambda node: (node, f(node)), nodes))

for (x,y) in table:
    print('f(%f)=%f' % (x, y))
J = F(a,b)
J1 = mid_rectangles(func, a, b)
J2 = interpol(table, a, b)
J3 = gauss(func, a, b)
J4 = nast(f, weight, a, b)
print('"Точно"  J=%f' % J)
print('Формула средних прямоугольников J=%f, фактическая погрешность %f' % (J1, abs(J1-J)))
print('Интерполяционная формула J=%f, фактическая погрешность %f' % (J2, abs(J2-J)))
print('Формула Гаусса J=%f, фактическая погрешность %f' % (J3, abs(J3-J)))
print('Формула Н.А.C.Т. J=%f, фактическая погрешность %f' % (J4, abs(J4-J)))
