# Inter-Tertiary-Institute CTF 2017 (Hong Kong): Smallest (Pwn, 400)

> [smallest](smallest_1A96E3D505305CC1702DBA86B6ACBD4C.zip)

## 解題

這題是比賽裡唯一一題pwn題目。這是個非常細小的執行檔，只有6行指令的，連libc程式庫也沒有連結。

```asm
                     EntryPoint:
00000000004000b0         xor        rax, rax
00000000004000b3         mov        edx, 1024
00000000004000b8         mov        rsi, rsp
00000000004000bb         mov        rdi, rax
00000000004000be         syscall
00000000004000c0         ret
```

程式把`rax`設為0，設置了`edx`、`rsi`和`rdi`的值，然後執行`syscall`。在Linux裡，`rax`是用來指定要呼叫的syscall，從[syscall例表](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)得到0對應syscall是`sys_read`，`rdi`、`rsi`和`rdx`是syscall頭三個參數，分別是file descriptor，buffer位址，和要讀取的長度。

留意呼叫`sys_read`時buffer位址設置為`rsp`的值，所以讀入來的資料是直接寫到stack上的，即是我們可以真接覆寫stack上的返回位址取得程式流程的控制。

用`checksec`檢查一下執行檔，它有NX flag，所以簡單的stack buffer overflow行不通，而且這個程式連沒有連結libc，return-to-libc也不行。

```
$ checksec smallest
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
```

唯一可以做的是返回到這個程式裡的其中一行指令。

`sys_read`會返回已讀取資料的長度，syscall返回時，返回值會寫在`rax`。如果這時我們把程式導向到0x4000be，我們可以透過輸入的長度控制呼叫那個syscall。

既然能夠呼叫任意的syscall，我們可以利用[sigreturn-oriented programming](https://en.wikipedia.org/wiki/Sigreturn-oriented_programming)的方法進一步控制其他register。我們的最終的目標是呼叫sys_execve執行`sh`。sys_execve的三個參數分別是`filename`、`argv`和`envp`。換句話說，我們要把`/bin/sh`字串的記憶體位址寫入到`rdi`，把null pointer寫入`rsi`和`rdx`。

記憶體空間裡沒有`/bin/sh`這個字串，所以我們要先把字串寫入到stack上，然後把`rdi`指向這個stack上的位址。不過，因為Linux的ASLR，stack並不在固定的位址上，我們要先取得stack的位址才可以呼叫sys_execve。

這是exploit方法。首先呼叫sys_write把stack的1024 bytes到`STDOUT`。從這個輸出能夠取得[environ的指針](https://lwn.net/Articles/631631/)。environ在stack的記憶體區間當中，不過它和stack之間的間距並非固定，所以不能直接計算出stack的位址。不過我們還是可以利用它找一個可行的stack記憶體區間位址，用`sigreturn`把`rsp`更改為這個已知位址。然後我們把`/bin/sh`字串寫入stack，再用sigreturn把`rax`設為59，把`rdi`、`rsi`和`rdx`設為stack上的位址，之後跳到`syscall`就可以呼叫execve取得`sh`。

## 完整解答

[smallest.py](smallest.py)

## Flag

```
flag{833d9b6f94c2df8e0bdf7f558a677870}
```

