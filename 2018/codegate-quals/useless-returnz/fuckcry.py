from enc import Encrypt


def e(iv,key,plain):
    return Encrypt(iv,key).encrypt(plain)

target = "IT's_Wh3re_MY_De4M0n5_Hid3_###_"

known_plain = "w0ng68.118.127.7"

known_cipher = "110a13731c3c2d2839542f704e767f4c"



#map
init_iv = "A"*8
init_key = "A"*16

print e(init_iv,init_key,known_plain)


ivmap = {}
for i in range(8):
    iv = ["A"]*8
    iv[i] = "B"
    #print "".join(iv)
    diff = int(e("".join(iv),init_key,known_plain),16) ^ int(e(init_iv,init_key,known_plain),16)
    diff = format(diff,"032x")
    ivmap[i] = []
    for k in range(0,16):
        if diff[k*2+1] == "3":
            ivmap[i].append(k)
    
keymap = {}

for i in range(16):
    key = ["A"]*16
    key[i] = "B"
    #print "".join(iv)
    diff = int(e(init_iv,"".join(key),known_plain),16) ^ int(e(init_iv,init_key,known_plain),16)
    diff = format(diff,"032x")
    keymap[i] = []
    for k in range(0,16):
        if diff[k*2+1] == "3":
            keymap[i].append(k)

print ivmap
print keymap


