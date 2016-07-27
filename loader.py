import os

def load(root):
	walklist = os.walk(root)
	filelist = []
	for path, dirs, files in walklist:
		for f in files:
			if f.endswith('.c') or f.endswith('.cpp') or f.endswith('.cc'):
				full = path.replace('\\', '/') + '/' + f
				if os.path.getsize(full) < 2097152:
					filelist.append(full)
	return filelist

