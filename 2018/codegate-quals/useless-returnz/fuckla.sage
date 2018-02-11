#!/usr/local/bin/sage -python

from sage.all import *

ivmap = {0: [0, 8], 1: [0, 2, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15], 2: [0, 5, 7, 10], 3: [0, 2, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15], 4: [4, 8, 10, 11, 12, 13, 14, 15], 5: [5, 8, 10, 15], 6: [6, 8, 9, 10, 12, 13, 14, 15], 7: [7, 15]}
keymap = {0: [0, 1, 2], 1: [0, 1, 3], 2: [0, 2, 3], 3: [1, 2, 3], 4: [4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15], 5: [4, 5, 7, 11, 14], 6: [4, 6, 7, 9, 11, 12, 14], 7: [5, 6, 7, 9, 12], 8: [0, 1, 2, 3, 4, 5, 6, 7], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [8, 9, 10, 11, 12, 13, 14, 15]}

target = "IT's_Wh3re_MY_De4M0n5_Hid3_###_"

known_plain = "w0ng68.118.127.7"

known_cipher = "110a13731c3c2d2839542f704e767f4c"

init_cipher = "4e005700060149081a5f1c055353535a"

sol = int(init_cipher,16) ^ int(known_cipher,16)
mat = []
for i in range(128):
	mat.append([])

# sol
for row in range(128):
	num = row/8
	bitpos = row % 8
	# var
	col = 0
	for i in range(8):
		for bit in range(8):
			if bitpos == bit:
				if num in ivmap[i]:
					mat[row].append(1)
				else:
					mat[row].append(0)
			else:
				print row, len(mat[row])
				mat[row].append(0)
	for i in range(16):
		for bit in range(8):
			if bitpos == bit:
				if num in keymap[i]:
					mat[row].append(1)
				else:
					mat[row].append(0)
			else:
				mat[row].append(0)
	mat[row].append(sol >> (127 - row) & 1)

A = matrix(GF(2), mat)
B = A.rref()


for i in range(128):
	s = ""
	for j in range(193):
		s += str(B[i][j])
	print s		
output = []
for i in range(128):
	output.append(str(B[i][192]))

print format(int("".join(output),2), "032x")
