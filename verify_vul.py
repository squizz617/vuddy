import os
import sys
import parseutility as pu

dirs = os.listdir('vul')
for dir in dirs:
	for vul in os.listdir(os.path.join('vul', dir)):
		if vul.endswith("OLD.vul"):
			with open(os.path.join('vul', dir, vul), "r") as fp:
				raw = ''.join(fp.readlines())
				body = pu.getBody(pu.removeComment(raw))
				# print body
			cnt = 0
			for line in body.split('\n'):
				if len(line.strip()) > 0:
					cnt += 1

			if cnt == 1:
				vulBase = vul[:-8]
				print vulBase
				print raw
				print "======"
				os.remove(os.path.join('vul', dir, vulBase + "_OLD.vul"))
				os.remove(os.path.join('vul', dir, vulBase + "_NEW.vul"))
				os.remove(os.path.join('vul', dir, vulBase + ".patch"))
