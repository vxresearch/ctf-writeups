# Useless returnz (Misc ???) 750 pt
----
## As usual Cantonese writeup come first, English writeup at the bottom. This writeup expect you know <useless> ALREADY.

## Intro (TL;DR)
前段由Kris 做, 跟住@samueltangz做左一part再俾我執尾刀 :0)

基本上就係chain 埋 useless 同埋linear block cipher.

呢題其實crypto題黎 :0)

題目描述:
> Useless returnz
> I don't know the cipher Key, but I can login as admin using "Useless" challenge!
> http://13.125.133.10
----
# Useless
Done by Ringo, Kris ??
Ringo 寫既writeup:
1. clone git repo from the website w/ GitTools
2. git checkout 7294 -> get enc.py with a function called encrypt
3. encrypt("admin127.0.0.1")
4. put the encrypted str back into cookie and get flag
----
# Writeup
咁同useless一樣都係有個網址啦, 好似同useless一樣都拎到個git既

咁一樣都係有 enc.py啦

但係enc.py 無key 無iv

咁點做好先gen到 encrypt("admin127.0.0.1") 黎log做admin呢?

整條一樣length既野, like account w0ng, 九個字既ip (我求其用vpngate都搵到) 黎gen encrypt("w0ng68.118.127.7"), encrypt("admin127.0.0.1")^encrypt("w0ng68.118.127.7")係任何(iv,key) pair之下都會係constant.

所以要做既野就係:
1. 係佢個site到用九個字ip reg 四個字ac (account name 最短四個字)
2. get cookie = 呢度既話係 get encrypt("w0ng68.118.127.7") by 佢地既(iv,key) pair (即係server side個pair)
3. 自己用enc.py 用求其一組(iv,key) pair gen encrpyt("w0ng68.118.127.7) 同埋 encrypt("admin127.0.0.1") 再xor埋佢地得```diff```
4. admin cookie就會係 ```cookie^diff```

咁就改cookie login到 :0)

^done by @samueltangz, 所以我無code. 咁 trivial 就當 exercise啦 :0)

但係login到都係唔得, 佢叫你用server (iv,key) pair encrpyt("IT's_Wh3re_MY_De4M0n5_Hid3_###_") 先係條flag :0)

咁就要攻擊個cryptosystem.

Kris 就俾左個idea: 改某d digit先會影響到個result ，改其他字都唔會搞到個result

咁@samueltangz就諗到linear cryptanaylsis 既方向: 試

iv一樣, key AAAAAAAAAAAAAAAA 同key BAAAAAAAAAAAAAAA 對個結果有咩影響

每個digit都試到係linearly affect :0) (佢真係好鐘意black box testing :0) )

i.e. key AAAAAAAAAAAAAAAA 同key BAAAAAAAAAAAAAAA result xor 之後某d byte 變03 = (A^B) :0), 其他byte 00 (即係無影響果d byte :0) )

^ done in fuckcry.py



即係可以做linear algebra Gaussian elimination :0)

i.e. 每個bit in iv/key (xor) 都會影響特定既output (cipher xor) bit

咁我地有(plaintext, ciphertext) pair using hidden (iv,key) pair (server side key pair),

咁就再gen個(plaintext, ciphertext) pair using known (iv,key) pair (A*8, A*16),

行 Gaussian elimination 計 (possible) 兩組(iv, key) pair既 xored result.

咁就recover到 (possible) 既 hidden (iv,key) pair.

講possible係因為呢個setup有好多組(iv,key)都encrypt到同結果 (i.e. 佢地既encrypt function 係一樣既) :0) (iv,key) pair 唔unique得好犀利 :0)

咁@samueltangz就俾左我執尾刀.


用sage 整左個GF(2) Gaussian elimination (xor = addition in GF(2))

model leave as exercise :0)

^done in fuckla.sage


咁就solve到Gaussian rref後既結果啦, 因為有192個variable (iv+key bits) 但係得 128 條equation (ciphertext bits) -> solution is not unique.

我地要手動令某d bit變0 -> 第一個1先set佢做1, 其他照set 0.

用翻個model we get: 

iv_x: 3546255950330000 \<\- set 第一個1以外既做0

key_x: 6e46174d6a4d447c6f00000000000000 \<\- set其他(128 row 之外)做0


咁將呢個xor翻known iv pair (A*8, A*16) 就等於server key (at least 效果等於server key)


咁我地就可以用黎encrypt 果串given string and get flag.



----
## Intro (TL;DR) English writeup
Done jointly by Kris, @samueltangz and harrier

Chain Useless and linear block cipher.

This is really a crypto question.

Description:
> Useless returnz
I don't know the cipher Key, but I can login as admin using "Useless" challenge!
http://13.125.133.10
----
## Useless
Done by Ringo, Kris ???

Writeup by Ringo:
1. clone git repo from the website w/ GitTools
2. git checkout 7294 -> get enc.py with a function called encrypt
3. encrypt("admin127.0.0.1")
4. put the encrypted str back into cookie and get flag
----
## Writeup
Same with useless, we are given a site, and obtain git likewise as in useless.

And we get the enc.py.

But this enc.py have the encrypt function without key nor iv.

Then how we can generate encrypt("admin127.0.0.1") to login as admin?

So the method we use here will be, generate a plaintext with same length, like an account name of "w0ng", and with ipaddress with only 9 number (as following), (I found this ip randomly on vpngate) "w0ng68.118.127.7". 

We found encrypt("admin127.0.0.1")^encrypt("w0ng68.118.127.7") under any (iv,key) pair will be constant.

So we need to do the following:
1. use the site register an four-character account (as it need at least 4 char) using a "9-lengthed" ip.
2. get cookie -> here will be encrypt("w0ng68.118.127.7") by their (iv,key) pair (i.e. server side)
3. Use enc.py to generate encrypt("w0ng68.118.127.7") and encrypt("admin127.0.0.1") using same whatever (iv,key) pair, then xor the result to get ```diff ```
4. admin cookie will be ```cookie^diff```

Then we can login as admin simply by changing cookie :0)

^done by @samueltangz, so I dont have the code. Its trivial as an exercise :0)


But login is just part 1. They tell you the flag is encrpyt("IT's_Wh3re_MY_De4M0n5_Hid3_###_") using server (iv,key) pair :0)

So we need to attack the cryptosystem.

Kris give out an idea: changing some digit of the key will change the result, changing some other digit will not change the result

Then @samueltangz comes out a way to test, using linear cryptanaylsis (he really like black box testing :0) ) :

try how the result (cipher) will change under same iv, key AAAAAAAAAAAAAAAA and key BAAAAAAAAAAAAAAA.

With every digit its linearly affecting the ciphertext :0)

i.e. key AAAAAAAAAAAAAAAA and key BAAAAAAAAAAAAAAA, some byte is 03 (A^B) with their result xor together :0) (Other will be 0, thus no change to those byte :0) )

^ done in fuckcry.py


This means we can do linear algebra, specificly Gaussian elimination :0)

i.e. every bit in iv/key (xored together) will change certain bits in output (cipher xored together)

So we have (plaintext, ciphertext) pair using hidden (iv,key) pair (server side key pair)

Then we geberate (plaintext, ciphertext) pair using known (iv,key) pair (A*8, A*16),

We run Gaussian elimination to calculate xor of two ciphertext generated by two (iv,key) pairs (one known, one hidden).

Then we can recover a (possible) hidden (iv,key) pair.

The reason of (possible) is because the setup/design makes many (iv,key) will be able to encrypt a same result, i.e. their encrypt function is essentially the same :0) (iv,key) pair is extremely not unique :0)

Then @samueltangz made me do the rest.



I use sage build a GF(2) Gaussian elimination solver (xor = addition in GF(2))

The modeling is leave as exercise :0)

^done in fuckla.sage


Then we can get the result after solving Gaussian rref. Because there are 192 variable (iv+key bits) but only 128 equations (ciphertext bit) -> solution is not unique.

We need to manuelly change some bits to 0 to make it a valid xored (iv,key) pair -> We set bits as 1 if it occurs first (leftmost in a row), otherwise 0.

Using the model we made, we get: 

iv_x: 3546255950330000 \<\- set all bits not first occurence as 0

key_x: 6e46174d6a4d447c6f00000000000000 \<\- set other (out of 128 rows) as 0


Then we use this result xor the known iv pair (A*8, A*16) and this will be equal to the server key (at least the encryption function is the same)


So we can use it to encrypt the given string and get flag.

