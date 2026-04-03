# ZRL_language
# ZRL (Zero-effort Rapid Language)

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows-green.svg)

**一种专为 Windows 平台设计的简洁易用的解释型编程语言**

[快速开始](#快速开始) • [特性](#特性) • [文档](#文档) • [示例](#示例)

</div>

---

## 关于 ZRL

ZRL (Zero-effort Rapid Language) 是一种现代化的解释型编程语言，旨在为 Windows 平台提供类似 Python 的简洁性和易用性，同时内置图形绘制、GUI 窗口和系统操作等强大功能。

### 设计理念

- **简洁易读**：借鉴 Python 的设计理念，追求代码的简洁性和可读性
- **功能丰富**：内置对图形、GUI 和系统操作的支持，简化常见应用开发
- **模块化**：支持模块导入和预编译，方便代码复用和项目管理
- **跨文件调用**：轻松组织和管理大型项目

---

## 特性

### 语言特性

- ✅ 简洁直观的语法，类似 Python
- ✅ 完整的面向对象编程支持（类、继承、方法）
- ✅ 强大的控制流语句（if/elif/else, for, while）
- ✅ 函数定义与调用
- ✅ 模块导入系统（import/from）
- ✅ 异常处理（try/except/finally）
- ✅ 变量与常量声明
- ✅ 列表、字典等数据结构

### 内置功能

- 🎨 **绘图模块** (painter)：类似 Python turtle，轻松创建图形
- 🖼️ **GUI 窗口** (window)：创建桌面应用程序界面
- ⚙️ **系统操作** (os)：文件管理、进程控制等系统功能
- 📝 **文本处理**：字符串操作、JSON、Base64 编码
- 🔢 **数学运算**：完整的数学函数库
- 🌐 **网络请求**：HTTP 请求支持

### 开发工具

- 📦 预编译支持（.zxx 字节码格式）
- 🔄 交互式 REPL 环境
- 🎯 语法检查工具
- 📊 AST 可视化
- 🖥️ 图形化终端（支持中文显示）
- 📝 IDE 集成开发环境
- 🔗 文件关联（双击运行、自定义图标）

---

## 快速开始

### 安装

#### 从源码运行

```bash
# 克隆或下载项目
git clone https://github.com/lonzrl/ZRL_language_Python
cd ZRL_Language_Python

# 运行 ZRL
python ZRL.py
```

#### 打包为 EXE

使用 PyInstaller 打包为单文件可执行程序：

```bash
# 安装依赖
pip install pyinstaller

# 执行打包
pyinstaller ZRL.spec

# 打包后的文件在 dist/ZRL.exe
```

详细打包说明请参考 [BUILD_GUIDE.md](BUILD_GUIDE.md)

### 基本使用

#### 1. 交互式 REPL

```bash
python ZRL.py
# 或
ZRL.exe
```

```
ZRL (Zero-effort Rapid Language) v1.1.0
zrl > var name = "世界"
zrl > print("你好, " + name)
你好, 世界
zrl >
```

#### 2. 运行脚本文件

```bash
python ZRL.py program.z
# 或
ZRL.exe program.z
```

#### 3. 编译为字节码

```bash
python ZRL.py -c program.z -o program.zxx
python ZRL.py program.zxx
```

#### 4. 语法检查

```bash
python ZRL.py --check program.z
```

#### 5. 查看版本信息

```bash
python ZRL.py --version
python ZRL.py --info
```

---

## 文件扩展名

ZRL 支持以下文件扩展名：

- `.z` - ZRL 源代码文件（推荐）
- `.zs` - ZRL 源代码文件（备用）
- `.zxx` - ZRL 预编译字节码文件

---

## 核心模块

### painter - 绘图模块

```zrl
import painter

painter.init(800, 600)
painter.pen_color("red")
painter.circle(50)
painter.done()
```

### window - GUI 窗口模块

```zrl
import window

var win = window.create("我的应用", 400, 300)
var label = window.label(win, "Hello ZRL!")
window.run(win)
```

### os - 系统操作模块

```zrl
import os

print("当前目录:", os.current_dir())
var files = os.list_dir(".")
for file in files:
    print(file)
```

---

## 命令行参数

```
用法: python ZRL.py [选项] [文件]

选项:
  file                  要运行的 ZRL 文件
  -c, --compile FILE    编译 .z 或 .zs 文件为 .zxx 格式
  -o, --output FILE     指定编译输出文件名
  -v, --version         显示版本信息
  --check FILE          检查语法而不执行
  --ast FILE            显示 AST 而不执行
  --info                显示语言信息和快速入门指南
  --register            注册 .z 文件类型关联（需要管理员权限）
  --unregister          取消 .z 文件类型关联（需要管理员权限）
  --terminal            启动图形化 GUI 终端（支持中文显示）
  --ide                 启动 ZRL IDE 集成开发环境
```

---

## 代码示例

### 基础语法

```zrl
# 变量与常量
var name = "张三"
var age = 25
const PI = 3.14159

# 条件语句
if age >= 18:
    print("成年人")
else:
    print("未成年人")

# 循环
for i in range(5):
    print(i)

while age > 0:
    age = age - 1

# 函数定义
func greet(name):
    print("你好, " + name + "!")

greet("小明")
```

### 面向对象

```zrl
class Person:
    func init(name, age):
        self.name = name
        self.age = age
    
    func greet():
        print("我是" + self.name)

var person = Person("王五", 25)
person.greet()
```

### 异常处理

```zrl
try:
    var result = 10 / 0
except:
    print("捕获到除零错误")
finally:
    print("finally 块总是执行")
```

### 模块导入

```zrl
import painter
import window
import os

painter.init(800, 600)
painter.circle(50)
painter.done()
```

更多示例请查看项目中的 `test_*.z` 文件。

---

## 项目结构

```
ZRL_Language_Python/
├── ZRL.py                  # 主程序入口
├── zrl_lexer.py            # 词法分析器
├── zrl_parser.py           # 语法分析器
├── zrl_interpreter.py      # 解释器
├── zrl_stdlib.py           # 标准库
├── zrl_terminal.py         # 图形化终端
├── ZRL.spec                # PyInstaller 打包配置
├── icons/                  # 图标资源
│   ├── icon.ico
│   └── fileicon.ico
├── test_*.z                # 测试文件
├── BUILD_GUIDE.md          # 构建指南
├── ZRL_Syntax_Specification.md  # 语法规范
└── ZRL_Package_Guide.md    # 打包说明
```

---

## 文件关联

ZRL 支持将 `.z` 文件关联到程序，实现双击运行：

### 注册文件关联

```bash
# 以管理员身份运行
python ZRL.py --register
# 或
ZRL.exe --register
```

这将：
- 注册 `.z` 文件类型
- 设置自定义图标
- 配置双击运行
- 添加右键菜单（打开、编辑）

### 取消文件关联

```bash
# 以管理员身份运行
python ZRL.py --unregister
# 或
ZRL.exe --unregister
```

---

## 开发与贡献

### 开发环境要求

- Python 3.11+
- Windows 操作系统

### 运行测试

```bash
# 运行基础测试
python ZRL.py test_basic.z

# 运行高级功能测试
python ZRL.py test_advanced.z

# 运行类测试
python ZRL.py test_class.z
```

---

## 版本历史

### v1.1.0 (当前版本)

- ✨ 完整的面向对象编程支持
- ✨ 图形化终端（支持中文显示）
- ✨ 文件关联功能
- ✨ 预编译字节码支持
- ✨ 异常处理机制
- ✨ 模块导入系统
- 🎨 绘图模块
- 🖼️ GUI 窗口模块
- ⚙️ 系统操作模块

---

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

## 联系方式

- 项目主页：[GitHub](https://github.com/lonzrl/ZRL_language_Python)
- 问题反馈：[Issues](https://github.com/lonzrl/ZRL_language_Python/issues)

---

## 致谢

感谢所有为 ZRL 语言做出贡献的开发者！
- ZRLzuoruilang(B站)
- lonzrl(github)

---

<div align="center">

**用 ZRL，让编程更简单！** 🚀

</div>
