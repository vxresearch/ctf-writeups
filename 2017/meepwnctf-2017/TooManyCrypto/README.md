# MeePwn CTF 2017: TooManyCrypto

### (web, 500 points, 13 team solved)

說明
>My kawaii little sister just create it for me... She tell me there is a secret inside. I wonder what it is?
>Remote: 128.199.190.23:8002

## 題解
一 Click 入去就覺得好毒. 入面有個 Love Live 公仔 同埋 Encryption 同埋 Decryption. 
佢話 there is a secret inside, 咁一係叫你解個 key 一係就解個 salt 好似係.
話說我連 source code 都冇睇就去 encrypt 下.
你鍾意睇可以咁睇
http://128.199.190.23:8002/index.php?page=pHp://filter/convert.base64-encode/resource=index

---
求其打一隻字見係 HzhTWlvm 開頭. 打 a 又係打 b 又係. 會唔會係 fixed IV 呢? 
求其 flip 下個 ciphertext 拿去 decrypt，點都 error.
之後打 aaaaaaaa 試下, 出 PnCmtLbN 開頭.
flip 下打 aaaaaaab, 出 fOBNaW2b 開頭. 差咁鬼遠 又有雪崩效應?
打 bbbbbbbb 試下, 竟然出返 PnCmtLbN 開頭. 不過後面同 aaaaaaaa 有 d 唔同既. 用緊 google translate 既朋友你大鑊啦. 個 d 你點譯呢. 咩叫做有 d 唔同呢.
見係咁明眼人一睇就知係有 compression. 拿唔信既話你睇返 encrypt.php 真係有. 雖然我解完都冇睇過.
呢類又係翻炒 SSL compression attack 果D咩 CRIME 啊 BREACH 啊. 話晒都係 VNSecurity 地頭唔意外.
因為你知個 flag 應該係 MeePwnCTF{ 開頭, 咁你打 MeePwnCTF{ 應該會 compress 多左. 
人手試既話, 打 MeePwnCTF{ 出 HzhTWlvm 開頭, 打 MeePwnCTF[ 同 MeePwnCTF( 都係出 PnCmtLbN 開頭. 咁你靠呢個方法就可以估到佢個 salt 係乜.
想當年我都係人手試幾十個字. 依家年紀大都係搵電腦試算數.

## Remark
![baka.gif](baka.gif)
Tsu, do you know "Tanaka-kun is Always Listless" is yaoi? :-) 
From Wikipedia: "Tanaka states that because of Ohta's caring nature, he sees Ohta as the perfect candidate for marriage."
呢段咁唔正常先打英文. 吹咩.
