# -*- mode: python -*-

block_cipher = None


a = Analysis(['dolphin_updater\\__main__.py'],
             pathex=['build'],
             binaries=None,
             datas=[('dolphin_updater\\7zr.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='DolphinUpdater',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='dolphin_updater\\icon\\Icon.ico')