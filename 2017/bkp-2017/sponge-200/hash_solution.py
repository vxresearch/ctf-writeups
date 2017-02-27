from Crypto.Cipher import AES
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import sys

"""
The challenge's hash function is based on the [sponge
construction](https://en.wikipedia.org/wiki/Sponge_function). A naive
brute-force preimage attack requires O(2^48) AES computations which is
apparently unattainable. However, since this hash function uses AES as the
permutation function and the secret key is known, the permutation is thus
invertible. Therefore, we can perform a meet-in-the-middle attack to obtain a
2nd preimage using about O(2^(48/2+1)) AES compuations and O(2^(48/2)) memory
space. The attack completes in about 1 minute.
"""

def to_hex(s):
  out = ""
  for c in s:
    out += "%02X" % ord(c)
  return out

def xor(a, b):
  out = ""
  for i in range(len(a)):
    out += chr(ord(a[i]) ^ ord(b[i]))
  return out

class Hasher:
  def __init__(self):
    self.aes = AES.new('\x00'*16)

  def reset(self):
    self.state = '\x00'*16

  def ingest(self, block):
    """Ingest a block of 10 characters """
    b = block
    block += '\x00'*6
    state = ""
    for i in range(16):
      state += chr(ord(self.state[i]) ^ ord(block[i]))
    self.state = self.aes.encrypt(state)
    print "\tingest {} ('{}') => r={}, c={}".format(to_hex(b), b, to_hex(self.state[0:10]), to_hex(self.state[10:16]))

  def final_ingest(self, block):
    """Call this for the final ingestion.

    Calling this with a 0 length block is the same as calling it one round
    earlier with a 10 length block.
    """
    if len(block) == 10:
      self.ingest(block)
      self.ingest('\x80' + '\x00'*8 + '\x01')
    elif len(block) == 9:
      self.ingest(block + '\x81')
    else:
      self.ingest(block + '\x80' + '\x00'*(8-len(block)) + '\x01')

  def squeeze(self):
    """Output a block of hash information"""
    result = self.state[:10]
    self.state = self.aes.encrypt(self.state)
    print "\tsqueeze => r={}, c={}".format(to_hex(self.state[0:10]), to_hex(self.state[10:16]))
    return result

  def hash(self, s):
    """Hash an input of any length of bytes.  Return a 160-bit digest."""
    print "Hashing {} ('{}')".format(to_hex(s), s)
    self.reset()
    blocks = len(s) // 10
    for i in range(blocks):
      self.ingest(s[10*i:10*(i+1)])
    self.final_ingest(s[blocks*10:])

    return self.squeeze() + self.squeeze()

HASHER = Hasher()
GIVEN = 'I love using sponges for crypto'
TARGET = HASHER.hash(GIVEN)
print "TARGET = {}".format(to_hex(TARGET))

aes = AES.new('\x00'*16)
table = {}

print "Precompute..."
r = 'EBC3BE61BC5708451FBC'.decode('hex') # Arbitrary seed
c2 = 'AFCFECD21A8D'.decode('hex') # C_2 of the target hash. Collision target.
for i in xrange(2**24):
  s = aes.decrypt(r + c2)
  r = s[0:10]
  c = s[10:]
  table[c] = r

print "Search forward..."
r = '\x00'*10 # Arbitrary seed
c0 = '\x00'*6 # Initial value of C. A constant.
for i in xrange(2**25):
  s1 = aes.encrypt(r + c0)
  r1 = s1[0:10]
  c1 = s1[10:]
  if table.has_key(c1):
    r1_m1 = table[c1]
    r2 = aes.encrypt(r1_m1 + c1)[0:10]
    r2_m2 = xor('EBC3BE61BC5708451FBC'.decode('hex'), ' for crypt')
    b = []
    b.append(r)
    b.append(xor(r1, r1_m1))
    b.append(xor(r2, r2_m2))
    b.append('o')
    m = "".join(b)

    print "Found m={} s1={}".format(to_hex(m), to_hex(s1))
    h = HASHER.hash(m)
    print "RESULT = {}".format(to_hex(h))
  r = r1


