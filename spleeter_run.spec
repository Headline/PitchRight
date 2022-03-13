# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['spleeter_run.py'],
             pathex=[],
             binaries=[],
             datas=[('pretrained_models/', 'pretrained_models/')],
             hiddenimports=['sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils', 'sklearn.neighbors._typedefs', 'sklearn.utils._cython_blas', 'sklearn.utils._weight_vector', 'sklearn.neighbors._quad_tree', 'sklearn.utils._typedefs', 'sklearn.neighbors._ball_tree', 'sklearn.neighbors._partition_nodes', 'spleeter.model.functions', 'spleeter.model.functions.unet'],
             hookspath=['extra-hooks'],
             hooksconfig={},
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
          name='spleeter_run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
