import os
import time
commandBase = "python hidxgen.py "

for repo in os.listdir('vul'):
	start = time.time()
	os.system(commandBase + repo)
	print time.time() - start, "sec"

	# for absLvl in range(0, 5):
	# 	for granLvl in range(4, 10):
	# 		os.system(commandBase + repo + ' ' + str(absLvl) + ' ' + str(granLvl))
	# 		

	# 	start = time.time()
	# 	os.system(commandBase + repo + ' ' + str(absLvl) + ' f')
	# 	print time.time() - start, "sec"

