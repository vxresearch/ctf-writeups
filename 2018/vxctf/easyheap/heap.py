from z3 import *

s = Solver()

p = []



for i in range(2,12):
	globals()["v%i"%i]=BitVec("v%i"%i,8)
	p.append(globals()["v%i"%i])

for i in p:
    s.add(i >= 32)
    s.add(i <= 127)


s.add( And(v2 + v3 == 97
      ,(v3 != 1)
      , v3 + v4 == 166
      ,(v4 != 70)
      , v4 + v5 == 169
      ,(v5 != 69)
      , v5 + v6 == 129
      ,(v6 != 125)
      , v6 + v7 == 142
      ,(v7 != 14)
      , v7 + v8 == 174
      ,(v8 != 46)
      , v8 + v9 == 207
      ,(v9 != 15)
      , v9 + v10 == 150
      ,(v10 != 84)
      , v10 + v11 == 104
      ,(v11 != 6)))

if s.check() == sat:
	model = s.model()
	print model
	pw = {}
	for x in model:
		pw[str(x)[1:]] = chr(model[x].as_long())
	s = ""
	for i in range(2,12):
		s += pw[str(i)]
	print s

from pwn import *

host = "35.194.219.218"
port = 8238

r = remote(host,port)

r.recvline()
r.sendline(s)
r.interactive()
