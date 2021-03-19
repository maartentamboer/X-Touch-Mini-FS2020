# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
import SimConnect
simconnect_root = os.path.dirname(SimConnect.__file__)

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\maart\\Documents\\dev\\X-Touch-Mini-FS2020'],
             binaries=[(f"{simconnect_root}/SimConnect.dll", 'SimConnect')],
             datas=[("Configurations/", "Configurations"), ("X-Touch-Editor-Configs/", "X-Touch-Editor-Configs")],
             hiddenimports=["rtmidi", "mido.backends.rtmidi"],
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
          [],
          exclude_binaries=True,
          name='X-Touch-Mini-FS2020',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='icon/airplane.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='X-Touch-Mini-FS2020')

print(Path.cwd())

simconnect_dll_rename = f"{DISTPATH}/X-Touch-Mini-FS2020/SimConnect/Simconnect.dll"
print(simconnect_dll_rename)

# Fix for simconnect getting the dll name by running _library_path = os.path.abspath(__file__).replace(".py", ".dll")
# this ends up in simconnect expecting simconnect.dllc
os.rename(simconnect_dll_rename, f"{simconnect_dll_rename}c")