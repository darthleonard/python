def f(x):
    return -pow(x, 2) - 2*x + 3

def calculate(a, b, n):
    h = (float(b - a) / n)
    summatory = f(a) + f(b)
    for i in range(1, n):
        summatory += (2 if i % 3 == 0 else 3) * f(a + i * h)
    return (float( 3 * h) / 8 ) * summatory

lower_limit = -1
upper_limit = 1
interval = 100

result = calculate(lower_limit, upper_limit, interval)

print(round(result, 6))
