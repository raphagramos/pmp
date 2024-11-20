# app.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Coleta submódulos e arquivos de dados do MySQL Connector
hiddenimports = collect_submodules('mysql.connector')
datas = collect_data_files('mysql.connector')

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
...
