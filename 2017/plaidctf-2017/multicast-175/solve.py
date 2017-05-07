import math

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * modinv(p, n_i) * p
    return sum % prod

f = open('data.txt', 'r')

ncr = [1, 5, 10, 10, 5, 1]

gs = [[0 for x in range(5)] for y in range(6)]
n = []
p = []
q = []
nprod = 1

for i in range(5):
    a = int(f.readline())
    b = int(f.readline())
    c = int(f.readline())
    n.append(int(f.readline()))
    ainv = modinv(a, n[i])
    p.append(ainv * b % n[i])
    q.append(pow(ainv, 5, n[i]) * c % n[i])
    # (m + pi)^5 = qi
    nprod *= n[i]

for i in range(5):
    for j in range(6):
        gs[j][i] = ncr[j] * pow(p[i], j, nprod) % n[i]
    gs[5][i] = ((gs[5][i] - q[i]) % n[i] + n[i]) % n[i]

gg = []
for i in range(6):
    gg.append(chinese_remainder(n, gs[i]))

print "N = %d" % nprod
print "x^5 + %d*x^4 + %d*x^3 + %d*x^2 + %d*x + %d" % (gg[1], gg[2], gg[3], gg[4], gg[5])
