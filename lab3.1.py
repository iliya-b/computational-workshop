from lab2 import * 

def bisection(f, a, b, e):
    steps = 0
    while b - a > 2 * e:
        steps += 1
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
            
    return (a + b) / 2
    

if __name__ == '__main__':
    print('Задача обратного интерполирования. Вариант 2.')
    print('f(x) = ln(1+x)')

    m = int(input('Число значений в таблице: ')) - 1
    a, b = float(input('Введите a: ')), float(input('Введите b: '))
    base_table = f_table(m, a, b)
    print_table(base_table)
    X, Y = zip(*base_table)
    inverse_table = list(zip(Y, X))
    while True:
        F = float(input('Значение в точке F = '))

        n = m + 1
        while n > m:
            n = int(input('Степень многочлена (n ≤ %d) n = ' % m))

        e = float(input('Точность бисекции ε = '))


        #### method 1
        table = sorted(inverse_table, key=lambda point: abs(point[0] - F))[:n+1]
        P = newtone_polynome(table)
        X = P(F)
        print("НЬЮТОН P(F) = ", X)
        print("НЬЮТОН невязка: ", abs(F - f(X)))

        #### method 2
        table = base_table[:n+1]
        P = newtone_polynome(table)

        x = bisection(lambda x: P(x) - F, a, b, e)
        print("BISECTION x =", x)
        print("BISECTION невязка", abs(F - f(x)))

        if input('повтор? [N/y]: ') != 'y':
            break


