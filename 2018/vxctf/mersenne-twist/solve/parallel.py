import subprocess

for i in range(0x40):
    subprocess.Popen(["./solve", "flag.out", str(i*0x4000000), str((i+1)*0x4000000-1)])
    print "Spawned process", i*0x4000000


