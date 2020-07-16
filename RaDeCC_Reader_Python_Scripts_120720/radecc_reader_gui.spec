# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/seanselzer/Documents/GitHub/RaDeCC_Reader/RaDeCC_Reader_Python_Scripts_120720/radecc_reader_gui.py'],
             pathex=['/Users/seanselzer/Desktop/Executables'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn', '_sysconfigdata_x86_64_apple_darwin13_4_0','scipy.special.cython_special'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('v', None, 'OPTION')],
          name='radecc_reader_gui_MacOS_v2_0-beta2',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
