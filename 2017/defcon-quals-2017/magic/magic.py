import angr
import simuvex
import base64
from pwn import *

context.update(log_level='debug')
r = remote('cm2k-magic_b46299df0752c152a8e0c5f0a9e5b8f0.quals.shallweplayaga.me', 12001)
r.recvline()

while True:
    chall = r.recvline().rstrip()
    if "The flag is:" in chall:
        log.info(chall)
        break
    log.info("cracking " + chall)
    p = angr.Project(chall.rstrip())
    st = p.factory.blank_state(addr=0x4007b2)
    st.regs.rdi = 0x500000
    code = st.se.BVS('code', 80 * 8)
    st.memory.store(st.regs.rdi, code)
    pg = p.factory.path_group(st)
    pg.explore(find=0x4007b7, avoid=0x400758)
    s = pg.found[0].state
    result = s.se.any_str(code)

    log.info("code is '{}'".format(result))
    r.send(base64.b64encode(result) + "\n")
