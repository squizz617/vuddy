import os
import platform
import version

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

version = version.version

fp = open("HMark_" + version + '_' + osName + '_' + bits + ".spec", "w")
cwd = os.getcwd()
if osName == "Linux":
	fp.write("\
# -*- mode: python -*-\n\n\
block_cipher = None\n\n\n\
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
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          a.binaries,\n\
          a.zipfiles,\n\
          a.datas,\n\
          name='HMark_" + version + "_" + osName + "_" + bits + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True )\n\
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
# -*- mode: python -*-\n\n\
block_cipher = None\n\n\n\
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
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          a.binaries,\n\
          a.zipfiles,\n\
          a.datas,\n\
          name='HMark_" + version + "_" + osName + "_" + bits + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True,\n\
          icon='icon.ico')\
""")


fp.close()