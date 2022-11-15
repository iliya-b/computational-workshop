from math import exp
from lab2 import * 

def f(x):
    exp(1.5 * 3 * x)



if __name__ == '__main__':
    print('Задача численного дифференцирования. Вариант 2.')
    print('f(x) = ln(1+x)')

    m = int(input('Число значений в таблице: ')) - 1
    a, h = float(input('Введите a: ')), float(input('Введите h: '))
    base_table = f_table(m, a, a + h*m)
    print_table(base_table)
    
    n = m
    # x_i f(x_i) f'(x_i)чд абс_погр отн_погр f''(x_i)чд абс_погр отн_погр
    for (x, y) in base_table:
        table = sorted(base_table, key=lambda point: abs(point[0] - x))[:n+1]




