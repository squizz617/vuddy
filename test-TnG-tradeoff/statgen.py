import os
import sys

fileList = sorted(os.listdir("RESULTS"))
os.chdir("RESULTS")

"""
lines[1] - gran 4
lines[4] - gran 7
lines[7] - gran 10
lines[8] - gran func
"""

string = ""
i = 10
for f in fileList:
	with open(f, "r") as fp:
		lines = fp.readlines()
		timesAsString = lines[8].rstrip().split('\t')[1:]
		timesAsFloat = []
		for t in timesAsString:
			timesAsFloat.append(float(t))
		# print timesAsFloat
		prep_ratio = timesAsFloat[0] / timesAsFloat[4] * 100
		hash_ratio = timesAsFloat[1] / timesAsFloat[4] * 100
		store_ratio = timesAsFloat[2] / timesAsFloat[4] * 100
		io_ratio = timesAsFloat[3] / timesAsFloat[4] * 100
		if i % 10 == 0:
			print "%d\t%.6f\t%.6f\t%.6f\t%.6f" % (i, timesAsFloat[0], timesAsFloat[1], timesAsFloat[2], timesAsFloat[3])
		if i == 40:
			break
		i += 1

		# prep_ratio = 
		# string += str(lines[1].split('\t')[-1].rstrip()) + '\t'

# print string