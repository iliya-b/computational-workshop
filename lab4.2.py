from scipy import integrate
from math import cos, sin, log, sqrt

print ("Приближённое вычисление интеграла по квадратурным формулам")
print ("Вариант 2 J = ∫cos(x)*x^2 dx")

input_f = input ("Введите другую функцию для интегрирования или нажмите enter: ")
if input_f.strip():
    f = eval("lambda x: " + input_f.strip())
else:
    f = lambda x: cos(x)*x*x

print("Ввод пределов интегрирования")
a =  float(input ('a = ')) # 0
b =  float(input ('b = ')) # 1

J, _ = integrate.quad(f, a, b)

print('Точное значение J=%f' % J)

def left_rect(a, b):
    return (a,), (1,)
left_rect.title = 'КФ левого прямоугольника'

def right_rect(a, b):
    return  (b,), (1,)
right_rect.title = 'КФ правого прямоугольника'

def middle_rect(a, b):
    return ((a+b)/2,), (1,)
middle_rect.title = 'КФ среднего прямоугольника'

def trapezoid(a, b):
    return (a, b), (0.5, 0.5)
trapezoid.title = 'КФ трапеции'

def simpson(a, b):
    return  (a, (a+b)/2, b), (1/6, 4/6, 1/6)
simpson.title = 'КФ Симпсона'

def three_over_eight(a, b):
    return (a,(2*a+b)/3, (a+2*b)/3, b), (1/8, 3/8, 3/8, 1/8)
three_over_eight.title = 'КФ 3/8'

def calculate(f, method, a, b):
    nodes, weights = method(a, b)
    S = 0
    for node, weight in zip(nodes, weights):
        S += f(node)*weight 
    return (b-a)*S

for method in [left_rect, right_rect, middle_rect, trapezoid, simpson, three_over_eight]:
    J1 =  calculate(f, method, a, b)
    print('%s: J = %f, погрешность: %.20f' % (method.title, J1, abs(J-J1)))