# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['src/chartranshandler.py', 'src/configutil.py', 'src/filetranshandler.py', 'src/ipchandler.py', 'src/logfilehandler.py', 'src/mainwindowhandler.py', 'src/newconnecthandler.py', 'src/openconnecthandler.py', 'src/serialprocess.py', 'ui/mainwindow.py', 'ui/newconnect.py', 'ui/openconnect.py', 'D:\\00_personal\\py_lesson\\myCmdParser\\serialtool\\py_serialtool'],
             binaries=[],
             datas=[],
             hiddenimports=['configparser', 'mainwindowhandler', 'src.mainwindowhandler', 'serial', 'serial.tools.list_ports', 'tkinter.messagebox', 'numpy', 'codecs', 'yaml', 'src.chartranshandler', 'src.configutil', 'src.filetranshandler', 'yaml', 'yaml', 'src.ipchandler', 'src.logfilehandler', 'src.newconnecthandler', 'src.openconnecthandler', 'src.serialprocess', 'ui.mainwindow', 'ui.newconnect', 'ui.openconnect'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='res\\crack.ico')
