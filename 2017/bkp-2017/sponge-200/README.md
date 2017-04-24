# Boston Key Party 2017: Sponge (Crypto, 200)

說明：
> I've written a hash function. Come up with a string that collides with "`I love using sponges for crypto`".
>
> [hash.py](hash.py)

## 解題

目標是對一個自定義的hash function進行2nd preimage攻擊，找出另一個和`I love using sponges for crypto`擁有一樣hash value的字串。

題目的hash function是基於[sponge construction](https://en.wikipedia.org/wiki/Sponge_function)設計（題目名字的暗示也很明顯）。

![Sponge construction](https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/SpongeConstruction.svg/1000px-SpongeConstruction.svg.png)

## Meet-in-the-middle攻擊

用窮舉法去找preimage的話須要O(2<sup>c</sup>)次AES運算，這裡c=48，明顯不太可能在比賽時間內完成。可是，這個hash function特別之處是用了AES作為sponge construction的permutation function，而且用固定的密鑰，所以這個permutation是可逆的。如此一來，我們可以運用[meet-in-the-middle attack](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack)找出2nd preimage，簡化成只要約O(2<sup>c/2+1</sup>)次AES運算和O(2<sup>c/2</sup>)的記憶空間，需時大約一分鐘。

## 完整解答

[hash_solution.py](hash_solution.py)

執行程式得到以下答案，遞交其中一個答案去題目的伺服器就可取得flag。

```
Hashing 49206C6F7665207573696E672073706F6E67657320666F722063727970746F ('I love using sponges for crypto')
	ingest 49206C6F766520757369 ('I love usi') => r=D940564A6F9B46249A94, c=CFE6C3D582C6
	ingest 6E672073706F6E676573 ('ng sponges') => r=EBC3BE61BC5708451FBC, c=AFCFECD21A8D
	ingest 20666F72206372797074 (' for crypt') => r=80C3CD0580D0491C117F, c=7740560A1D64
	ingest 6F800000000000000001 ('o?') => r=11153C85D1B549E58B1B, c=6FD6609E5464
	squeeze => r=40EEB0FD7E34D53A48BA, c=395445452F3E
	squeeze => r=956E116D90D5AE3DF8AE, c=2688417445F1
TARGET = 11153C85D1B549E58B1B40EEB0FD7E34D53A48BA
Precompute...
Search forward...
Found m=31857AC972C310C2581A65864A7104DEF7C6E5DC85F1A588E6B087065AD36F s1=F9BAD49C09AA5B56C81B93C998608C43
Hashing 31857AC972C310C2581A65864A7104DEF7C6E5DC85F1A588E6B087065AD36F ('1?z?r??Xe?Jq????܅?氇Z?o')
	ingest 31857AC972C310C2581A ('1?z?r??X') => r=F9BAD49C09AA5B56C81B, c=93C998608C43
	ingest 65864A7104DEF7C6E5DC ('e?Jq?????') => r=4E54749B7A84FD3A351B, c=AFCFECD21A8D
	ingest 85F1A588E6B087065AD3 ('??氇Z?') => r=80C3CD0580D0491C117F, c=7740560A1D64
	ingest 6F800000000000000001 ('o?') => r=11153C85D1B549E58B1B, c=6FD6609E5464
	squeeze => r=40EEB0FD7E34D53A48BA, c=395445452F3E
	squeeze => r=956E116D90D5AE3DF8AE, c=2688417445F1
RESULT = 11153C85D1B549E58B1B40EEB0FD7E34D53A48BA
Found m=AC85AD89B2EBF0ED9DAF63ADDB7F8B55F68F5C53721C4D43ADA61E15ECC06F s1=D92E1012749352CA2CEC51A6C0F205AA
Hashing AC85AD89B2EBF0ED9DAF63ADDB7F8B55F68F5C53721C4D43ADA61E15ECC06F ('???????흯c???U??\SrMC????o')
	ingest AC85AD89B2EBF0ED9DAF ('???????흯') => r=D92E1012749352CA2CEC, c=51A6C0F205AA
	ingest 63ADDB7F8B55F68F5C53 ('c???U??\S') => r=B9B99C50319264298308, c=AFCFECD21A8D
	ingest 721C4D43ADA61E15ECC0 ('rMC????') => r=80C3CD0580D0491C117F, c=7740560A1D64
	ingest 6F800000000000000001 ('o?') => r=11153C85D1B549E58B1B, c=6FD6609E5464
	squeeze => r=40EEB0FD7E34D53A48BA, c=395445452F3E
	squeeze => r=956E116D90D5AE3DF8AE, c=2688417445F1
RESULT = 11153C85D1B549E58B1B40EEB0FD7E34D53A48BA
```

## Flag

```
FLAG{MITM 3: This Time It's Personal!}
```