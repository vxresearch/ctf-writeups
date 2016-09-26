#!/usr/bin/env python

from sys import stdin, stdout, stderr
from itertools import product
from re import search
from string import digits, letters
from hashlib import sha1

def proof_of_work():
    # Before we begin, a quick proof of work:\n
    stderr.write(stdin.readline())
    # Give me a string starting with {}, of length {}, such that its sha1 sum ends in ffffff\n
    line = stdin.readline()
    stderr.write(line)
    stderr.flush()
    m = search(r'with (\w+), of length (\d+)', line)
    assert m is not None
    prefix = m.group(1)
    length = long(m.group(2))
    for t in product(digits + letters, repeat=length-len(prefix)):
        s = prefix + "".join(t)
        if sha1(s).digest()[-3:] == "\xff"*3:
            stderr.write("{}\n".format(s))
            stderr.flush()
            stdout.write(s)
            stdout.flush()
            return

def guess():
    # Welcome to the LSB oracle! N = {}\n
    line = stdin.readline()
    stderr.write(line)
    m = search(r'N = (\d+)', line)
    assert m is not None
    N = long(m.group(1))
    # Encrypted Flag: {}\n
    line = stdin.readline()
    stderr.write(line)
    stderr.flush()
    m = search(r'Encrypted Flag: (\d+)', line)
    assert m is not None
    enc_flag = long(m.group(1))
    # Give a ciphertext:
    lower = 0
    upper = N
    c = enc_flag
    i = 0
    while lower < upper:
        c = (4 * c) % N
        stdout.write("{}\n".format(c))
        stdout.flush()
        # lsb is {}\n
        m = search(r'lsb is (\d+)', stdin.readline())
        assert m is not None
        lsb = int(m.group(1))
        if lsb == 1:
            lower = (lower + upper) // 2
        else:
            upper = (lower + upper) // 2
        stderr.write("#{} lsb={} remaining={} {}<=x<{}\n".
            format(i, lsb, (upper-lower).bit_length(), lower, upper))
        stderr.flush()
        i += 1
    stderr.write("flag is {}\n".format(format(upper, 'x').decode('hex')))
    stderr.flush()

proof_of_work()
guess()
