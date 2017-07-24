import urllib, urllib2
header = {"Cookie": "PHPSESSID=yaoi"}

req = urllib2.Request('http://128.199.190.23:8002/index.php?page=encrypt',None,header)
res = urllib2.urlopen(req)
red = res.read().split('token" value=')
token = red[1][:32]
res.close()

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!}"
done = 0
unknown = 'MeePwnCTF{' #MeePwnCTF{Tim3_t0w4tch_mY_0niichan_CSC_win_somE_D3cRypti0n}
while done == 0:
    if unknown[-1] == "}":
        break
    params = urllib.urlencode({
        'enc': unknown+"`", #let's say they don't use backtick in flag lol
        'token': token
    })
    req = urllib2.Request('http://128.199.190.23:8002/index.php?page=encrypt',params,header)
    res = urllib2.urlopen(req)
    red = res.read()
    token = red.split('token" value=')[1][:32]
    oracleX = red.split('blue">')[1][:4]

    done = 1
    for i in charset:
            unknown += i
            print 'Checking: ', unknown
            params = urllib.urlencode({
                'enc': unknown,
                'token': token
            })
            req = urllib2.Request('http://128.199.190.23:8002/index.php?page=encrypt',params,header)
            res = urllib2.urlopen(req)
            red = res.read()
            token = red.split('token" value=')[1][:32]
            oracle = red.split('blue">')[1][:4]      
            if oracle != oracleX:
                print "Found: ", unknown
                done = 0
                break
            else:
                unknown = unknown[:-1]
            res.close()
print "Done: ", unknown
