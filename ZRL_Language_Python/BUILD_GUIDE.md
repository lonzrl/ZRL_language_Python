# ZRL 打包说明

## 打包前准备

1. 确保已安装PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 确保图标文件存在：
   - `icons/icon.ico` - 程序图标
   - `icons/fileicon.ico` - .z文件图标

## 打包步骤

### 1. 使用PyInstaller打包

```bash
pyinstaller ZRL.spec
```

这将根据ZRL.spec文件的配置进行打包。

### 2. 打包后的文件结构

打包完成后，在`dist/ZRL`目录下会生成以下文件：

```
dist/ZRL/
├── ZRL.exe              # 主程序
├── fileicon.ico         # .z文件图标
├── _internal/           # 内部依赖文件
│   ├── python311.dll
│   ├── ...
│   └── icons/
│       ├── icon.ico
│       └── fileicon.ico
└── 其他依赖文件...
```

### 3. 配置文件关联

打包完成后，需要以管理员身份运行ZRL.exe来注册文件关联：

```bash
# 以管理员身份运行
ZRL.exe --register
```

这将：
- 注册.z文件类型
- 设置fileicon.ico为.z文件的图标
- 配置双击.z文件用ZRL.exe打开
- 添加右键菜单（打开、编辑）

### 4. 取消文件关联

如需取消文件关联：

```bash
# 以管理员身份运行
ZRL.exe --unregister
```

## 打包配置说明

### ZRL.spec 文件说明

```python
# 数据文件
datas=[
    ('icons/*', 'icons/'),      # 包含所有图标文件
    ('fileicon.ico', '.'),      # 将fileicon.ico复制到根目录
],

# 隐藏导入
hiddenimports=[
    'turtle',                   # 绘图模块
    'tkinter',                  # GUI模块
    'pickle',                   # 序列化
    'argparse',                 # 命令行参数
    'readline',                 # 命令历史
    'math',                     # 数学函数
    'time',                     # 时间函数
    'random',                   # 随机数
    'datetime',                 # 日期时间
    'shutil',                   # 文件操作
    'json',                     # JSON处理
    'base64',                   # Base64编码
    'urllib.request',           # HTTP请求
    'urllib.parse',             # URL解析
    'tempfile',                 # 临时文件
    'subprocess',               # 子进程
    'psutil',                   # 进程管理
],

# 程序配置
exe = EXE(
    ...
    icon='icons/icon.ico',      # 程序图标
    console=True,               # 显示控制台窗口
    ...
)
```

## 分发建议

### 1. 创建安装包

推荐使用NSIS或Inno Setup创建安装程序，可以：
- 复制文件到Program Files
- 注册文件关联
- 创建桌面快捷方式
- 添加到开始菜单
- 配置卸载程序

### 2. 简单分发

如果不需要安装程序，可以：
1. 将`dist/ZRL`目录打包为ZIP
2. 提供用户解压后运行`ZRL.exe --register`的说明
3. 或者提供批处理脚本自动注册

### 3. 便携版

创建便携版本：
1. 将所有文件打包到单个目录
2. 不注册文件关联
3. 提供用户手动配置的说明

## 常见问题

### Q1: 打包后运行出现模块缺失错误

**A**: 检查ZRL.spec中的hiddenimports是否包含所有需要的模块。

### Q2: 打包后文件关联不工作

**A**: 
1. 确保以管理员身份运行
2. 检查fileicon.ico文件是否在正确位置
3. 查看Windows注册表中是否正确注册

### Q3: 打包后文件过大

**A**: 
1. 使用UPX压缩（已在spec中启用）
2. 排除不需要的模块
3. 使用虚拟环境打包，只包含必要的依赖

### Q4: 中文显示乱码

**A**: ZRL已内置UTF-8支持，确保：
1. 源文件使用UTF-8编码
2. 控制台支持UTF-8（Windows 10+默认支持）

### Q5: 图标不显示

**A**:
1. 清除Windows图标缓存：删除`%localappdata%\IconCache.db`
2. 重启资源管理器或重启电脑
3. 确保图标文件格式正确（.ico，支持多种尺寸）

## 测试清单

打包完成后，请测试以下功能：

- [ ] 运行ZRL.exe显示版本信息
- [ ] 运行简单的.z文件
- [ ] 启动REPL交互模式
- [ ] 测试help命令
- [ ] 测试info命令
- [ ] 注册文件关联
- [ ] 双击.z文件运行
- [ ] 右键.z文件编辑
- [ ] 查看文件图标
- [ ] 测试所有内置函数
- [ ] 测试绘图功能
- [ ] 测试GUI功能
- [ ] 测试HTTP请求
- [ ] 测试文件操作
- [ ] 测试JSON/Base64

## 版本信息

- 当前版本: v1.1.0
- Python版本: 3.11+
- 平台: Windows