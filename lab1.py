from  math import sin, cos, log


debug = True

def f(x):
    return 2**(-x) - sin(x)

def df(x):
    return -log(2) * 2**(-x) - cos(x)

def separate(a, b, n):
    res = []
    h = (b - a) / n
    x1 = a
    x2 = x1 + h
    y1 = f(x1)

    while x2 <= b:
        y2 = f(x2)
        if y1 * y2 <= 0:
            res.append( (x1, x2) )
        (x1, x2) = (x2, x1 + h)
        y1 = y2
    return res

def bisection(a, b, e):
    steps = 0
    while b - a > 2 * e:
        steps += 1
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
    if debug:
        print('steps: ', steps )
        print('|b - a|', abs(b - a))
    return (a + b) / 2
    
def newtone(a, b, e):
    x = (a + b) / 2
    prev = None
    steps = 0
    while prev is None or abs(x - prev) >= e:
        steps += 1
        prev = x
        x = x - f(x) / df(x)
    if debug:
        print('steps: ', steps)
        print('|x_m - x_m-1| = ', abs(x - prev))

    return x


def modified_newtone(a, b, e):
    x = (a + b) / 2
    df_0 = df(x)
    prev = None
    steps = 0

    while prev is None or abs(x - prev) >= e:
        steps += 1
        prev = x
        x = x - f(x) / df_0

    if debug:
        print('steps: ', steps)
        print('|x_m - x_m-1| = ', abs(x - prev))

    return x

def secant(a, b, e):
    x = b
    x_prev = a
    steps = 0
    while abs(x - x_prev) >= e:
        steps += 1
        tmp = x
        x = x - (x - x_prev) * f(x) / (f(x) - f(x_prev)) 
        x_prev = tmp

    if debug:
        print('steps: ', steps)
    return x


print('ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ')
e = input('ε = ') ; e = float(eval(e)) # 0.000001
A, B = eval(input('A, B = ')); A = float(A) ; B = float(B) # -5, 10
N = 5
print('A, B = ' , A, B)
print('ε = ' , e)

intervals = separate (A, B, N)

print(intervals, len(intervals))


algos = [bisection, newtone, modified_newtone, secant]
for algo in algos:
    print(algo.__name__)
    for interval in intervals:
        a, b = interval
        approx = algo(a, b, e)
        print(interval, approx, abs(f(approx)))