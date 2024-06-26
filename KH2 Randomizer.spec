# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


import os, glob, shutil, importlib, khbr

for root, dirs, files in os.walk(DISTPATH):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


khbrpath = os.path.dirname(khbr.__file__)
def build_datas_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      if os.path.isfile(filename):
        dest_dirname = os.path.dirname(filename)
        if dest_dirname == "":
          dest_dirname = "."
        
        data_entry = (filename, dest_dirname)
        datas.append(data_entry)
        print(data_entry)
  
  return datas

def external_data_recursive(paths):
  datas = []
  
  for path in paths:
    for filename in glob.iglob(path, recursive=True):
      if os.path.isfile(filename):
        dest_dirname = os.path.dirname(filename)
        if dest_dirname == "":
          dest_dirname = "."
        else:
          dest_dirname = dest_dirname.split("site-packages\\")[1]
        
        data_entry = (filename, dest_dirname)
        datas.append(data_entry)
        print(data_entry)
  
  return datas


updater_analysis = Analysis(
    ['updater.py'],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'Module/icon.png',
       ]),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(updater_analysis.pure, updater_analysis.zipped_data, cipher=block_cipher)

updater_exe = EXE(
    pyz,
    updater_analysis.scripts,
    updater_analysis.binaries,
    updater_analysis.zipfiles,
    updater_analysis.datas,
    [],
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rando.ico'
)

a = Analysis(
    ['localUI.py'],
    pathex=[],
    binaries=[('{0}/updater.exe'.format(DISTPATH),".")],
    datas=build_datas_recursive([
        'UI/**/*.*',
        'UI/*.*',
        'static/**/*.*',
        'static/*.*',
        'presets/*.*',
        'Module/icon.png',
        'extracted_data.zip'
       ]) + external_data_recursive([khbrpath+"/**/*"]),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

rando_pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    rando_pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KH2 Randomizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='rando.ico'
)

#presetPath = '{0}/presets'.format(DISTPATH)
#if os.path.exists(presetPath):
#  shutil.rmtree(presetPath)

#shutil.copytree('presets', presetPath)

#shutil.make_archive('Kingdom Hearts II Final Mix Randomizer', 'zip', DISTPATH)
