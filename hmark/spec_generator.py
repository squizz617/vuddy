import os
import platform

pf = platform.platform()
if 'Windows' in pf:
	osName = 'Win'
elif 'Linux' in pf:
	osName = 'Linux'
else:
	osName = 'OSX'

bits, _ = platform.architecture()
if '64' in bits:
	bits = 'x64'
else:
	bits = 'x86'

if osName == 'OSX':
	bits = ''

with open("version", "r") as fp:
	version = fp.readline()

fp = open("HMark_" + version + '_' + osName + '_' + bits + ".spec", "w")
cwd = os.getcwd()
if osName == "Linux":
	fp.write("\
# -*- mode: python -*-\n\
block_cipher = None\n\
a = Analysis(['hmark.py'],\n\
             pathex=['" + cwd + "'],\n\
             binaries=None,\n\
             datas=None,\n\
             hiddenimports=[],\n\
             hookspath=[],\n\
             runtime_hooks=[],\n\
             excludes=[],\n\
             win_no_prefer_redirects=False,\n\
             win_private_assemblies=False,\n\
             cipher=block_cipher)\n\
a.datas += [('icon.gif', '" + os.path.join(cwd, 'icon.gif') + "', 'DATA')]\n\
a.datas += [('FuncParser.jar', '" + os.path.join(cwd, 'FuncParser.jar') + "', 'DATA')]\n\
a.datas += [('version', '" + os.path.join(cwd, 'version') + "', 'DATA')]\n\
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          exclude_binaries=True,\n\
          name='HMark_" + version + "_" + osName + "_" + bits + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True )\n\
coll = COLLECT(exe,\n\
               a.binaries,\n\
               a.zipfiles,\n\
               a.datas,\n\
               strip=False,\n\
               upx=True,\n\
               name='HMark_" + version + "_" + osName + "_" + bits + "',)\
""")

elif osName == "OSX":
		fp.write("\
	# -*- mode: python -*-\n\
	block_cipher = None\n\
	a = Analysis(['hmark.py'],\n\
	             pathex=['" + cwd + "'],\n\
	             binaries=None,\n\
	             datas=None,\n\
	             hiddenimports=[],\n\
	             hookspath=[],\n\
	             runtime_hooks=[],\n\
	             excludes=[],\n\
	             win_no_prefer_redirects=False,\n\
	             win_private_assemblies=False,\n\
	             cipher=block_cipher)\n\
	a.datas += [('icon.gif', '" + os.path.join(cwd, 'icon.gif') + "', 'DATA')]\n\
	a.datas += [('FuncParser.jar', '" + os.path.join(cwd, 'FuncParser.jar') + "', 'DATA')]\n\
	a.datas += [('version', '" + os.path.join(cwd, 'version') + "', 'DATA')]\n\
	pyz = PYZ(a.pure, a.zipped_data,\n\
	             cipher=block_cipher)\n\
	exe = EXE(pyz,\n\
	          a.scripts,\n\
	          a.binaries,\n\
	          a.zipfiles,\n\
	          a.datas,\n\
	          name='HMark_" + version + "_" + osName + "',\n\
	          debug=False,\n\
	          strip=False,\n\
	          upx=True,\n\
	          console=True )\n\
	""")

elif osName == "Win":
		fp.write("\
	# -*- mode: python -*-\n\
	block_cipher = None\n\
	a = Analysis(['hmark.py'],\n\
	             pathex=['" + cwd + "'],\n\
	             binaries=None,\n\
	             datas=None,\n\
	             hiddenimports=[],\n\
	             hookspath=None,\n\
	             runtime_hooks=None,\n\
	             excludes=None,\n\
	             win_no_prefer_redirects=None,\n\
	             win_private_assemblies=None,\n\
	             cipher=block_cipher)\n\
	a.datas += [('icon.gif', '" + os.path.join(cwd, 'icon.gif') + "', 'DATA')]\n\
	a.datas += [('FuncParser.jar', '" + os.path.join(cwd, 'FuncParser.jar') + "', 'DATA')]\n\
	a.datas += [('version', '" + os.path.join(cwd, 'version') + "', 'DATA')]\n\
	pyz = PYZ(a.pure, a.zipped_data,\n\
	             cipher=block_cipher)\n\
	exe = EXE(pyz,\n\
	          a.scripts,\n\
	          a.binaries,\n\
	          a.zipfiles,\n\
	          a.datas,\n\
	          name='HMark_" + version + "_" + osName + "_" + bits + "',\n\
	          debug=False,\n\
	          strip=None,\n\
	          upx=True,\n\
	          console=True,\n\
	          icon='icon.ico')\
	""")


fp.close()