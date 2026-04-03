# ZRL 语言语法规范

## 1. 简介

ZRL (Zero-effort Rapid Language) 是一种专为 Windows 平台设计的解释型编程语言，旨在提供类似 Python 的简洁性和易用性，同时集成图形绘制、窗口操作和系统调用等功能。本规范详细定义了 ZRL 语言的词法、语法和核心语义。

## 2. 设计哲学

*   **简洁易读**：借鉴 Python 的设计理念，追求代码的简洁性和可读性。
*   **功能丰富**：内置对图形、GUI 和系统操作的支持，简化常见应用开发。
*   **跨文件调用**：支持模块化编程，方便代码复用和项目管理。
*   **解释执行**：提供类似 `.pyc` 的预编译 `.zxx` 格式，提高执行效率。

## 3. 词法规范

### 3.1 字符集

ZRL 源代码使用 Unicode (UTF-8) 字符集。

### 3.2 关键字

以下是 ZRL 的保留关键字，不能用作标识符：

| 关键字   | 描述         |
| :------- | :----------- |
| `if`     | 条件语句     |
| `else`   | 条件语句     |
| `elif`   | 条件语句     |
| `for`    | 循环语句     |
| `while`  | 循环语句     |
| `func`   | 函数定义     |
| `return` | 函数返回值   |
| `import` | 模块导入     |
| `as`     | 导入别名     |
| `from`   | 从模块导入   |
| `class`  | 类定义       |
| `self`   | 实例引用     |
| `true`   | 布尔真       |
| `false`  | 布尔假       |
| `null`   | 空值         |
| `var`    | 变量声明     |
| `const`  | 常量声明     |
| `and`    | 逻辑与       |
| `or`     | 逻辑或       |
| `not`    | 逻辑非       |
| `in`     | 成员运算     |
| `try`    | 异常处理     |
| `except` | 异常捕获     |
| `finally`| 异常最终块   |
| `raise`  | 抛出异常     |

### 3.3 标识符

标识符用于命名变量、函数、类等。必须以字母（a-z, A-Z）或下划线（_）开头，后续可包含字母、数字（0-9）或下划线。

### 3.4 字面量

*   **整数**：十进制整数，如 `123`, `0`, `-45`。
*   **浮点数**：包含小数点的数字，如 `3.14`, `-0.5`, `1.0`。
*   **字符串**：使用双引号 `"` 或单引号 `'` 包裹的字符序列，支持转义字符（如 `\n`, `\t`）。
*   **布尔值**：`true`, `false`。
*   **空值**：`null`。

### 3.5 运算符

| 类型     | 运算符                               |
| :------- | :----------------------------------- |
| 算术     | `+`, `-`, `*`, `/`, `%`, `**` (幂) |
| 比较     | `==`, `!=`, `<`, `>`, `<=`, `>=`   |
| 逻辑     | `and`, `or`, `not`                   |
| 赋值     | `=`, `+=`, `-=`, `*=`, `/=`, `%=`   |
| 成员     | `in`                                 |

### 3.6 分隔符与标点符号

*   **括号**：`()`, `[]`, `{}`
*   **逗号**：`,`
*   **冒号**：`:`
*   **点号**：`.`
*   **分号**：`;` (可选，用于分隔同一行的多个语句)

### 3.7 注释

*   **单行注释**：以 `#` 开头，直到行尾。
*   **多行注释**：使用 `'''` 或 `"""` 包裹。

## 4. 语法规范 (BNF 范式简化表示)

### 4.1 程序结构

```bnf
<program> ::= { <statement> | <function_definition> | <class_definition> | <import_statement> }*
```

### 4.2 语句

```bnf
<statement> ::= <expression_statement>
              | <variable_declaration>
              | <assignment_statement>
              | <if_statement>
              | <for_statement>
              | <while_statement>
              | <return_statement>
              | <break_statement>
              | <continue_statement>
              | <print_statement>
              | <input_statement>
```

### 4.3 表达式

ZRL 支持常见的算术、比较、逻辑表达式。表达式的优先级遵循传统规则。

```bnf
<expression> ::= <assignment_expression>
               | <logical_or_expression>
               | ... (其他优先级表达式)
```

### 4.4 变量声明与赋值

```bnf
<variable_declaration> ::= ( `var` | `const` ) <identifier> [ `=` <expression> ]
<assignment_statement> ::= <identifier> <assignment_operator> <expression>
```

### 4.5 控制流

#### 4.5.1 条件语句

```bnf
<if_statement> ::= `if` <expression> `:` <block>
                 [ `elif` <expression> `:` <block> ]*
                 [ `else` `:` <block> ]
<block> ::= <indentation> { <statement> }*
```

ZRL 使用缩进来表示代码块，类似 Python。默认 4 个空格。

#### 4.5.2 循环语句

```bnf
<for_statement> ::= `for` <identifier> `in` <expression> `:` <block>
<while_statement> ::= `while` <expression> `:` <block>
```

### 4.6 函数

```bnf
<function_definition> ::= `func` <identifier> `(` [ <parameter_list> ] `)` `:` <block>
<parameter_list> ::= <identifier> { `,` <identifier> }*
<return_statement> ::= `return` [ <expression> ]
<function_call> ::= <identifier> `(` [ <argument_list> ] `)`
<argument_list> ::= <expression> { `,` <expression> }*
```

### 4.7 类与对象 (面向对象基础)

```bnf
<class_definition> ::= `class` <identifier> [ `(` <parent_class> `)` ] `:` <block>
<parent_class> ::= <identifier>
<method_definition> ::= `func` <identifier> `(` `self` [ `,` <parameter_list> ] `)` `:` <block>
<attribute_access> ::= <expression> `.` <identifier>
<method_call> ::= <expression> `.` <identifier> `(` [ <argument_list> ] `)`
```

### 4.8 模块导入

```bnf
<import_statement> ::= `import` <module_name> [ `as` <alias> ]
                     | `from` <module_name> `import` ( <identifier> | `*` ) [ `as` <alias> ]
<module_name> ::= <identifier> { `.` <identifier> }*
<alias> ::= <identifier>
```

ZRL 文件扩展名支持 `.z`, `.zxx`, `.zs`。导入时，解释器会按此顺序查找文件。

## 5. 内置函数与标准库

ZRL 将提供以下内置函数和标准库模块：

### 5.1 内置函数

*   `print(...)`: 输出到控制台。
*   `input(prompt)`: 从控制台读取输入。
*   `len(obj)`: 返回对象长度（字符串、列表等）。
*   `type(obj)`: 返回对象类型。

### 5.2 标准库模块

#### 5.2.1 `painter` 模块 (绘图)

提供类似 Python `turtle` 模块的简单绘图功能。

```zrl
import painter

painter.init(width=800, height=600) # 初始化画布
painter.pen_color("red")
painter.move_to(100, 100)
painter.line_to(200, 200)
painter.circle(50) # 画圆
painter.fill_color("blue")
painter.begin_fill()
painter.rectangle(50, 50, 100, 100)
painter.end_fill()
painter.done() # 保持窗口显示
```

#### 5.2.2 `window` 模块 (GUI 窗口)

提供类似 Python `tkinter` 的基本 GUI 窗口和控件功能。

```zrl
import window

var main_window = window.create("My ZRL App", 400, 300)
var label = window.label(main_window, "Hello ZRL!")
window.set_position(label, 50, 50)

func on_button_click():
    print("Button clicked!")

var button = window.button(main_window, "Click Me", on_button_click)
window.set_position(button, 50, 100)

window.run(main_window) # 运行事件循环
```

#### 5.2.3 `os` 模块 (系统调用)

提供操作系统相关的函数，如文件操作、进程管理等。

```zrl
import os

print(os.current_dir())
os.make_dir("new_folder")
var files = os.list_dir(".")
for file in files:
    print(file)

os.execute("notepad.exe") # 执行外部程序
```

## 6. 预编译与执行

ZRL 解释器将支持直接执行 `.z`、`.zs` 源代码文件。同时，为了提高加载速度，将提供将源代码预编译为 `.zxx` 字节码文件的功能。`.zxx` 文件可以直接由解释器执行，类似于 Python 的 `.pyc` 文件。

## 7. 文件扩展名

ZRL 语言支持以下文件扩展名：

*   `.z`: ZRL 源代码文件 (推荐)
*   `.zs`: ZRL 源代码文件 (备用)
*   `.zxx`: ZRL 预编译字节码文件

## 8. 错误处理

ZRL 将提供清晰的错误消息，包括语法错误、运行时错误等，帮助开发者快速定位问题。

## 9. 总结

本规范为 ZRL 语言的实现提供了基础。通过遵循这些设计原则和语法规则，我们将构建一个功能强大、易于使用的编程语言环境。

## 10. 示例代码

### 10.1 基础语法示例

#### 变量与数据类型

```zrl
# 变量声明
var name = "张三"
var age = 25
var height = 1.75
var is_student = true

# 常量声明
const PI = 3.14159
const MAX_SIZE = 100

# 列表
var numbers = list([1, 2, 3, 4, 5])
var fruits = list(["苹果", "香蕉", "橙子"])

# 字典
var person = {"name": "李四", "age": 30, "city": "北京"}
```

#### 条件语句

```zrl
var score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 复杂条件
var age = 20
var has_license = true

if age >= 18 and has_license:
    print("可以开车")
else:
    print("不能开车")
```

#### 循环语句

```zrl
# for循环
for i in range(5):
    print("i =", i)

# 遍历列表
var fruits = list(["苹果", "香蕉", "橙子"])
for fruit in fruits:
    print(fruit)

# 遍历字典
var person = {"name": "张三", "age": 25}
for key in keys(person):
    print(key, ":", get_dict(person, key))

# while循环
var count = 0
while count < 5:
    print("count =", count)
    count = count + 1
```

### 10.2 函数定义

```zrl
# 基本函数
func greet(name):
    print("你好, " + name + "!")

greet("小明")

# 带返回值的函数
func add(a, b):
    return a + b

var result = add(5, 3)
print("5 + 3 =", result)

# 带默认参数的函数
func power(base, exponent=2):
    return pow(base, exponent)

print("平方:", power(5))
print("立方:", power(5, 3))

# 多个返回值（使用列表）
func get_stats(numbers):
    var total = sum(numbers)
    var avg = total / len(numbers)
    return list([total, avg])

var stats = get_stats(list([1, 2, 3, 4, 5]))
print("总和:", get_item(stats, 0))
print("平均:", get_item(stats, 1))
```

### 10.3 类与对象

```zrl
# 类定义
class Person:
    func init(name, age):
        self.name = name
        self.age = age
    
    func greet():
        print("我是" + self.name + "，今年" + str(self.age) + "岁")
    
    func is_adult():
        return self.age >= 18

# 创建对象
var person = Person("王五", 25)
person.greet()
print("是否成年:", person.is_adult())

# 继承
class Student(Person):
    func init(name, age, grade):
        self.init(name, age)  # 调用父类构造函数
        self.grade = grade
    
    func study():
        print(self.name + "正在" + self.grade + "学习")

var student = Student("小红", 16, "高一")
student.greet()
student.study()
```

### 10.4 异常处理

```zrl
# 基本异常处理
try:
    var result = 10 / 0
except:
    print("捕获到除零错误")

# 捕获特定异常
try:
    var d = {"a": 1}
    var value = d["nonexistent"]
except KeyError:
    print("键不存在")

# finally块
try:
    print("执行一些操作")
except:
    print("发生错误")
finally:
    print("finally块总是执行")

# else块
try:
    var x = 5 + 3
except:
    print("错误")
else:
    print("没有异常，执行else块")
```

### 10.5 模块导入

```zrl
# 导入绘图模块
import painter

painter.init(800, 600)
painter.pen_color("blue")
painter.circle(50)
painter.done()

# 导入窗口模块
import window

var win = window.create("我的窗口", 400, 300)
var label = window.label(win, "Hello ZRL!")
window.run(win)

# 导入系统模块
import os

print("当前目录:", os.current_dir())
var files = os.list_dir(".")
for f in files:
    print(f)

# 导入HTTP模块
import http

var response = http.get("http://example.com")
print(response)
```

### 10.6 JSON处理

```zrl
# JSON序列化
var data = {"name": "张三", "age": 25, "city": "北京"}
var json_str = json_dumps(data)
print("JSON:", json_str)

# JSON反序列化
var parsed = json_loads(json_str)
print("解析:", parsed)
print("姓名:", get_dict(parsed, "name"))

# 处理列表JSON
var items = list([1, 2, 3, 4, 5])
var items_json = json_dumps(items)
var items_parsed = json_loads(items_json)
print("列表:", items_parsed)
```

### 10.7 Base64编码

```zrl
var text = "Hello ZRL!"
var encoded = base64_encode(text)
print("编码:", encoded)

var decoded = base64_decode(encoded)
print("解码:", decoded)

# 中文编码
var chinese = "你好世界"
var chinese_encoded = base64_encode(chinese)
var chinese_decoded = base64_decode(chinese_encoded)
print("中文:", chinese_decoded)
```

### 10.8 列表和字典操作

```zrl
# 列表操作
var numbers = list([5, 2, 8, 1, 9])
print("原始:", numbers)
print("排序:", sorted(numbers))
print("包含8:", contains(numbers, 8))
print("8的位置:", index(numbers, 8))
print("1的个数:", count(numbers, 1))
print("切片[1:4]:", slice(numbers, 1, 4))

# 字典操作
var person = {"name": "李四", "age": 30}
print("键:", keys(person))
print("值:", values(person))
print("姓名:", get_dict(person, "name"))

# zip函数
var names = list(["张三", "李四", "王五"])
var scores = list([85, 92, 78])
print("姓名分数:", zip(names, scores))

# enumerate函数
print("带索引:", enumerate(numbers))
```

### 10.9 数学运算

```zrl
# 基本运算
print("平方根:", sqrt(16))
print("幂运算:", pow(2, 10))
print("绝对值:", abs(-5))
print("四舍五入:", round(3.7))

# 三角函数
print("sin(30度):", sin(3.14159 / 6))
print("cos(0):", cos(0))
print("tan(45度):", tan(3.14159 / 4))

# 对数函数
print("自然对数:", log(10))
print("常用对数:", log10(100))
print("指数:", exp(1))

# 其他数学函数
print("向上取整:", ceil(3.2))
print("向下取整:", floor(3.8))
print("阶乘:", factorial(5))
print("最大公约数:", gcd(12, 8))
print("最小公倍数:", lcm(12, 8))
```

### 10.10 类型检查

```zrl
var s = "hello"
var n = 42
var lst = list([1, 2, 3])
var d = {"a": 1}
var b = true
var empty = null

print("是字符串:", is_string(s))
print("是数字:", is_number(n))
print("是列表:", is_list(lst))
print("是字典:", is_dict(d))
print("是布尔:", is_bool(b))
print("是空值:", is_null(empty))
```

### 10.11 进制转换

```zrl
print("十六进制:", hex(255))
print("八进制:", oct(64))
print("二进制:", bin(16))
print("字符:", chr(65))
print("ASCII:", ord("A"))
```

### 10.12 文件操作

```zrl
import os

# 写入文件
os.write_file("test.txt", "Hello ZRL!")

# 读取文件
var content = os.read_file("test.txt")
print("内容:", content)

# 追加文件
os.append_file("test.txt", "\n追加内容")

# 检查文件
print("文件存在:", os.path_exists("test.txt"))
print("是文件:", os.is_file("test.txt"))
print("大小:", os.get_size("test.txt"))

# 目录操作
os.make_dir("new_folder")
var files = os.list_dir(".")
print("文件列表:", files)

# 删除文件
os.remove_file("test.txt")
```

### 10.13 完整示例：简单计算器

```zrl
# 简单计算器
func calculator():
    print("=== 简单计算器 ===")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    
    var choice = input("请选择操作 (1-4): ")
    var num1 = float(input("请输入第一个数字: "))
    var num2 = float(input("请输入第二个数字: "))
    
    var result = 0
    
    if choice == "1":
        result = num1 + num2
        print("结果:", num1, "+", num2, "=", result)
    elif choice == "2":
        result = num1 - num2
        print("结果:", num1, "-", num2, "=", result)
    elif choice == "3":
        result = num1 * num2
        print("结果:", num1, "*", num2, "=", result)
    elif choice == "4":
        if num2 == 0:
            print("错误: 除数不能为零")
        else:
            result = num1 / num2
            print("结果:", num1, "/", num2, "=", result)
    else:
        print("无效的选择")

# 运行计算器
calculator()
```

### 10.14 完整示例：学生成绩管理系统

```zrl
# 学生成绩管理系统

var students = dict()

func add_student():
    var name = input("请输入学生姓名: ")
    var score = float(input("请输入学生成绩: "))
    set_dict(students, name, score)
    print("添加成功!")

func show_students():
    print("=== 学生成绩列表 ===")
    if len(keys(students)) == 0:
        print("暂无学生数据")
    else:
        for name in keys(students):
            print(name, ":", get_dict(students, name))

func calculate_average():
    if len(keys(students)) == 0:
        print("暂无学生数据")
        return
    
    var total = 0
    for name in keys(students):
        total = total + get_dict(students, name)
    
    var avg = total / len(keys(students))
    print("平均成绩:", avg)

func find_max():
    if len(keys(students)) == 0:
        print("暂无学生数据")
        return
    
    var max_score = -1
    var max_student = ""
    
    for name in keys(students):
        var score = get_dict(students, name)
        if score > max_score:
            max_score = score
            max_student = name
    
    print("最高分:", max_student, "-", max_score)

func main():
    while true:
        print("\n=== 学生成绩管理系统 ===")
        print("1. 添加学生")
        print("2. 显示所有学生")
        print("3. 计算平均分")
        print("4. 查找最高分")
        print("5. 退出")
        
        var choice = input("请选择操作 (1-5): ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            calculate_average()
        elif choice == "4":
            find_max()
        elif choice == "5":
            print("感谢使用!")
            break
        else:
            print("无效的选择")

# 运行系统
main()
```

### 10.15 完整示例：图形绘制

```zrl
import painter

# 绘制彩虹螺旋
painter.init(800, 600)
painter.set_title("彩虹螺旋")
painter.bg_color("black")
painter.speed(10)

var colors = list(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

for i in range(360):
    painter.pen_color(get_item(colors, i % 7))
    painter.forward(i * 2)
    painter.right(90)

painter.done()
```

这些示例展示了ZRL语言的主要特性和用法，开发者可以根据需要组合使用这些功能来构建各种应用程序。
