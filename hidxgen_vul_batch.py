import os

vulList = os.listdir("vul")
print vulList

for vul in vulList:
	os.system("python hidxgen_vul.py " + vul + " 4 100")
