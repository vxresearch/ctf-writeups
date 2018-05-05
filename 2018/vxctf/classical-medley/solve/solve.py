from pwn import *
import gmpy2

host = "35.185.151.73"
port = 8031

r = remote(host,port)

r.recvline()
r.recvline()

nstr = r.recvline()
n = int(nstr[3:-1])

cstr = r.recvline()
ciphertext = eval(cstr[12:-1])
print ciphertext

# stage 2
r.recvline()
r.recvline()
r.recvline()
cstr = r.recvline()
ciphertext2 = eval(cstr[12:-1])
print ciphertext2
r.close()

# Stage 1
inc = []
for i in range(256):
    inc.append(i * (n-1)/255)

flag = "vx"
f = []
for i in flag:
    f.append(inc[ord(i)])
c = ciphertext
# may fail as f[0]-f[1] may not have inverse, you can try other pairs, or i just random generate again using server, success in third time.
a = ((c[0] - c[1]) % n) * gmpy2.invert((f[0]-f[1]) % n,n)
a %= n
b = (c[0] - a * f[0]) % n
ainv = gmpy2.invert(a,n)
flag = ""
for i in range(len(c)):
    flag += chr(inc.index(((c[i]-b) % n * ainv) % n))

print flag



# Stage 2
c2 = ciphertext2
for i in range(9):
    for j in range(9):
        c2[i][j] = chr(inc.index(c2[i][j]))

print c2

def dr(arr,ori):
    for i in range(len(arr)):
        if arr[i] != ori[i]:
            continue
        return False
    return True
i9 = [i for i in range(9)]
original = [i for i in range(9)]
import itertools
for it in itertools.permutations(i9,9):
    if dr(it,original):
        tmp = ["" for _ in range(9)]
        for k in range(9):
            tmp[k] = c2[0][it.index(k)]
        if (tmp[0] == 'v' and tmp[1] == 'x' and tmp[2] == 'c' and tmp[3] == 't' and tmp[4] == 'f' and tmp[5] == '{'):
            flag = ""
            for i in range(9):
                for k in range(9):
                    tmp[k] = c2[i][it.index(k)]
                flag += "".join(tmp)
            print flag


