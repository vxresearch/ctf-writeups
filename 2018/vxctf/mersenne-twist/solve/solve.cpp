#include <bits/stdc++.h>

using namespace std;

struct Random {
	mt19937_64 rng;
	uint64_t state;
	int count;
	Random(uint64_t seed) : rng(seed), state(0), count(0) {}
	uint64_t getNumber() {
		if (count == 0)
			state = rng();
		uint64_t res = state & (0xFF << (8 * (3 - count)));
		res >> (8 * (3 - count));
		count++;
		if (count > 3) count = 0;
		return res;
	}
};

int main(int argc, const char **argv) {
	if (argc < 4){
		cerr << "[*] Usage: " << argv[0] << " flag.out start end" << endl;
		return 1; 
	}
	// bug, atoi return sign int, which 32 bit int fail
	uint64_t start = stoull(argv[2]);
	uint64_t end = stoull(argv[3]);
	string flag = "vxctf{";
	valarray<uint64_t> ft(flag.size());
	copy(flag.begin(), flag.end(), begin(ft));
	string f(argv[1]);
	ifstream in(f, ios::binary);

	// you know its 49 by wc flag.out
	valarray<uint64_t> cipher(49);
	char buf[8];
	for (int i = 0; i < 49; i++){
		in.read(buf,8);
		cipher[i] = *reinterpret_cast<uint64_t*>(buf);
	}
	ofstream log("log", ios::out | ios::app);
	for (uint64_t i = start; i <= end; i++){
		if (i % 0xFFFFF == 0)
			log << "Start: " << start << "Percentage: " << (i-start)*100.0/(end-start) << endl;
		Random stream(i);
		int count = 0;
		string realflag = "";
		for (auto x : cipher) {
			x ^= stream.getNumber();
			if ((count < 6) && (x != ft[count])) break;
			log.write(reinterpret_cast<const char*>(&x), sizeof x);
			realflag += reinterpret_cast<const char*>(&x);
			count++;
		}
		if (count > 5) {
			ofstream fout("realflag");
			fout << realflag << endl;
			return 0;
		}
	}
}
