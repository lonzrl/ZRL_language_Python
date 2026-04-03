# ZRL 文件关联说明

## 功能说明

ZRL现在支持将.z文件与ZRL解释器关联，使.z文件在Windows文件资源管理器中显示专用图标，并可以双击直接运行。

## 使用方法

### 开发环境

1. 运行文件关联注册工具（需要管理员权限）：
   ```bash
   python register_filetype.py --register
   ```
   或双击 `register_zrl_files.bat` 文件

2. 取消注册：
   ```bash
   python register_filetype.py --unregister
   ```
   或双击 `unregister_zrl_files.bat` 文件

### 打包后

1. 将ZRL打包后，在dist/ZRL目录下运行：
   ```bash
   ZRL.exe --register
   ```

2. 取消注册：
   ```bash
   ZRL.exe --unregister
   ```

## 文件图标说明

- **程序图标**：`icons/icon.ico` - ZRL解释器主程序图标
- **文件图标**：`icons/fileicon.ico` - .z源代码文件图标（在文件资源管理器中显示）

## 注册后的功能

注册.z文件类型后，您可以：

1. **双击运行**：双击.z文件直接用ZRL解释器运行
2. **右键菜单**：右键.z文件可以看到"打开"和"编辑"选项
   - 打开：用ZRL解释器运行
   - 编辑：用记事本打开
3. **专用图标**：.z文件在文件资源管理器中显示专用图标
4. **文件类型描述**：鼠标悬停在.z文件上显示"ZRL源代码文件"

## 注意事项

- 注册文件类型需要管理员权限
- 如果打包后使用，确保fileicon.ico文件在可执行文件同目录下
- 取消注册也需要管理员权限
- 注册信息存储在Windows注册表的HKEY_CLASSES_ROOT中

## 手动注册（高级用户）

如果您想手动注册，可以修改Windows注册表：

1. 打开注册表编辑器（regedit）
2. 导航到 HKEY_CLASSES_ROOT
3. 创建或修改以下项：

```
.z (默认值) = ZRLFile

ZRLFile (默认值) = ZRL源代码文件
  └─ DefaultIcon (默认值) = fileicon.ico的完整路径,0
  └─ shell
     ├─ open
     │   └─ command (默认值) = "ZRL.exe的完整路径" "%1"
     └─ edit
         └─ command (默认值) = notepad "%1"
```

## 故障排除

**问题1：图标不显示**
- 确保fileicon.ico文件存在于正确位置
- 尝试清除Windows图标缓存：
  1. 删除 %localappdata%\IconCache.db
  2. 重启资源管理器或重启电脑

**问题2：双击文件无反应**
- 检查可执行文件路径是否正确
- 确保ZRL.exe有执行权限
- 尝试右键"打开"查看是否有错误信息

**问题3：注册失败**
- 确保以管理员身份运行注册工具
- 检查是否有安全软件阻止注册表修改
- 尝试手动注册（见上）