import os
import platform
import version

pf = platform.platform()
if 'Windows' in pf:
    osName = 'win'
elif 'Linux' in pf:
    osName = 'linux'
else:
    osName = 'osx'

# bits, _ = platform.architecture()
# if '64' in bits:
# 	bits = 'x64'
# else:
# 	bits = 'x86'

# if osName == 'OSX':
# 	bits = ''

version = version.version

fp = open("hmark_" + version + '_' + osName + ".spec", "w")
cwd = os.getcwd()
if osName == "linux":
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
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          a.binaries,\n\
          a.zipfiles,\n\
          a.datas,\n\
          name='hmark_" + version + "_" + osName + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True )\n\
""")

elif osName == "osx":
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
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          a.binaries,\n\
          a.zipfiles,\n\
          a.datas,\n\
          name='hmark_" + version + "_" + osName + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True )\n\
""")

elif osName == "win":
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
pyz = PYZ(a.pure, a.zipped_data,\n\
             cipher=block_cipher)\n\
exe = EXE(pyz,\n\
          a.scripts,\n\
          a.binaries,\n\
          a.zipfiles,\n\
          a.datas,\n\
          name='hmark_" + version + "_" + osName + "',\n\
          debug=False,\n\
          strip=False,\n\
          upx=True,\n\
          console=True,\n\
          icon='icon.ico')\
""")

fp.close()
print "Pyinstaller spec file generated: " + "hmark_" + version + '_' + osName + ".spec"
