import turtle
import tkinter as tk
from tkinter import messagebox
import os
import sys
import pickle
from zrl_lexer import Lexer
from zrl_parser import Parser

class ZRLPainter:
    def __init__(self):
        self.t = None
        self.screen = None

    def init(self, width=800, height=600):
        if not self.screen:
            self.screen = turtle.Screen()
            self.screen.setup(width, height)
            self.t = turtle.Turtle()

    def pen_color(self, color): self.t.pencolor(color)
    def fill_color(self, color): self.t.fillcolor(color)
    def move_to(self, x, y): self.t.goto(x, y)
    def forward(self, dist): self.t.forward(dist)
    def backward(self, dist): self.t.backward(dist)
    def left(self, angle): self.t.left(angle)
    def right(self, angle): self.t.right(angle)
    def circle(self, radius): self.t.circle(radius)
    def rectangle(self, x, y, w, h):
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        for _ in range(2):
            self.t.forward(w)
            self.t.left(90)
            self.t.forward(h)
            self.t.left(90)
    def begin_fill(self): self.t.begin_fill()
    def end_fill(self): self.t.end_fill()
    def clear(self): self.t.clear()
    def done(self): turtle.done()
    def pen_up(self): self.t.penup()
    def pen_down(self): self.t.pendown()
    def pen_size(self, size): self.t.pensize(size)
    def speed(self, s): self.t.speed(s)
    def set_title(self, title): self.screen.title(title)
    def bg_color(self, color): self.screen.bgcolor(color)
    def dot(self, size=None, color=None): self.t.dot(size, color)
    def triangle(self, size):
        for _ in range(3):
            self.t.forward(size)
            self.t.left(120)
    def polygon(self, sides, size):
        angle = 360 / sides
        for _ in range(sides):
            self.t.forward(size)
            self.t.left(angle)
    def star(self, size, points=5):
        angle = 180 - (180 / points)
        for _ in range(points * 2):
            self.t.forward(size)
            self.t.left(angle)
    def spiral(self, size, loops=10):
        for i in range(loops * 10):
            self.t.forward(size + i * 2)
            self.t.left(30)
    def hide_turtle(self): self.t.hideturtle()
    def show_turtle(self): self.t.showturtle()
    def home(self): self.t.home()
    def set_heading(self, angle): self.t.setheading(angle)
    def get_x(self): return self.t.xcor()
    def get_y(self): return self.t.ycor()
    def write_text(self, text, move=False, align="left", font=("Arial", 12, "normal")):
        self.t.write(text, move=move, align=align, font=font)

class ZRLWindow:
    def create(self, title, width, height):
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{width}x{height}")
        return root

    def label(self, parent, text, font=None):
        lbl = tk.Label(parent, text=text, font=font)
        lbl.pack()
        return lbl

    def button(self, parent, text, command, width=None):
        btn = tk.Button(parent, text=text, command=command, width=width)
        btn.pack()
        return btn

    def entry(self, parent, width=None):
        ent = tk.Entry(parent, width=width)
        ent.pack()
        return ent

    def text(self, parent, width=40, height=10):
        txt = tk.Text(parent, width=width, height=height)
        txt.pack()
        return txt

    def get_entry(self, entry):
        return entry.get()

    def set_entry(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def get_text(self, text_widget):
        return text_widget.get("1.0", tk.END)

    def set_text(self, text_widget, text):
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", text)

    def set_position(self, widget, x, y):
        widget.place(x=x, y=y)

    def set_size(self, widget, width, height):
        widget.config(width=width, height=height)

    def message_box(self, title, message, msg_type="info"):
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "question":
            return messagebox.askquestion(title, message)

    def confirm(self, title, message):
        return messagebox.askyesno(title, message)

    def run(self, root):
        root.mainloop()

    def frame(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        return frame

    def scale(self, parent, from_, to, orient=tk.HORIZONTAL):
        scale = tk.Scale(parent, from_=from_, to=to, orient=orient)
        scale.pack()
        return scale

    def get_scale(self, scale):
        return scale.get()

    def listbox(self, parent, height=10):
        lb = tk.Listbox(parent, height=height)
        lb.pack()
        return lb

    def add_listbox(self, listbox, item):
        listbox.insert(tk.END, item)

    def get_selected(self, listbox):
        return listbox.get(tk.ANCHOR)

class ZRLOS:
    def current_dir(self): return os.getcwd()
    def list_dir(self, path="."): return os.listdir(path)
    def make_dir(self, path): os.makedirs(path, exist_ok=True)
    def execute(self, cmd): return os.system(cmd)
    def exit(self, code=0): sys.exit(code)
    def path_exists(self, path): return os.path.exists(path)
    def is_file(self, path): return os.path.isfile(path)
    def is_dir(self, path): return os.path.isdir(path)
    def remove_file(self, path): os.remove(path)
    def remove_dir(self, path): os.rmdir(path)
    def rename(self, old, new): os.rename(old, new)
    def copy_file(self, src, dst): 
        import shutil
        shutil.copy(src, dst)
    def get_env(self, key): return os.environ.get(key)
    def set_env(self, key, value): os.environ[key] = value
    def platform(self): return sys.platform
    def get_size(self, path): return os.path.getsize(path)
    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    def write_file(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    def append_file(self, path, content):
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
    
    def join_path(self, *paths): return os.path.join(*paths)
    def split_path(self, path): return os.path.split(path)
    def basename(self, path): return os.path.basename(path)
    def dirname(self, path): return os.path.dirname(path)
    def abs_path(self, path): return os.path.abspath(path)
    def real_path(self, path): return os.path.realpath(path)
    def exists(self, path): return os.path.exists(path)
    def expand_user(self, path): return os.path.expanduser(path)
    def expand_vars(self, path): return os.path.expandvars(path)
    def get_cwd(self): return os.getcwd()
    def chdir(self, path): os.chdir(path)
    
    def get_env_all(self): return dict(os.environ)
    def del_env(self, key): 
        if key in os.environ:
            del os.environ[key]
    def env_keys(self): return list(os.environ.keys())
    
    def get_pid(self): return os.getpid()
    def get_ppid(self): return os.getppid()
    def get_user(self): return os.getlogin()
    def get_home(self): return os.path.expanduser("~")
    def get_temp_dir(self):
        import tempfile
        return tempfile.gettempdir()
    
    def start_process(self, cmd):
        import subprocess
        return subprocess.Popen(cmd, shell=True).pid
    
    def run_process(self, cmd):
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    
    def kill_process(self, pid):
        import signal
        os.kill(pid, signal.SIGTERM)
    
    def sleep(self, seconds):
        import time
        time.sleep(seconds)
    
    def mkdir_p(self, path):
        os.makedirs(path, exist_ok=True)
    
    def mkdir(self, path):
        os.mkdir(path)
    
    def copy_dir(self, src, dst):
        import shutil
        shutil.copytree(src, dst, dirs_exist_ok=True)
    
    def remove_tree(self, path):
        import shutil
        shutil.rmtree(path)
    
    def walk(self, path):
        return list(os.walk(path))
    
    def stat(self, path):
        return {
            "size": os.path.getsize(path),
            "mtime": os.path.getmtime(path),
            "atime": os.path.getatime(path),
            "ctime": os.path.getctime(path),
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path)
        }
    
    def cpu_count(self):
        return os.cpu_count()
    
    def load_avg(self):
        if hasattr(os, 'getloadavg'):
            return os.getloadavg()
        return [0.0, 0.0, 0.0]
    
    def mem_info(self):
        import psutil
        process = psutil.Process(os.getpid())
        return {
            "rss": process.memory_info().rss,
            "vms": process.memory_info().vms
        }

class ZRLHTTP:
        def get(self, url):
            import urllib.request
            try:
                response = urllib.request.urlopen(url)
                data = response.read()
                return data.decode('utf-8')
            except Exception as e:
                raise RuntimeError(f"HTTP GET failed: {e}")
        
        def post(self, url, data=None):
            import urllib.request
            import urllib.parse
            try:
                data_encoded = urllib.parse.urlencode(data).encode('utf-8') if data else None
                request = urllib.request.Request(url, data=data_encoded, method='POST')
                response = urllib.request.urlopen(request)
                return response.read().decode('utf-8')
            except Exception as e:
                raise RuntimeError(f"HTTP POST failed: {e}")
        
        def put(self, url, data=None):
            import urllib.request
            import urllib.parse
            try:
                data_encoded = urllib.parse.urlencode(data).encode('utf-8') if data else None
                request = urllib.request.Request(url, data=data_encoded, method='PUT')
                response = urllib.request.urlopen(request)
                return response.read().decode('utf-8')
            except Exception as e:
                raise RuntimeError(f"HTTP PUT failed: {e}")
        
        def delete(self, url):
            import urllib.request
            try:
                request = urllib.request.Request(url, method='DELETE')
                response = urllib.request.urlopen(request)
                return response.read().decode('utf-8')
            except Exception as e:
                raise RuntimeError(f"HTTP DELETE failed: {e}")
        
        def request(self, method, url, data=None, headers=None):
            import urllib.request
            import urllib.parse
            try:
                data_encoded = urllib.parse.urlencode(data).encode('utf-8') if data else None
                request = urllib.request.Request(url, data=data_encoded, method=method.upper())
                if headers:
                    for key, value in headers.items():
                        request.add_header(key, value)
                response = urllib.request.urlopen(request)
                return response.read().decode('utf-8')
            except Exception as e:
                raise RuntimeError(f"HTTP {method.upper()} failed: {e}")

def handle_import(stmt, env, interpreter):
    module_name = stmt.module_name
    
    # 1. 内置标准库
    if module_name == "painter":
        env.define(stmt.alias or "painter", ZRLPainter())
        return
    if module_name == "window":
        env.define(stmt.alias or "window", ZRLWindow())
        return
    if module_name == "os":
        env.define(stmt.alias or "os", ZRLOS())
        return
    if module_name == "http":
        env.define(stmt.alias or "http", ZRLHTTP())
        return

    # 2. 本地文件导入
    for ext in ['.zxx', '.z', '.zs']:
        filename = f"{module_name}{ext}"
        if os.path.exists(filename):
            from zrl_interpreter import Interpreter, Environment
            module_env = Environment(interpreter.global_env)
            
            if ext == '.zxx':
                with open(filename, 'rb') as f:
                    program = pickle.load(f)
            else:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                lexer = Lexer(code)
                parser = Parser(lexer.tokenize())
                program = parser.parse()
            
            module_interpreter = Interpreter(module_env)
            module_interpreter.interpret(program)
            
            class ModuleObject:
                def __init__(self, env):
                    self.__dict__.update(env.values)
                def __getattr__(self, name):
                    if name in self.__dict__: return self.__dict__[name]
                    raise AttributeError(f"Module has no attribute '{name}'")

            env.define(stmt.alias or module_name, ModuleObject(module_env))
            return

    raise ImportError(f"Module '{module_name}' not found.")
