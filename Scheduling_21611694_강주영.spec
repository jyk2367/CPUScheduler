# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Scheduling_21611694_강주영.py'],
             pathex=['C:\\Users\\admin\\OneDrive - 영남대학교\\대학교용\\2021\\21-1학기\\운영체제설계\\과제1\\끝\\최종'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Scheduling_21611694_강주영',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
