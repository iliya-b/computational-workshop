from math import exp
from lab2 import * 

def f(x):
    return exp(1.5 * 3 * x)

def df(x):
    return exp(1.5 * 3 * x) * 1.5 * 3

def ddf(x):
    return exp(1.5 * 3 * x) * 1.5 * 3 * 1.5 * 3


def f_table(m, a, b):
    X = [a + j*(b - a)/m for j in range(m + 1)]
    Y = [f(x) for x in X]
    return list(zip(X, Y))



def lab():
    print('Задача численного дифференцирования. Вариант 2.')
    print('f(x) = ln(1+x)')

    m = int(input('Число значений в таблице: ')) - 1
    a, h = float(input('Введите a: ')), float(input('Введите h: '))
    table = f_table(m, a, a + h*m)
    print_table(table)
    
    n = m
    print("x_i\tf(x_i)\t\tf'(x_i)чд\tабс_погр\tотн_погр\tf''(x_i)чд\tабс_погр\tотн_погр")
    for k, (x, y) in enumerate(table):
        if k == 0:
            x1, y1 = table[1]
            x2, y2 = table[2]
            der1 = (-3*y + 4*y1 - y2) / (2*h)
            der2 = None
        elif k == len(table) - 1:
            x1, y1 = table[-2]
            x2, y2 = table[-3]
            der1 = (3*y - 4*y1 + y2) / (2*h)
            der2 = None
        else:
            x1, y1 = table[k + 1]
            x2, y2 = table[k - 1]
            der1 = (y1  - y2) / (2*h)
            der2 = (y1 - 2*y + y2) / ((x1 - x)**2)
        
        acc1 = abs(der1 - df(x))

        if der2 is not None:
            acc2 = abs(der2 - ddf(x))
            print("%.5f\t%.10f\t%.10f\t%.10f\t%.10f\t%.10f\t%.10f\t%.10f" % (x, y, der1, acc1, acc1/df(x),der2,acc2,acc2/ddf(x)))
        else:
            print("%.5f\t%.10f\t%.10f\t%.10f\t%.10f\t------------\t-------------\t-----------" % (x, y, der1, acc1, acc1/df(x)))
    if input('Повтор [Y/n]: ').strip() == 'n':
        return
    lab()



if __name__ == '__main__':
    lab()