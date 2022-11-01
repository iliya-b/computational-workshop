from functools import reduce
from  math import  log
format = lambda p: "%.4f\t%.4f" % (p[0], p[1])

def print_table(table):
    print('X\tY')
    print('\n'.join(map(format, table)))

def newtone_polynome(table):
    X, _ = zip(*table)
    n = len(table)
    def A(j):
        if j == 0:
            return f(X[0])
        x, y = table[j]
        _x, _y = table[j-1]
        return (y - _y)/(x - _x)

    def P(x):
        S = 0
        acc = 1
        for j in range(n):
            S += A(j) * acc
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
    return log(1 + x)

a, b = 0, 1

def f_table(m):
    X = [a + j*(b - a)/m for j in range(m + 1)]
    Y = [f(x) for x in X]
    return list(zip(X, Y))

print('Задача алгебраического интерполирования. Вариант 2.')
print('f(x) = ln(1+x)')

m = int(input('Число значений в таблице m = '))
base_table = f_table(m)

while True:
    x = float(input('Точка интерполирования x = '))
    print_table(base_table)
    n = m + 1
    while n > m:
        n = int(input('Степень многочлена (n ≤ m) n = ')) + 1

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
