#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZRL Terminal - 专门为ZRL语言设计的图形化终端
支持中文显示,语法高亮,命令历史等功能
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
import os
from zrl_lexer import Lexer
from zrl_parser import Parser
from zrl_interpreter import Interpreter

VERSION = "1.1.0"


class ZRLTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title(f"ZRL Terminal v{VERSION}")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # 居中显示窗口
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"900x600+{x}+{y}")
        
        # 设置UTF-8编码
        if sys.platform == 'win32':
            # Windows下设置编码
            import locale
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass
        
        # 初始化解释器
        self.interpreter = Interpreter()
        
        # 替换print函数，使其输出到GUI
        original_print = self.interpreter.global_env.get('print')
        def gui_print(*args, **kwargs):
            output = ' '.join(str(arg) for arg in args)
            self.append_output(output + '\n', tag='output')
        
        # 直接在环境字典中替换
        self.interpreter.global_env.values['print'] = gui_print
        
        # 命令历史
        self.history = []
        self.history_index = -1
        self.history_file = os.path.expanduser("~/.zrl_terminal_history")
        self.load_history()
        
        # 多行输入缓存
        self.input_buffer = []
        self.in_multiline = False
        
        # 设置样式
        self.setup_styles()
        
        # 创建UI
        self.create_widgets()
        
        # 显示欢迎信息
        self.show_welcome()
        
        # 绑定事件
        self.setup_bindings()
        
        # 注册退出时保存历史
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 自动聚焦到输入框
        self.input_entry.focus_set()
    
    def setup_styles(self):
        """设置颜色和字体样式"""
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#d4d4d4',
            'output_bg': '#1e1e1e',
            'output_fg': '#d4d4d4',
            'input_bg': '#252526',
            'input_fg': '#d4d4d4',
            'prompt': '#4ec9b0',
            'error': '#f48771',
            'success': '#4ec9b0',
            'keyword': '#569cd6',
            'string': '#ce9178',
            'comment': '#6a9955',
            'number': '#b5cea8',
            'operator': '#d4d4d4',
            'function': '#dcdcaa',
        }
        
        # 尝试使用支持中文的字体
        fonts = ['Microsoft YaHei UI', 'Microsoft YaHei', 'SimHei', 'Consolas', 'Monaco', 'monospace']
        self.font_family = None
        for font in fonts:
            if font in self.root.tk.call('font', 'families'):
                self.font_family = font
                break
        
        if self.font_family is None:
            self.font_family = 'Courier New'
        
        self.font_size = 11
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 工具栏
        toolbar = tk.Frame(main_frame, bg=self.colors['bg'], height=30)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # 工具栏按钮
        btn_style = {'bg': self.colors['input_bg'], 'fg': self.colors['fg'],
                    'activebackground': self.colors['input_fg'], 'activeforeground': self.colors['bg'],
                    'relief': tk.FLAT, 'padx': 10, 'pady': 5, 'font': (self.font_family, 9)}
        
        run_btn = tk.Button(toolbar, text="📁 打开文件", command=self.open_file, **btn_style)
        run_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = tk.Button(toolbar, text="💾 保存代码", command=self.save_code, **btn_style)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(toolbar, text="🧹 清屏", command=self.clear_output, **btn_style)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        help_btn = tk.Button(toolbar, text="❓ 帮助", command=self.show_help, **btn_style)
        help_btn.pack(side=tk.LEFT, padx=2)
        
        # 版本标签
        version_label = tk.Label(toolbar, text=f"ZRL v{VERSION}", 
                               bg=self.colors['bg'], fg=self.colors['prompt'],
                               font=(self.font_family, 9, 'bold'))
        version_label.pack(side=tk.RIGHT, padx=10)
        
        # 分割线
        separator = tk.Frame(main_frame, bg=self.colors['prompt'], height=2)
        separator.pack(fill=tk.X)
        
        # 输出区域
        output_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            bg=self.colors['output_bg'],
            fg=self.colors['output_fg'],
            font=(self.font_family, self.font_size),
            wrap=tk.WORD,
            state=tk.DISABLED,
            padx=10,
            pady=10,
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['prompt'],
            selectforeground=self.colors['bg']
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置文本标签用于语法高亮
        self.configure_text_tags()
        
        # 输入区域
        input_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 提示符标签
        self.prompt_label = tk.Label(
            input_frame,
            text="zrl > ",
            bg=self.colors['bg'],
            fg=self.colors['prompt'],
            font=(self.font_family, self.font_size, 'bold')
        )
        self.prompt_label.pack(side=tk.LEFT)
        
        # 输入框
        self.input_entry = tk.Entry(
            input_frame,
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            font=(self.font_family, self.font_size),
            insertbackground=self.colors['fg'],
            relief=tk.FLAT,
            bd=0
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def configure_text_tags(self):
        """配置文本标签用于语法高亮"""
        tags = {
            'prompt': {'foreground': self.colors['prompt']},
            'error': {'foreground': self.colors['error']},
            'success': {'foreground': self.colors['success']},
            'output': {'foreground': self.colors['output_fg']},
        }
        
        for tag, config in tags.items():
            self.output_text.tag_configure(tag, **config)
    
    def setup_bindings(self):
        """绑定键盘事件"""
        self.input_entry.bind('<Return>', self.on_return)
        self.input_entry.bind('<Up>', self.on_up_arrow)
        self.input_entry.bind('<Down>', self.on_down_arrow)
        self.input_entry.bind('<Escape>', lambda e: self.input_entry.delete(0, tk.END))
        
        # 复制粘贴快捷键
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-v>', self.paste_text)
    
    def load_history(self):
        """加载命令历史"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"加载历史记录失败: {e}")
    
    def save_history(self):
        """保存命令历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for line in self.history[-100:]:  # 只保存最近100条
                    f.write(line + '\n')
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def show_welcome(self):
        """显示欢迎信息"""
        welcome_text = f"""
╔════════════════════════════════════════════════════════════╗
║  ZRL Terminal - 零努力快速语言                             ║
║  版本: {VERSION}                                              ║
║  支持中文显示 | 语法高亮 | 命令历史                        ║
╚════════════════════════════════════════════════════════════╝

欢迎使用 ZRL 终端！

可用命令:
  help          - 显示帮助信息
  clear         - 清屏
  history       - 显示命令历史
  exit          - 退出终端

快速测试:
  1. 点击"📁 打开文件"按钮选择 test_output.z 测试输出
  2. 或在下方直接输入: print("你好，世界！")

开始输入 ZRL 代码或使用 'help' 查看更多帮助信息...
"""
        self.append_output(welcome_text, tag='prompt')
    
    def append_output(self, text, tag='output'):
        """添加输出到文本区域"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_output(self):
        """清空输出区域"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.input_entry.focus_set()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
═════════════════════════════════════════════════════════
  ZRL 终端帮助系统
═════════════════════════════════════════════════════════

终端命令:
  help     - 显示此帮助信息
  clear    - 清屏
  history  - 显示命令历史 (最近10条)
  exit     - 退出终端

快捷键:
  ↑        - 向上浏览历史
  ↓        - 向下浏览历史
  ESC      - 清空输入
  Ctrl+C   - 复制选中文本
  Ctrl+V   - 粘贴文本

内置函数:
  print(...)      - 输出内容
  input(prompt)   - 从用户获取输入
  len(obj)        - 返回对象长度
  range(start, stop, step) - 生成序列
  str(obj)        - 转为字符串
  int(obj)        - 转为整数
  float(obj)      - 转为浮点数

语言特性:
  • 变量声明: var x = 10, const PI = 3.14
  • 条件语句: if x > 5: ... elif ... else ...
  • 循环语句: for i in range(5): ... while ...
  • 函数定义: func name(params): ...
  • 类定义: class Name: ...
  • 模块导入: import module

示例:
  var name = "张三"
  if len(name) > 0:
      print("你好, " + name)
  for i in range(5):
      print(i)
═════════════════════════════════════════════════════════
"""
        self.append_output(help_text, tag='prompt')
    
    def show_history(self):
        """显示命令历史"""
        if not self.history:
            self.append_output("命令历史为空\n", tag='prompt')
        else:
            self.append_output("命令历史 (最近10条):\n", tag='prompt')
            for i, cmd in enumerate(self.history[-10:], 1):
                self.append_output(f"  {i}: {cmd}\n", tag='output')
    
    def on_return(self, event):
        """处理回车键"""
        line = self.input_entry.get().strip()
        
        if not line:
            self.input_entry.delete(0, tk.END)
            return
        
        # 显示输入的命令
        self.append_output(f"zrl > {line}\n", tag='prompt')
        
        # 处理特殊命令
        if line == "exit" or line == "quit":
            self.on_closing()
            return
        elif line == "help":
            self.show_help()
            self.input_entry.delete(0, tk.END)
            return
        elif line == "clear":
            self.clear_output()
            return
        elif line == "history":
            self.show_history()
            self.input_entry.delete(0, tk.END)
            return
        
        # 添加到历史
        if not self.history or line != self.history[-1]:
            self.history.append(line)
        
        # 重置历史索引
        self.history_index = len(self.history)
        
        # 执行代码
        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            self.interpreter.interpret(program)
        except SyntaxError as e:
            self.append_output(f"语法错误: {e}\n", tag='error')
        except RuntimeError as e:
            self.append_output(f"运行时错误: {e}\n", tag='error')
        except Exception as e:
            self.append_output(f"错误: {e}\n", tag='error')
        
        # 清空输入框
        self.input_entry.delete(0, tk.END)
    
    def on_up_arrow(self, event):
        """处理向上箭头 - 浏览历史"""
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.history[self.history_index])
        return 'break'
    
    def on_down_arrow(self, event):
        """处理向下箭头 - 浏览历史"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.input_entry.delete(0, tk.END)
        return 'break'
    
    def copy_text(self, event):
        """复制选中的文本"""
        try:
            selected = self.output_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except:
            pass
        return 'break'
    
    def paste_text(self, event):
        """粘贴文本"""
        try:
            text = self.root.clipboard_get()
            self.input_entry.insert(tk.INSERT, text)
        except:
            pass
        return 'break'
    
    def open_file(self):
        """打开并运行ZRL文件"""
        file_path = filedialog.askopenfilename(
            title="选择ZRL文件",
            filetypes=[
                ("ZRL文件", "*.z"),
                ("ZRL源文件", "*.zs"),
                ("ZRL编译文件", "*.zxx"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.run_file(file_path)
    
    def run_file(self, file_path):
        """运行ZRL文件"""
        self.append_output(f"\n运行文件: {file_path}\n", tag='prompt')
        
        try:
            # 读取文件
            ext = os.path.splitext(file_path)[1]
            source_code = None
            
            if ext == '.zxx':
                import pickle
                with open(file_path, 'rb') as f:
                    program = pickle.load(f)
                self.interpreter.interpret(program)
            else:
                # 尝试多种编码读取文件
                for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            source_code = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if source_code is None:
                    raise ValueError(f"无法读取文件 {file_path}，不支持的编码")
                
                # 执行代码
                lexer = Lexer(source_code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                program = parser.parse()
                self.interpreter.interpret(program)
            
            self.append_output(f"\n✓ 文件执行成功\n", tag='success')
            
        except SyntaxError as e:
            self.append_output(f"语法错误: {e}\n", tag='error')
        except RuntimeError as e:
            self.append_output(f"运行时错误: {e}\n", tag='error')
        except Exception as e:
            self.append_output(f"错误: {e}\n", tag='error')
    
    def save_code(self):
        """保存当前输入的代码到文件"""
        code = self.input_entry.get()
        if not code:
            messagebox.showinfo("提示", "输入框为空，没有可保存的代码")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存ZRL代码",
            defaultextension=".z",
            filetypes=[
                ("ZRL文件", "*.z"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                self.append_output(f"\n✓ 代码已保存到: {file_path}\n", tag='success')
            except Exception as e:
                self.append_output(f"保存失败: {e}\n", tag='error')
    
    def on_closing(self):
        """关闭窗口时的处理"""
        self.save_history()
        self.root.destroy()


def main():
    """主函数"""
    # 设置Windows控制台编码
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except:
            pass
    
    # 创建主窗口并立即隐藏，避免显示空白窗口
    root = tk.Tk()
    root.withdraw()
    
    # 尝试设置图标
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.ico')
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except:
            pass
    
    # 创建终端
    terminal = ZRLTerminal(root)
    
    # 强制更新窗口显示
    root.update()
    root.update_idletasks()
    
    # 确保窗口可见并置顶
    root.deiconify()
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()