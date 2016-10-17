# -*- mode: python -*-

block_cipher = None


a = Analysis(['hashmarker-2.py'],
             pathex=['/Users/Jaesang/Desktop/hashmarker'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('hashmarker_icon.gif', '/Users/Jaesang/Desktop/hashmarker/hashmarker_icon.gif', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='HashMarker_2.0_OSX',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='hashmarker_icon.ico')
