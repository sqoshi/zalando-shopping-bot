import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if ".ui" in f:
        print(f[:len(f) - 3])
        os.system("pyuic5 -x " + f + " -o " + f[:len(f) - 3] + ".py -x")
os.system("rm os")
