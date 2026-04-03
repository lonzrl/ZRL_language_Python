#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试窗口显示"""

import tkinter as tk
import sys

# 设置UTF-8编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

print("正在创建窗口...")

root = tk.Tk()
root.title("测试窗口")
root.geometry("400x300")

label = tk.Label(root, text="如果你看到这个窗口，说明GUI正常工作！", 
                 font=('Microsoft YaHei UI', 12))
label.pack(pady=50)

def on_close():
    print("窗口关闭")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

print("窗口已创建，应该会显示...")
print("如果看不到窗口，请检查是否有其他窗口遮挡")

root.mainloop()

print("窗口已关闭，程序结束")