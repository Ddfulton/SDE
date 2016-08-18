import subprocess

p = subprocess.Popen(["ruby", "verifyOnyen.rb", "ddfulton", "bojangles5'"], stdout=subprocess.PIPE)

out, err = p.communicate()

print(out[-3:].decode('utf-8'))