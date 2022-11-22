from functools import reduce
from  math import  log
from random import randint, random
from functools import lru_cache

format = lambda p: "%.5f\t%.4f" % (p[0], p[1])

def print_table(table):
    print('X\tY')
    print('\n'.join(map(format, table)))

def newtone_polynome(table):
    X, Y = zip(*table)
    n = len(table)

    @lru_cache
    def A(i, j):  # разделенная разность
        if i == j == 0:
            return Y[0]
        if j-i == 1:
            return (Y[j] - Y[i])/(X[j] - X[i])
            
        return (A(i+1, j)-A(i, j-1))/(X[j] - X[i])
    

    def P(x):
        S = 0
        acc = 1
        for j in range(n):
            S += A(0, j) * acc
            acc *= x - X[j]
        return S
    
    return P

def lagrange_polynome(table):
    X, Y = zip(*table)
    n = len(table)

    def P(x):
        S = 0
        for k in range(n):
            p = 1
            for i in range(n):
                if i == k:
                    continue
                p *= (x - X[i])/(X[k] - X[i])
            S += p * Y[k]
        return S
    return P


def f(x):
    return x*x/(1+x*x)

def f_table_random(m, a, b):
    X = []
    for j in range(m+1):
        X.append(randint(int(a*10000), int(b*10000))/10000)
    if len(set(X)) < len(X):
        return f_table_random(m)
    Y = [f(x) for x in X]
    return list(zip(X, Y))

def f_table(m, a, b):
    X = [a + j*(b - a)/m for j in range(m + 1)]
    Y = [f(x) for x in X]
    return list(zip(X, Y))

if __name__ == '__main__':
    print('Задача алгебраического интерполирования. Вариант 2.')
    print('f(x) = ln(1+x)')

    m = int(input('Число значений в таблице m = '))
    a, b = float(input('Введите a: ')), float(input('Введите b: '))
    base_table = f_table(m, a, b)
    print_table(base_table)

    while True:
        x = float(input('Точка интерполирования x = '))

        n = m + 1
        while n > m:
            n = int(input('Степень многочлена (n <= %d) n = ' % m))

        table = sorted(base_table, key=lambda point: abs(point[0] - x))[:n+1]

        print_table(table)

        P = newtone_polynome(table)
        print("НЬЮТОН P(x) =", P(x))
        print("НЬЮТОН погрешность: ", abs(P(x) - f(x)))



        PL = lagrange_polynome(table)
        print("ЛАГРАНЖ P(x) =", PL(x))
        print("ЛАГРАНЖ погрешность: ", abs(PL(x) - f(x)))

        if input('повтор? [N/y]: ') != 'y':
            break
