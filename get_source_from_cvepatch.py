"""
This module retrieves the vulnerable function from cvepatch (diff)
Author: Seulbae Kim (seulbae@korea.ac.kr)
Last Modified: July 20, 2016
Usage: python get_source_from_cvepatch REPONAME [-m]
	-m: multi-repo mode

* THIS IS MK-2.
  See Mk-1 for more info about this weird manual branching system.

[CHANGELOG]
Jul 20	SBKIM	discard comment changes

Aug 08	SBKIM	Major update: with parser (codesensor.jar)
"""

import os
import sys
import re
import subprocess
# import cparser
import pickle

import parseutility

cveDict = pickle.load(open("cvedata.pkl", "rb"))

# GLOBALS
originalDir = os.getcwd()
chunksCnt = 0		# number of DIFF patches
resultList = []
multimodeFlag = 0
dummyFunction = parseutility.function("NULL")

# ARGUMENTS
if len(sys.argv) < 2:
	repoName = "glibc"	# name of the directory that holds DIFF patches
	multimodeFlag = 0
elif len(sys.argv) == 2:
	repoName = sys.argv[1]
else:
	repoName = sys.argv[1]
	if sys.argv[2] == '-m':
		multimodeFlag = 1

print "Retrive vulnerable functions from " + repoName + "\nMulti-repo mode: ",
if multimodeFlag:
	print "On"
else:
	print "Off"

# try making missing directories
try:
	os.mkdir('vul')
except OSError as e:
	pass
try:
	os.mkdir(os.path.join(originalDir, 'vul', repoName))
except OSError as e:
	pass

""" re patterns """
# pat_merge = r"\Wmerge\s"
# compiled_merge = re.compile(pat_merge)
pat_src = '[\n](?=diff --git a/)'
pat_chunk = '[\n](?=@@\s[^a-zA-Z]*\s[^a-zA-Z]*\s@@)'
pat_linenum = r"-(\d+,\d+) \+(\d+,\d+) "
pat_linenum = re.compile(pat_linenum)

diffFileCnt = 0
total = len(os.listdir(os.path.join(originalDir, "diff", repoName)))
for diffFileName in os.listdir(os.path.join(originalDir, "diff", repoName)):	# diffFileName holds the filename of each DIFF patch
	# diffFileName looks like: CVE-2012-2372_7a9bc620049fed37a798f478c5699a11726b3d33.diff
	print str(diffFileCnt+1) + '/' + str(total),
	diffFileCnt += 1

	if os.path.getsize(os.path.join(originalDir, "diff", repoName, diffFileName)) > 1000000:
		# don't fucking do anything with big DIFFs.
		# these are often merges, upgrades, ...
		print "[-]", diffFileName, "\t(file too large)"
		pass
	else:
		diffFileNameSplitted = diffFileName.split('_')
		cveId = diffFileNameSplitted[0]	# use only one CVEid
		commitHashValue = diffFileNameSplitted[-1].split('.')[0]

		print "[+]", diffFileName, "\t(proceed)"
		with open(os.path.join(originalDir, "diff", repoName, diffFileName), 'r') as fp:
			patchLines = ''.join(fp.readlines())
			patchLinesSplitted = re.split(pat_src, patchLines)
			commitLog = patchLinesSplitted[0]
			affectedFilesList = patchLinesSplitted[1:]

			# mergeMatch = compiled_merge.search(commitLog)
			# if mergeMatch is None:	# use re for better filtering. this doesn't discard logs that contain "emerge".
			# however now, merge is filtered in the previous step (get_cvepatch_from_git.py)

			if multimodeFlag:	# multimode DIFFs have repoPath at the beginning.
				repoPath = commitLog.split('\n')[0]
			# print len(affectedFilesList), 'sources'
			numAffectedFiles = len(affectedFilesList)
			for aidx, affectedFile in enumerate(affectedFilesList):
				print "\tFile # " + str(aidx+1) + '/' + str(numAffectedFiles),
				firstLine = affectedFile.split('\n')[0]	# git --diff a/path/filename.ext b/path/filename.ext
				codePath = firstLine.split(' b')[1].strip()	# path/filename.ext

				if not codePath.endswith('.c') and not codePath.endswith('.cpp'):	# and not codePath.endswith('.cc'):
					print "\t[-]", codePath, "(wrong type)"
				else:
					secondLine = affectedFile.split('\n')[1]
					srcFileName = codePath.split('/')[-1]

					if secondLine.split(' ')[0] != "index":
						print "\t[-]", codePath, "(invalid metadata)"	# we are looking for "index"
					else:
						print "\t[+]", codePath
						# print secondLine
						indexHashOld = secondLine.split(' ')[1].split('..')[0]
						indexHashNew = secondLine.split(' ')[1].split('..')[1]
						# print "CODEPATH:  ", codePath
						# print "INDEXHASH: ", indexHashOld

						chunksList = re.split(pat_chunk, affectedFile)[1:]	# diff file per chunk (in list)
						# print len(chunksList), 'chunks'
						chunksCnt += len(chunksList)

						if multimodeFlag:
							os.chdir(os.path.join(originalDir, "data/gitrepos", repoName, repoPath))
						else:
							# os.chdir(os.path.join(originalDir, "data/gitrepos", repoName))
							os.chdir(os.path.join("/home/squizz/devgit/", repoName))	#temporary change!!!! Aug 8

						try:
							os.remove(originalDir + "/tmp_old")
							os.remove(originalDir + "/tmp_new")
						except:
							pass

						command_show = 'git show ' + indexHashOld + ">> " + originalDir + "/tmp_old"
						os.system(command_show)
						command_show = 'git show ' + indexHashNew + ">> " + originalDir + "/tmp_new"
						os.system(command_show)

						# print indexHashOld
						os.chdir(originalDir)
						
						oldFunctionInstanceList = parseutility.parseFile("tmp_old")
						newFunctionInstanceList = parseutility.parseFile("tmp_new")

						# if indexHashOld == "1e25854":	# for testing
						# 	oldFunctionInstanceList = parseutility.parseFile("tmp2")

						# if indexHashOld != "1e25854":
						os.remove("tmp_old")
						os.remove("tmp_new")
						os.chdir(os.path.join("/home/squizz/devgit/", repoName))

						finalOldFunctionList = []

						numChunks = len(chunksList)
						for ci, chunk in enumerate(chunksList):
							print "\t\tChunk # " + str(ci+1) + "/" + str(numChunks),

							chunkSplitted = chunk.split('\n')
							chunkFirstLine = chunkSplitted[0]
							chunkLines = chunkSplitted[1:]

							print chunkFirstLine
							lineNums = pat_linenum.search(chunkFirstLine)
							oldLines = lineNums.group(1).split(',')
							newLines = lineNums.group(2).split(',')
							
							offset = int(oldLines[0])
							pmList = []
							lnList = []
							for chunkLine in chunkSplitted[1:]:
								if len(chunkLine) != 0:
									# print offset, '\t', chunkLine
									pmList.append(chunkLine[0])
								# offset += 1
							
							tmp = offset
							for i, pm in enumerate(pmList):
								if pm == ' ' or pm == '-':
									lnList.append(tmp + i)
								elif pm == '+':
									lnList.append(tmp + i - 1)
									tmp -= 1

							# print pmList
							# print lnList

							# print the chunk
							# for c, chunkLine in enumerate(chunkSplitted[1:]):
							# 	if len(chunkLine) > 0:
							# 		print lnList[c], chunkLine

							# seven lines below are not used.
							# plusCnt = 0
							# minusCnt = 0
							# for pm in pmList:
							# 	if pm == '+':
							# 		plusCnt += 1
							# 	elif pm == '-':
							# 		minusCnt += 1

							# bound = offset + int(oldLines[1]) - 1
							# print "FROM", offset
							# print "TO", offset + int(oldLines[1]) - 1


							""" HERE, ADD CHECK FOR NEW FUNCTIONS """
							hitOldFunctionList = []
							for f in oldFunctionInstanceList:
								# print f.lines[0], f.lines[1]

								for num in range(f.lines[0], f.lines[1]+1):
									if num in lnList:
										# print "Hit at", num
										hitOldFunctionList.append(f)
										break	# found the function to be patched

								# if f.lines[0] <= offset <= f.lines[1]:
								# 	print "\t\t\tOffset HIT!!", f.name
								# elif f.lines[0] <= bound <= f.lines[1]:
								# 	print "\t\t\tBound  HIT!!", f.name

							for f in hitOldFunctionList:
								print "Verify hitFunction", f.name
								# print "ln",
								for num in range(f.lines[0], f.lines[1]+1):
									# print num,
									try:
										listIndex = lnList.index(num)
									except ValueError:
										pass
									else:
										# print "\nmatch:", num
										# print "value\t", chunkSplitted[1:][lnList.index(num)]
										# print "pm   \t", pmList[lnList.index(num)]
										if pmList[listIndex] == '+' or pmList[listIndex] == '-':
											# print "Maybe meaningful",
											flag = 0
											for commentKeyword in ["/*", "*/", "//", "*"]:
												if chunkLines[listIndex][1:].lstrip().startswith(commentKeyword):
													flag = 1
													break
											if flag:
												pass
												# print "but not."
											else:
												# print "MEANINGFUL!!"
												finalOldFunctionList.append(f)
												break
										else:
											pass
											# print "Not meaningful"
								# print "============\n"

						# print "FINALLY"
						finalNewFunctionList = []
						for fold in finalOldFunctionList:
							flag = 0
							for fnew in newFunctionInstanceList:
								if fold.name == fnew.name:
									finalNewFunctionList.append(fnew)
									flag = 1
									break
							if not flag:
								finalNewFunctionList.append(dummyFunction)

						print finalOldFunctionList
						print finalNewFunctionList

							# if indexHashOld == "1e25854":
							# 	sys.exit()

								# if offset >= f.lines[0] and bound <= f.lines[1]:
								# 	print "\t\t\tFOUND:", f.name, f.lines

							# print "--------chunkLine----------"
							# print chunk
							# print "--------------------------"

							# """
							# NOTE, JUL 20
							# Before other checks, do 'chunk effect check'.
							# compare oldChunk vs newChunk, both of which don't include comments.
							# If two chunks (as strings) are identical, skip that chunk.
							# """
							# oldChunk = ""
							# newChunk = ""
							# for chunkLine in chunk.split('\n'):
							# 	l = chunkLine.replace(' ', '').replace('\t', '')
							# 	if l.startswith('+'):
							# 		if l[1:].startswith('/*') or l[1:].startswith('*') or l[1:].startswith('*/'):
							# 			pass
							# 		else:
							# 			newChunk += l[1:]
							# 	elif l.startswith('-'):
							# 		if l[1:].startswith('/*') or l[1:].startswith('*') or l[1:].startswith('*/'):
							# 			pass
							# 		else:
							# 			oldChunk += l[1:]
							# 	else:
							# 		newChunk += l
							# 		oldChunk += l

							# if oldChunk == newChunk:
							# 	print "\t [-] (Chunk without impact)"
							# 	continue	# jump to the next chunk

							# preprocessedChunk = cparser.preprocess_func_reconst(chunk.split('\n'))
							# preprocessedChunkLinesList = preprocessedChunk.split('\n')[1:]
							# # print "-=-=-=-=-prep=-=-=-=-=-="
							# # print preprocessedChunk
							# # print "-=-=-=-=-=-=-=-=-=-="

							# """
							# NOTE, MAY 17
							# Before doing everything else, first check if the patch only modifies comments.
							# If so, discard the chunk, or we end up detecting irrelevant function (false positive)
							# commentcnt would be greater than 0 when preprocessed diff (which will not have a comment) fixes something.
							
							# [MAY 17 version]
							# commentcnt = 0
							# for preprocessedChunkLine in preprocessedChunkLinesList:
							# 	pl = preprocessedChunkLine.lstrip()
							# 	if pl.startswith('+') or pl.startswith('-'):
							# 		commentcnt += 1
							# """
							# """
							# NOTE, JUL 20
							# A few changes had to be made, to fully implement the things the comment above refers to.
							# We must notice that cparser.preprocess_func_reconst does not exterminate the comments.
							# It leaves the prefix (+ or -), and broken comments are not addressed at all.
							# Thus, to check if the patch only modifies comments,
							# I had to count the lines (w/o whitespace and longer than 2) that don't start with +/*, +*, +*/, -/*, -*, -*/
							# Such lines are the lines that actually change the code.
							# The previous version is moved into the upper comment.
							# """
							# commentcnt = 0
							# for preprocessedChunkLine in preprocessedChunkLinesList:
							# 	normalizedChunkLine = ''.join(preprocessedChunkLine.replace('\t', '').lstrip().split(' '))
							# 	if normalizedChunkLine.startswith('+') or normalizedChunkLine.startswith('-'):
							# 		n = normalizedChunkLine[1:]
							# 		if n.startswith('/*') or n.startswith('*') or n.startswith('*/'):
							# 			pass
							# 		else:
							# 			commentcnt += 1

							# if commentcnt == 0:
							# 	print "\t [-] (comment only chunk)"
							# 	continue	# jump to next chunk

							# # else:	# only if the patch fixes lines other than comments,
							# oldLineList = []
							# oldLineLenSummed = 0
							# # print "\t [+] Proceed"
							# for chunkLine in preprocessedChunkLinesList:	# chunkLine is a line in the chunk
							# 	""" NOTE, MAY 13
							# 	select the lines to search in the list of function bodies of the source code.
							# 	Exclusion rules include lines that
							# 		1. length < 3 (e.g., line that only has closing parenthesis)
							# 		2. start with + (lines for new code)
							# 		3. start with /*, *, */ (possibly comments)
							# 		4. start with # (#define case)
							# 		5. WHAT IF WE EXCLUDE THE FUNCTION HEADERS???!?!?!?!?!?!?!?! - NOT APPLIED YET (MAY 13).

							# 		NOTE, JULY 29
							# 	Add one more exclusion rule:
							# 	start with // (inlined comments)
							# 	"""
							# 	if len(chunkLine.replace(' ', '').replace('\t', '')) > 2:
							# 		if chunkLine.startswith('+'):
							# 			pass
							# 		elif len(chunkLine[1:].strip()) > 1:
							# 			line = chunkLine
							# 			ll = line.lstrip()
							# 			if ll.startswith('*') or ll.startswith('*/') or ll.startswith('/*') or ll.startswith('#') or ll.startswith('//'):
							# 				pass	# exclude the comment lines
							# 			else:
							# 				oldLineList.append(chunkLine[1:].lstrip())	# this oldLineList should have all the old lines
							# 				oldLineLenSummed += len(chunkLine[1:].lstrip())

							# preprocessedsrc = cparser.preprocess_func_reconst(srclines)
							# if len(oldLineList) < 2:	# if a chunk contains less than two old lines, discard that chunk.
							# 	print '\t [-] (less than 2 old lines)'
							# elif oldLineLenSummed < 30:	# for accuracy, if the sum of length of old lines is below a threshold, discard that chunk.
							# 	print '\t [-] (sum of oldlines shorter than 30)'
							# else:
							# 	(funcdeflist, funcbodylist, funcbodyrawlist) = cparser.parse_function(preprocessedsrc, 0)

							# 	matchFlag = 0
							# 	for fi, f in enumerate(funcbodyrawlist):
							# 		# search for the vulnerable function
							# 		matchcnt = 0
							# 		for l in oldLineList:
							# 			if l in f:
							# 				matchcnt += 1
							# 		if matchcnt > 0 and matchcnt == len(oldLineList):
							# 			matchFlag = 1

							# 			if len(cveId) > 14:
							# 				cveId = cveId.split('_')[0]

							# 			cvss = "0.0"
							# 			try:
							# 				cvss = cveDict[cveId][0]
							# 			except:
							# 				pass

							# 			if cvss == "":
							# 				cvss = "0.0"

							# 			cwe = "CWE-000"
							# 			try:
							# 				cwe = cveDict[cveId][1]
							# 			except:
							# 				pass

							# 			if cwe == "":
							# 				cwe = "CWE-000"
							# 			elif len(cwe) < 7:
							# 				cwesplitted = cwe.split('-')
							# 				cwenum = cwesplitted[1]
							# 				cwenum = cwenum.zfill(3)
							# 				cwe = str(cwesplitted[0]) + '-' + str(cwenum)

							# 			# """ okay now if you uncomment this and replace prints with fp.write then everything's done. leaving that, i'll go get some fucking sleep."""
							# 			saveFileName = cveId + '_' + cvss + '_' + cwe + '_' + commitHashValue + '_' + srcFileName + '_' +  str(fi) + '.vul'
							# 			print '\t [+] Saving', saveFileName
										
							# 			with open(os.path.join(originalDir, "vul", repoName, saveFileName), 'w') as fp:
							# 				fp.write(funcdeflist[fi] + '\n{\n' + f + '\n}\n')
							# 			# os.chdir(curdir)
							# 			# print "\nHERE:", os.getcwd()
							# 			# resultList.append(saveFileName)

							# 			# break when you find the matching vulnerable function.
							# 			break
									
							# 	# if program did not break from the previous for loop,
							# 	if fi+1 == len(funcbodyrawlist):
							# 		print '\t [-] (no matched function)'

						# os.chdir(originalDir)

print ""
print "Done getting vulnerable functions from", repoName
print "Reconstructed", len(os.listdir(os.path.join(originalDir, 'vul', repoName))), "vulnerable functions from", diffFileCnt, "patches."