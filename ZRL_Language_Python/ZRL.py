import sys
import os
import argparse
import pickle
import atexit
from zrl_lexer import Lexer
from zrl_parser import Parser
from zrl_interpreter import Interpreter

VERSION = "1.1.0"

def compile_zrl(source_code, output_file):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    with open(output_file, 'wb') as f:
        pickle.dump(program, f)
    print(f"Successfully compiled to {output_file}")

def run_zrl_file(filename, interpreter):
    ext = os.path.splitext(filename)[1]
    if ext == '.zxx':
        with open(filename, 'rb') as f:
            program = pickle.load(f)
    elif ext in ['.z', '.zs']:
        # 尝试多种编码读取文件
        source_code = None
        for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    source_code = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if source_code is None:
            raise ValueError(f"无法读取文件 {filename}，不支持的编码")
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    interpreter.interpret(program)

def register_file_association():
    """注册.z文件类型关联"""
    try:
        import winreg
        
        # 获取当前可执行文件路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            exe_path = sys.executable
            icon_path = os.path.join(os.path.dirname(exe_path), 'fileicon.ico')
        else:
            # 如果是开发环境
            exe_path = os.path.abspath(sys.argv[0])
            # 对于开发环境，使用pythonw.exe
            if exe_path.endswith('.py'):
                exe_path = f'pythonw.exe "{exe_path}"'
            icon_path = os.path.abspath('icons/fileicon.ico')
        
        # 如果图标文件不存在，尝试使用icon.ico
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(exe_path.replace('"', '')), 'icon.ico')
        
        print("正在注册.z文件类型...")
        print(f"可执行文件: {exe_path}")
        print(f"图标文件: {icon_path}")
        
        # 创建ZRL文件类型
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, '.z') as key:
            winreg.SetValue(key, None, winreg.REG_SZ, 'ZRLFile')
        
        # 设置ZRL文件类型描述
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile') as key:
            winreg.SetValue(key, None, winreg.REG_SZ, 'ZRL源代码文件')
        
        # 设置默认图标
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\DefaultIcon') as key:
            winreg.SetValue(key, None, winreg.REG_SZ, f'{icon_path},0')
        
        # 设置打开命令
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\open\\command') as key:
            winreg.SetValue(key, None, winreg.REG_SZ, f'"{exe_path}" "%1"')
        
        # 设置编辑命令
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\edit\\command') as key:
            winreg.SetValue(key, None, winreg.REG_SZ, f'notepad "%1"')
        
        print("ZRL文件类型注册成功!")
        print("\n现在您可以：")
        print("1. 双击.z文件直接用ZRL运行")
        print("2. 右键.z文件选择'编辑'用记事本打开")
        print("3. 在文件资源管理器中看到.z文件的专用图标")
        
    except PermissionError:
        print("错误: 需要管理员权限来注册文件类型")
        print("请以管理员身份运行此程序")
        sys.exit(1)
    except Exception as e:
        print(f"注册失败: {e}")
        sys.exit(1)

def unregister_file_association():
    """取消注册.z文件类型关联"""
    try:
        import winreg
        
        print("正在取消注册.z文件类型...")
        
        # 删除注册表项
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\edit\\command')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\edit')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\open\\command')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell\\open')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\shell')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile\\DefaultIcon')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 'ZRLFile')
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, '.z')
            print("ZRL文件类型取消注册成功!")
        except FileNotFoundError:
            print("ZRL文件类型未注册，无需取消")
        
    except PermissionError:
        print("错误: 需要管理员权限来取消注册文件类型")
        print("请以管理员身份运行此程序")
        sys.exit(1)
    except Exception as e:
        print(f"取消注册失败: {e}")
        sys.exit(1)

def show_detailed_info():
    print("\n" + "=" * 60)
    print("ZRL (Zero-effort Rapid Language) - 语言信息")
    print("=" * 60)
    print(f"\n版本: {VERSION}")
    print("作者: ZRL Team")
    print("平台: Windows")
    print("\n语言特性:")
    print("  • 简洁的语法，类似Python")
    print("  • 支持面向对象编程")
    print("  • 内置绘图模块 (painter)")
    print("  • 内置GUI窗口模块 (window)")
    print("  • 内置系统操作模块 (os)")
    print("  • 支持模块导入和预编译 (.zxx)")
    print("\n快速入门:")
    print("\n1. 变量声明:")
    print("   var x = 10")
    print("   const PI = 3.14")
    print("   var name = 'ZRL'")
    print("\n2. 条件语句:")
    print("   if x > 5:")
    print("       print('x is greater than 5')")
    print("   else:")
    print("       print('x is less or equal to 5')")
    print("\n3. 循环:")
    print("   for i in range(5):")
    print("       print(i)")
    print("   while x > 0:")
    print("       x = x - 1")
    print("\n4. 函数:")
    print("   func add(a, b):")
    print("       return a + b")
    print("   var result = add(5, 3)")
    print("\n5. 类:")
    print("   class Person:")
    print("       func init(name):")
    print("           self.name = name")
    print("       func greet():")
    print("           print('Hello, ' + self.name)")
    print("\n6. 模块导入:")
    print("   import painter")
    print("   painter.init()")
    print("   painter.circle(50)")
    print("   painter.done()")
    print("\n更多信息请访问: https://github.com/zrl-lang/zrl")
    print("=" * 60 + "\n")

def show_help():
    print("\n" + "=" * 50)
    print("ZRL 帮助系统")
    print("=" * 50)
    print("\n内置命令:")
    print("  help     - 显示此帮助信息")
    print("  exit()   - 退出REPL")
    print("  quit     - 退出REPL")
    print("  clear    - 清屏")
    print("  history  - 显示命令历史")
    print("\n命令行参数:")
    print("  --terminal  - 启动图形化终端")
    print("  --ide       - 启动IDE集成开发环境")
    print("\n内置函数:")
    print("  print(...)      - 输出内容到控制台")
    print("  input(prompt)   - 从控制台读取输入")
    print("  len(obj)        - 返回对象长度")
    print("  range(start, stop, step) - 生成数字序列")
    print("  type(obj)       - 返回对象类型")
    print("  str(obj)        - 转换为字符串")
    print("  int(obj)        - 转换为整数")
    print("  float(obj)      - 转换为浮点数")
    print("\n标准库模块:")
    print("  import painter  - 绘图模块")
    print("  import window   - GUI窗口模块")
    print("  import os       - 系统操作模块")
    print("\n示例:")
    print("  var x = 10")
    print("  if x > 5: print('x is greater than 5')")
    print("  for i in range(5): print(i)")
    print("  func add(a, b): return a + b")
    print("\n要启动IDE，请运行: ZRL --ide")
    print("=" * 50 + "\n")

def start_repl():
    print(f"ZRL (Zero-effort Rapid Language) v{VERSION}")
    print("Type 'exit()' or 'quit' to exit. Type 'help' for available commands.")
    print("=" * 50)
    interpreter = Interpreter()
    
    # 定义退出函数
    def zrl_exit(code=0): sys.exit(code)
    interpreter.global_env.define("exit", zrl_exit)
    
    # 命令历史
    history = []
    history_file = os.path.expanduser("~/.zrl_history")
    
    # 加载历史记录
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = [line.strip() for line in f if line.strip()]
    except:
        pass
    
    # 保存历史记录
    def save_history():
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                for line in history[-100:]:  # 只保存最近100条
                    f.write(line + '\n')
        except:
            pass
    
    atexit.register(save_history)
    
    # 可用命令补全列表
    keywords = ['if', 'else', 'elif', 'for', 'while', 'func', 'return', 'import', 'as', 
                'from', 'class', 'self', 'true', 'false', 'null', 'var', 'const', 'and', 'or', 'not', 'in']
    builtins = ['print', 'input', 'len', 'range', 'str', 'int', 'float', 'type']
    modules = ['painter', 'window', 'os']
    
    def autocomplete(text, state):
        options = keywords + builtins + modules + [str(i) for i in range(100)]
        if not text:
            return None
        matches = [opt for opt in options if opt.startswith(text)]
        try:
            return matches[state]
        except IndexError:
            return None
    
    # 尝试导入readline模块（Windows可能不可用）
    try:
        import readline
        readline.set_completer(autocomplete)
        readline.parse_and_bind("tab: complete")
        # 加载历史
        for item in history[-50:]:
            readline.add_history(item)
    except:
        pass
    
    while True:
        try:
            line = input("zrl > ")
            if not line: 
                continue
            
            # 处理特殊命令
            if line.strip() == "exit()" or line.strip() == "quit":
                save_history()
                break
            elif line.strip() == "help":
                show_help()
                continue
            elif line.strip() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif line.strip() == "history":
                for i, h in enumerate(history[-10:], 1):
                    print(f"  {i}: {h}")
                continue
            
            # 添加到历史
            if line and (not history or line != history[-1]):
                history.append(line)
                try:
                    readline.add_history(line)
                except:
                    pass
            
            # 执行代码
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter.interpret(program)
            
        except KeyboardInterrupt:
            print("\nType 'exit()' or 'quit' to exit.")
            continue
        except EOFError:
            print("\nGoodbye!")
            save_history()
            break
        except SyntaxError as e:
            print(f"语法错误: {e}")
        except RuntimeError as e:
            print(f"运行时错误: {e}")
        except Exception as e:
            print(f"错误: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="ZRL (Zero-effort Rapid Language) - 简洁易用的编程语言",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  ZRL                    启动交互式REPL
  ZRL program.z          运行ZRL程序
  ZRL -c program.z       编译程序为.zxx格式
  ZRL -c program.z -o out.zxx  指定输出文件名
  ZRL --help             显示帮助信息
  ZRL --version          显示版本信息
  ZRL --terminal         启动图形化终端
  ZRL --ide              启动IDE集成开发环境

支持的文件扩展名:
  .z   - ZRL源代码文件（推荐）
  .zs  - ZRL源代码文件（备用）
  .zxx - ZRL预编译字节码文件
        """
    )
    parser.add_argument("file", nargs="?", help="要运行的ZRL文件 (.z, .zs, .zxx)")
    parser.add_argument("-c", "--compile", help="编译.z或.zs文件为.zxx格式", metavar="FILE")
    parser.add_argument("-o", "--output", help="编译输出文件名", metavar="OUTFILE")
    parser.add_argument("-v", "--version", action="store_true", help="显示版本信息")
    parser.add_argument("--check", help="检查语法而不执行", metavar="FILE")
    parser.add_argument("--ast", help="显示AST而不执行", metavar="FILE")
    parser.add_argument("--info", action="store_true", help="显示语言信息和快速入门指南")
    parser.add_argument("--register", action="store_true", help="注册.z文件类型关联")
    parser.add_argument("--unregister", action="store_true", help="取消.z文件类型关联")
    parser.add_argument("--terminal", action="store_true", help="启动图形化GUI终端(支持中文显示)")
    parser.add_argument("--ide", action="store_true", help="启动ZRL IDE集成开发环境")

    args = parser.parse_args()
    
    if args.version:
        print(f"ZRL (Zero-effort Rapid Language) v{VERSION}")
        print("一个简洁易用的编程语言，支持图形、GUI和系统操作")
        return
    
    if args.info:
        show_detailed_info()
        return
    
    if args.register:
        register_file_association()
        return
    
    if args.unregister:
        unregister_file_association()
        return
    
    if args.terminal:
        try:
            from zrl_terminal import main as terminal_main
            terminal_main()
        except ImportError:
            print("错误: 无法导入zrl_terminal模块")
            print("请确保zrl_terminal.py文件存在")
            sys.exit(1)
        except Exception as e:
            print(f"启动GUI终端失败: {e}")
            sys.exit(1)
        return
    
    if args.ide:
        try:
            from zrl_ide import main as ide_main
            ide_main()
        except ImportError:
            print("错误: 无法导入zrl_ide模块")
            print("请确保zrl_ide.py文件存在")
            sys.exit(1)
        except Exception as e:
            print(f"启动IDE失败: {e}")
            sys.exit(1)
        return
    
    if args.check:
        try:
            # 尝试多种编码读取文件
            code = None
            for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
                try:
                    with open(args.check, 'r', encoding=encoding) as f:
                        code = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if code is None:
                print(f"错误: 无法读取文件 {args.check}，不支持的编码")
                sys.exit(1)
            
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            print(f"语法检查通过: {args.check}")
        except SyntaxError as e:
            print(f"语法错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
        return
    
    if args.ast:
        try:
            # 尝试多种编码读取文件
            code = None
            for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
                try:
                    with open(args.ast, 'r', encoding=encoding) as f:
                        code = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if code is None:
                print(f"错误: 无法读取文件 {args.ast}，不支持的编码")
                sys.exit(1)
            
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            print(f"AST for {args.ast}:")
            print(program)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
        return

    if args.compile:
        source = args.compile
        output = args.output or source.rsplit('.', 1)[0] + ".zxx"
        if not os.path.exists(source):
            print(f"错误: 文件 '{source}' 不存在")
            sys.exit(1)
        try:
            # 尝试多种编码读取文件
            code = None
            for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
                try:
                    with open(source, 'r', encoding=encoding) as f:
                        code = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if code is None:
                print(f"错误: 无法读取文件 {source}，不支持的编码")
                sys.exit(1)
            
            compile_zrl(code, output)
            print(f"编译成功: {source} -> {output}")
        except SyntaxError as e:
            print(f"语法错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"编译错误: {e}")
            sys.exit(1)
        return

    if args.file:
        if not os.path.exists(args.file):
            print(f"错误: 文件 '{args.file}' 不存在")
            sys.exit(1)
        interpreter = Interpreter()
        try:
            run_zrl_file(args.file, interpreter)
        except SyntaxError as e:
            print(f"语法错误: {e}")
            sys.exit(1)
        except RuntimeError as e:
            print(f"运行时错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        start_repl()

if __name__ == "__main__":
    main()
