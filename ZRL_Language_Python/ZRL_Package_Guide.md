# ZRL 编程语言：Windows 单文件打包教程

为了让您的 ZRL 语言拥有类似 Python 的单个 `ZRL.exe` 运行环境，我们使用 **PyInstaller** 进行打包。

## 1. 打包配置文件 (ZRL.spec)

以下是为您准备好的 `ZRL.spec` 配置文件。它会自动包含所有核心模块、标准库以及图标资源。

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ZRL.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('zrl_lexer.py', '.'),
        ('zrl_parser.py', '.'),
        ('zrl_interpreter.py', '.'),
        ('zrl_stdlib.py', '.'),
        ('icons/*', 'icons/'),
    ],
    hiddenimports=['turtle', 'tkinter', 'pickle', 'argparse'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ZRL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico',  # 设置 ZRL.exe 的程序图标
)
```

## 2. Windows 环境打包步骤

请在您的 Windows 电脑上按照以下步骤操作：

### 第一步：安装依赖
打开 PowerShell 或 CMD，执行：
```bash
pip install pyinstaller pillow
```

### 第二步：准备文件
确保您的文件夹结构如下：
```text
/your_project/
├── ZRL.py
├── zrl_lexer.py
├── zrl_parser.py
├── zrl_interpreter.py
├── zrl_stdlib.py
├── ZRL.spec
└── icons/
    ├── icon.ico
    └── fileicon.ico
```

### 第三步：执行打包命令
在项目根目录下运行：
```bash
pyinstaller ZRL.spec
```

### 第四步：获取结果
打包完成后，您可以在 `dist/` 目录下找到生成的 **`ZRL.exe`**。

---

## 3. ZRL 语言使用指南

### 3.1 命令行运行
```bash
ZRL.exe test.z
```

### 3.2 交互模式 (REPL)
直接运行 `ZRL.exe` 即可进入交互式环境：
```text
ZRL (Zero-effort Rapid Language) v1.0.0
zrl > var x = 10
zrl > print(x * 2)
20
```

### 3.3 预编译字节码
将源代码编译为 `.zxx` 以提高加载速度：
```bash
ZRL.exe -c main.z -o main.zxx
ZRL.exe main.zxx
```

### 3.4 文件关联 (可选)
您可以将 `.z`, `.zs`, `.zxx` 文件关联到 `ZRL.exe`，并使用 `icons/fileicon.ico` 作为它们的图标，这样双击脚本即可直接运行。
