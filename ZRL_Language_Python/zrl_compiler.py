import pickle
import os
from zrl_lexer import Lexer
from zrl_parser import Parser

def compile_zrl(source_code, output_file):
    """将 ZRL 源代码编译为 .zxx 字节码文件（使用 pickle 序列化 AST）"""
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    with open(output_file, 'wb') as f:
        pickle.dump(program, f)
    print(f"Successfully compiled to {output_file}")

def load_zxx(bytecode_file):
    """加载 .zxx 字节码文件并返回 AST"""
    with open(bytecode_file, 'rb') as f:
        program = pickle.load(f)
    return program

def run_zrl_file(filename, interpreter):
    """根据文件扩展名执行 ZRL 文件"""
    ext = os.path.splitext(filename)[1]
    if ext == '.zxx':
        program = load_zxx(filename)
    elif ext in ['.z', '.zs']:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    interpreter.interpret(program)

if __name__ == "__main__":
    # 简单测试编译
    test_code = 'print("Hello from compiled ZRL!")'
    compile_zrl(test_code, "test.zxx")
    from zrl_interpreter import Interpreter
    run_zrl_file("test.zxx", Interpreter())
