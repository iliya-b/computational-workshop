from scipy import integrate
from sympy import Symbol, cos, sin, log, sqrt, Interval,pi
from sympy.functions import Abs
from scipy.optimize import minimize_scalar
from sympy.utilities.lambdify import lambdify

IS_LAB4 = True

x = Symbol('x', real=True)

#### input function
input_function =  sin(x)*2*x**5 # 1.27 * x**5 + 2.04 * x
input_weight = 1
####

function_expression = x-x + input_function # a workaround to allow pure constants as a functions
weight_expression = x-x + input_weight
weight= lambdify(x, weight_expression) 
func = lambdify(x, function_expression)
f = lambda x: weight(x) * func(x)

def maxima(func, a, b):
    res = minimize_scalar(lambda x: -abs(func(x)), bounds=(a,b), method='bounded')
    return abs(func(res.x))

def Df(n):
    deriv = function_expression.diff((x, n))
    return lambdify(x, deriv)

print ("Приближённое вычисление интеграла по квадратурным формулам")
print ("Вариант 2 J = ∫(%s)dx" % str(function_expression))

print("Ввод пределов интегрирования")
a =  float(input ('a = ')) # 0
b =  float(input ('b = ')) # 1

J, _ = integrate.quad(f, a, b)

print('Точное значение J=%.20f' % J)

m = int(input("Число промежутков m = "))
print("h=%f", (b-a) / m)
if IS_LAB4:
    l = int(input("l = "))
else:
    l = 1

def left_rect(a, b, m):
    h = (b-a)/m
    return [a + (k-1)*h for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
left_rect.title = 'КФ левых прямоугольника'
left_rect.d = 0
left_rect.C = 1/2

def right_rect(a, b, m):
    h = (b-a)/m
    return [a + h + (k-1)*h for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
right_rect.title = 'КФ правых прямоугольников'
right_rect.d = 0
right_rect.C = 1/2

def middle_rect(a, b, m):
    h = (b-a)/m
    return [a - h/2 + h*k for k in range(1, m + 1)], [1 for k in range(1, m + 1)]
middle_rect.title = 'КФ средних прямоугольников'
middle_rect.d = 1
middle_rect.C = 1/24

def trapezoid(a, b, m):
    h = (b-a)/m
    return [a + k*h for k in range(0, m + 1)], [1/2, *[1 for k in range(1, m)], 1/2]
trapezoid.title = 'КФ трапеций'
trapezoid.d = 1
trapezoid.C = 1/12

def simpson(a, b, m):
    h = (b-a)/(2*m)
    S = 1/6 * f(a) + 1/6*f(b) + 2/3 * sum([f(a + k*h) for k in range(1, 2*m, 2)]) + 1/3 * sum([f(a + k*h) for k in range(2, 2*m-1, 2)])
    return S * (b-a)/m, None
simpson.title = 'КФ Симпсона'
simpson.d = 3
simpson.C = 1/2880


def calculate(f, method, a, b, m):
    nodes, weights = method(a, b, m)
    if weights is None: # if the method makes last computations on its own (simpson)
        return nodes
    S = 0
    for node, weight in zip(nodes, weights):
        S += f(node)*weight 
    return (b-a)/m*S

def residue(d, C, a, b, m):
    return  C*(b-a)*(((b-a)/(m))**(d+1)) *  maxima(Df(d+1), a, b)


if IS_LAB4:
    for method in [left_rect, right_rect, middle_rect, trapezoid, simpson]:
        J1 =  calculate(f, method, a, b, m)
        J2 =  calculate(f, method, a, b, m*l) 
        R  = (J2-J1) / (l ** (method.d + 1) - 1)
        J_adj = J2 + R
        print("[m] %s: J = %.20f,\n\tфактическая погрешность:\t%.20f\n\tотносительная погрешность:\t%.20f\n\tтеоретическая погрешность<=\t%.20f" % (method.title, J1, abs(J-J1), abs(abs(J-J1)/J) if J != 0 else 0, \
            residue(method.d, method.C, a, b, m)))

        print("[m*l] %s: J = %.20f,\n\tфактическая погрешность:\t%.20f\n\tотносительная погрешность:\t%.20f\n\tтеоретическая погрешность<=\t%.20f" % (method.title, J2, abs(J-J2), abs(abs(J-J2)/J) if J != 0 else 0, \
            residue(method.d, method.C, a, b, m*l)))
        print("[m*l+Runge] %s: J = %.20f,\n\tфактическая погрешность:\t%.20f\n\tотносительная погрешность:\t%.20f" % (method.title, J_adj, abs(J-J_adj), abs(abs(J-J_adj)/J) if J != 0 else 0))
    
else:
    for method in [left_rect, right_rect, middle_rect, trapezoid, simpson]:
        J1 =  calculate(f, method, a, b, m)
        print("%s: J = %.20f,\n\tфактическая погрешность:\t%.20f\n\tотносительная погрешность:\t%.20f\n\tтеоретическая погрешность<=\t%.20f" % (method.title, J1, abs(J-J1), abs(abs(J-J1)/J) if J != 0 else 0, \
            residue(method.d, method.C, a, b, m)))
