
def get_cpu_count():
	try:
		import multiprocessing
		return multiprocessing.cpu_count()
	except (ImportError, NotImplementedError):
		pass
	
	# http://code.google.com/p/psutil/
	try:
		import psutil
		return psutil.cpu_count() #psutil.NUM_CPUS on old versions
	except (ImportError, AttributeError):
		pass
	
	return 1
