from scipy import integrate
from sympy import Symbol, cos, sin, log, sqrt, Interval,pi
from sympy.functions import Abs
from scipy.optimize import minimize_scalar
from sympy.utilities.lambdify import lambdify

x = Symbol('x', real=True)

#### input function
function_expression = x**2*cos(x)
####

f = lambdify(x, function_expression)

def weight(t):
    return 1

def max_Df(n, a, b):
    deriv = function_expression.diff((x, n))
    l = lambdify(x, deriv)
    res = minimize_scalar(lambda x: -abs(l(x)), bounds=(a,b), method='bounded')
    return abs(l(res.x))

print ("Приближённое вычисление интеграла по квадратурным формулам")
print ("Вариант 2 J = ∫(%s)dx" % str(function_expression))

print("Ввод пределов интегрирования")
a =  float(input ('a = ')) # 0
b =  float(input ('b = ')) # 1


J, _ = integrate.quad(f, a, b)

print('Точное значение J=%f' % J)

m = int(input("Число промежутков m = "))

def left_rect(a, b, m):
    h = (b-a)/m
    return [a + (k-1)*h for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
left_rect.title = 'КФ левого прямоугольника'
left_rect.d = 0
left_rect.C = 1/2

def right_rect(a, b, m):
    h = (b-a)/m
    return [a + h + (k-1)*h for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
right_rect.title = 'КФ правого прямоугольника'
right_rect.d = 0
right_rect.C = 1/2

def middle_rect(a, b, m):
    h = (b-a)/m
    return [a + h/2 + (k-1)*h for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
middle_rect.title = 'КФ среднего прямоугольника'
middle_rect.d = 1
middle_rect.C = 1/24

def trapezoid(a, b, m):
    h = (b-a)/m
    return [a + k*h for k in range(0, m + 1)], [1/2, *[1 for k in range(1, m)], 1/2]
trapezoid.title = 'КФ трапеции'
trapezoid.d = 1
trapezoid.C = 1/12

def simpson(a, b, m):
    h = (b-a)/(2*m)
    return [a + k*h for k in range(0, 2*m + 1)], [1/6, *[(2/3 if i % 2 == 1 else 1/3) for i in range(1, 2*m)], 1/6]
simpson.title = 'КФ Симпсона'
simpson.d = 3
simpson.C = 1/2880


def calculate(f, method, a, b, m):
    nodes, weights = method(a, b, m)
    S = 0
    for node, weight in zip(nodes, weights):
        S += (b-a)/m*f(node)*weight 
    return S

def residue(d, C, a, b, m):
    return  C*(b-a)*(((b-a)/m)**(d+1)) *  max_Df(d+1, a, b)


for method in [left_rect, right_rect, middle_rect, trapezoid, simpson]:
    J1 =  calculate(f, method, a, b, m)
    print("%s: J = %f,\n\tфактическая погрешность:\t%.20f\n\tотносительная погрешность:\t%.20f\n\tтеоретическая погрешность<=\t%.20f" % (method.title, J1, abs(J-J1), abs(abs(J-J1)/J), \
        residue(method.d, method.C, a, b, m)))