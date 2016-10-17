# -*- mode: python -*-

block_cipher = None


a = Analysis(['hashmarker-2.py'],
             pathex=['C:\\Users\\Squizz-CCS\\Desktop\\hashmarker'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
a.datas += [('hashmarker_icon.gif', 'C:\\Users\\Squizz-CCS\\Desktop\\hashmarker\\hashmarker_icon.gif', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='HashMarker_2.0_Win_x64',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='hashmarker_icon.ico')
