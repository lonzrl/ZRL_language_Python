import operator
from zrl_parser import *

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.constants = set()
        self.parent = parent

    def define(self, name, value, is_const=False):
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def assign(self, name, value):
        if name in self.values:
            if name in self.constants:
                raise RuntimeError(f"Cannot assign to constant '{name}'.")
            self.values[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise RuntimeError(f"Undefined variable '{name}'.")

    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise RuntimeError(f"Undefined variable '{name}'.")

class ZRLFunction:
    def __init__(self, name, params, block, env):
        self.name = name
        self.params = params
        self.block = block
        self.env = env

    def call(self, interpreter, args):
        new_env = Environment(self.env)
        for i in range(min(len(args), len(self.params))):
            new_env.define(self.params[i], args[i])
        try:
            interpreter.execute_block(self.block, new_env)
        except ReturnException as e:
            return e.value
        return None

class ZRLClass:
    def __init__(self, name, parent, methods, global_env=None):
        self.name = name
        self.parent = parent
        self.methods = methods
        self.global_env = global_env

    def call(self, interpreter, args):
        instance = ZRLInstance(self, self.global_env)
        if 'init' in self.methods:
            method = self.methods['init']
            # 使用全局环境作为parent
            method_env = Environment(self.global_env)
            method_env.define('self', instance)
            bound_method = ZRLFunction(method.name, method.params, method.block, method_env)
            bound_method.call(interpreter, args)
        return instance

class ZRLInstance:
    def __init__(self, zrl_class, global_env=None):
        self.zrl_class = zrl_class
        self.global_env = global_env
        self.env = Environment()

    def get(self, name):
        if name in self.env.values:
            return self.env.values[name]
        if name in self.zrl_class.methods:
            method = self.zrl_class.methods[name]
            # 使用全局环境作为parent，使方法可以访问全局函数
            method_env = Environment(self.global_env)
            method_env.define('self', self)
            bound_method = ZRLFunction(method.name, method.params, method.block, method_env)
            return bound_method
        if self.zrl_class.parent:
            # Simplified inheritance
            pass
        raise RuntimeError(f"Undefined property '{name}'.")

    def set(self, name, value):
        self.env.define(name, value)

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self, global_env=None):
        self.global_env = global_env or Environment()
        self.setup_builtins()

    def setup_builtins(self):
        # Windows 控制台编码修复
        import sys
        import math
        import time
        import random
        from datetime import datetime

        # 自定义print函数以正确处理中文编码
        def zrl_print(*args, **kwargs):
            try:
                output = ' '.join(str(arg) for arg in args)
                if sys.platform == 'win32':
                    # 直接写入UTF-8字节流到stdout
                    sys.stdout.buffer.write(output.encode('utf-8', errors='replace') + b'\n')
                    sys.stdout.buffer.flush()
                else:
                    print(output, **kwargs)
            except Exception as e:
                print(str(args), **kwargs)

        # 设置控制台编码
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='gbk', errors='replace', line_buffering=True)
                sys.stderr.reconfigure(encoding='gbk', errors='replace', line_buffering=True)
            except:
                pass

        # 基础内置函数
        self.global_env.define("print", zrl_print)
        self.global_env.define("input", input)
        self.global_env.define("len", len)
        self.global_env.define("range", range)
        self.global_env.define("str", str)
        self.global_env.define("int", int)
        self.global_env.define("float", float)
        self.global_env.define("type", type)
        
        # 数学函数
        self.global_env.define("abs", abs)
        self.global_env.define("round", round)
        self.global_env.define("min", min)
        self.global_env.define("max", max)
        self.global_env.define("sum", sum)
        self.global_env.define("pow", pow)
        self.global_env.define("sqrt", math.sqrt)
        self.global_env.define("sin", math.sin)
        self.global_env.define("cos", math.cos)
        self.global_env.define("tan", math.tan)
        self.global_env.define("pi", math.pi)
        self.global_env.define("e", math.e)
        
        # 时间函数
        self.global_env.define("time", time.time)
        self.global_env.define("sleep", time.sleep)
        self.global_env.define("now", lambda: str(datetime.now()))
        
        # 随机数函数
        self.global_env.define("random", random.random)
        self.global_env.define("randint", random.randint)
        self.global_env.define("choice", random.choice)
        self.global_env.define("random_int", lambda min_val, max_val: random.randint(min_val, max_val))
        self.global_env.define("random_float", random.random)
        self.global_env.define("random_range", lambda start, stop, step=1.0: random.uniform(start, stop))
        
        # sys模块
        class ZRLSys:
            version = sys.version
            platform = sys.platform
            argv = sys.argv
            path = sys.path
            exit = sys.exit
            getdefaultencoding = sys.getdefaultencoding
            getfilesystemencoding = sys.getfilesystemencoding
        
        self.global_env.define("sys", ZRLSys())
        
        # 字符串函数
        self.global_env.define("upper", str.upper)
        self.global_env.define("lower", str.lower)
        self.global_env.define("strip", str.strip)
        self.global_env.define("split", str.split)
        self.global_env.define("join", lambda sep, lst: sep.join(str(x) for x in lst))
        self.global_env.define("replace", lambda s, old, new: s.replace(old, new))
        self.global_env.define("reverse", lambda s: s[::-1])
        
        # 列表函数
        self.global_env.define("list", list)
        self.global_env.define("append", lambda lst, item: lst.append(item))
        self.global_env.define("pop", lambda lst: lst.pop())
        self.global_env.define("sort", lambda lst: lst.sort())
        self.global_env.define("reverse", lambda lst: lst.reverse())
        
        # 类型检查函数
        self.global_env.define("is_string", lambda x: isinstance(x, str))
        self.global_env.define("is_number", lambda x: isinstance(x, (int, float)))
        self.global_env.define("is_list", lambda x: isinstance(x, list))
        self.global_env.define("is_dict", lambda x: isinstance(x, dict))
        self.global_env.define("is_bool", lambda x: isinstance(x, bool))
        self.global_env.define("is_null", lambda x: x is None)
        
        # 更多数学函数
        self.global_env.define("log", math.log)
        self.global_env.define("log10", math.log10)
        self.global_env.define("log2", math.log2)
        self.global_env.define("ceil", math.ceil)
        self.global_env.define("floor", math.floor)
        self.global_env.define("radians", math.radians)
        self.global_env.define("degrees", math.degrees)
        self.global_env.define("exp", math.exp)
        self.global_env.define("fabs", math.fabs)
        self.global_env.define("factorial", math.factorial)
        self.global_env.define("gcd", math.gcd)
        self.global_env.define("lcm", math.lcm)
        
        # 更多列表/字典函数
        self.global_env.define("keys", lambda d: list(d.keys()))
        self.global_env.define("values", lambda d: list(d.values()))
        self.global_env.define("items", lambda d: list(d.items()))
        self.global_env.define("get_dict", lambda d, k, default=None: d.get(k, default) if isinstance(d, dict) else None)
        self.global_env.define("set_dict", lambda d, k, v: d.__setitem__(k, v) if isinstance(d, dict) else None)
        self.global_env.define("del_dict", lambda d, k: d.__delitem__(k) if isinstance(d, dict) else None)
        self.global_env.define("contains", lambda lst, item: item in lst)
        self.global_env.define("index", lambda lst, item: lst.index(item) if item in lst else -1)
        self.global_env.define("count", lambda lst, item: lst.count(item))
        self.global_env.define("slice", lambda lst, start, end: lst[start:end])
        self.global_env.define("get_item", lambda lst, idx: lst[idx] if 0 <= idx < len(lst) else None)
        self.global_env.define("set_item", lambda lst, idx, val: lst.__setitem__(idx, val) if 0 <= idx < len(lst) else None)
        self.global_env.define("extend", lambda lst1, lst2: lst1.extend(lst2))
        self.global_env.define("insert", lambda lst, idx, val: lst.insert(idx, val))
        self.global_env.define("remove", lambda lst, val: lst.remove(val) if val in lst else None)
        self.global_env.define("clear", lambda lst: lst.clear())
        
        # Python内置函数
        self.global_env.define("zip", lambda *iterables: list(zip(*iterables)))
        self.global_env.define("map", lambda func, iterable: list(map(func, iterable)))
        self.global_env.define("filter", lambda func, iterable: list(filter(func, iterable)))
        self.global_env.define("any", lambda iterable: any(iterable))
        self.global_env.define("all", lambda iterable: all(iterable))
        self.global_env.define("enumerate", lambda iterable: list(enumerate(iterable)))
        self.global_env.define("sorted", lambda iterable: sorted(iterable))
        self.global_env.define("reversed", lambda iterable: list(reversed(iterable)))
        self.global_env.define("hasattr", lambda obj, attr: hasattr(obj, attr))
        self.global_env.define("getattr", lambda obj, attr: getattr(obj, attr))
        self.global_env.define("setattr", lambda obj, attr, val: setattr(obj, attr, val))
        self.global_env.define("callable", lambda obj: callable(obj))
        self.global_env.define("hash", lambda obj: hash(obj))
        self.global_env.define("id", lambda obj: id(obj))
        self.global_env.define("hex", lambda obj: hex(obj))
        self.global_env.define("oct", lambda obj: oct(obj))
        self.global_env.define("bin", lambda obj: bin(obj))
        self.global_env.define("chr", lambda obj: chr(obj))
        self.global_env.define("ord", lambda obj: ord(obj))
        
        # 字典构造函数
        self.global_env.define("dict", lambda *args, **kwargs: dict(*args, **kwargs))
        
        # JSON支持
        import json
        self.global_env.define("json_loads", lambda s: json.loads(s))
        self.global_env.define("json_dumps", lambda obj, indent=None: json.dumps(obj, ensure_ascii=False, indent=indent))
        self.global_env.define("json_load", lambda f: json.load(f))
        self.global_env.define("json_dump", lambda obj, f, indent=None: json.dump(obj, f, ensure_ascii=False, indent=indent))
        
        # Base64支持
        import base64
        self.global_env.define("base64_encode", lambda s: base64.b64encode(s.encode('utf-8')).decode('utf-8'))
        self.global_env.define("base64_decode", lambda s: base64.b64decode(s).decode('utf-8'))
        self.global_env.define("base64_encode_bytes", lambda b: base64.b64encode(b).decode('utf-8'))
        self.global_env.define("base64_decode_bytes", lambda s: base64.b64decode(s))

    def interpret(self, program):
        try:
            for stmt in program.statements:
                self.execute(stmt, self.global_env)
            # 使用环境中的print函数
            print_func = self.global_env.get('print')
            print_func("Run Successful")
        except Exception as e:
            # 使用环境中的print函数
            print_func = self.global_env.get('print')
            print_func(f"Runtime Error: {e}")

    def execute(self, stmt, env):
        if isinstance(stmt, VarDecl):
            val = self.evaluate(stmt.value, env) if stmt.value else None
            env.define(stmt.name, val, stmt.is_const)
        elif isinstance(stmt, Assignment):
            val = self.evaluate(stmt.value, env)
            if isinstance(stmt.name, str):
                env.assign(stmt.name, val)
            elif isinstance(stmt.name, BinaryOp) and stmt.name.operator == '.':
                obj = self.evaluate(stmt.name.left, env)
                attr = stmt.name.right.name
                if isinstance(obj, ZRLInstance):
                    obj.set(attr, val)
                else:
                    setattr(obj, attr, val)
        elif isinstance(stmt, IfStmt):
            if self.evaluate(stmt.condition, env):
                self.execute_block(stmt.then_block, Environment(env))
            else:
                for elif_cond, elif_block in stmt.elif_blocks:
                    if self.evaluate(elif_cond, env):
                        self.execute_block(elif_block, Environment(env))
                        return
                if stmt.else_block:
                    self.execute_block(stmt.else_block, Environment(env))
        elif isinstance(stmt, WhileStmt):
            while self.evaluate(stmt.condition, env):
                self.execute_block(stmt.block, Environment(env))
        elif isinstance(stmt, ForStmt):
            iterable = self.evaluate(stmt.iterable, env)
            for item in iterable:
                new_env = Environment(env)
                new_env.define(stmt.item, item)
                self.execute_block(stmt.block, new_env)
        elif isinstance(stmt, FuncDef):
            func = ZRLFunction(stmt.name, stmt.params, stmt.block, env)
            env.define(stmt.name, func)
        elif isinstance(stmt, ClassDef):
            cls = ZRLClass(stmt.name, stmt.parent, stmt.methods, self.global_env)
            env.define(stmt.name, cls)
        elif isinstance(stmt, ReturnStmt):
            val = self.evaluate(stmt.value, env) if stmt.value else None
            raise ReturnException(val)
        elif isinstance(stmt, PrintStmt):
            vals = [self.evaluate(e, env) for e in stmt.expressions]
            print(*vals)
        elif isinstance(stmt, TryStmt):
            caught_exception = None
            # Execute try block
            try:
                self.execute_block(stmt.try_block, Environment(env))
            except Exception as e:
                caught_exception = e
                # Find matching except block
                handled = False
                for exc_type, exc_alias, except_block in stmt.except_blocks:
                    if exc_type is None or exc_type == type(e).__name__:
                        new_env = Environment(env)
                        if exc_alias:
                            new_env.define(exc_alias, str(e))
                        self.execute_block(except_block, new_env)
                        handled = True
                        break
                
                if not handled and caught_exception:
                    raise e
            
            # Execute else block if no exception was caught
            if not caught_exception and stmt.else_block:
                self.execute_block(stmt.else_block, Environment(env))
            
            # Execute finally block
            if stmt.finally_block:
                self.execute_block(stmt.finally_block, Environment(env))
        elif isinstance(stmt, ImportStmt):
            from zrl_stdlib import handle_import
            handle_import(stmt, env, self)
        elif isinstance(stmt, (FuncCall, BinaryOp, UnaryOp, Literal, Identifier, ListLiteral)):
            self.evaluate(stmt, env)

    def execute_block(self, block, env):
        for stmt in block:
            self.execute(stmt, env)

    def evaluate(self, expr, env):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, ListLiteral):
            return [self.evaluate(e, env) for e in expr.elements]
        elif isinstance(expr, DictLiteral):
            result = {}
            for key_expr, value_expr in expr.pairs:
                key = self.evaluate(key_expr, env)
                value = self.evaluate(value_expr, env)
                result[key] = value
            return result
        elif isinstance(expr, Identifier):
            return env.get(expr.name)
        elif isinstance(expr, UnaryOp):
            val = self.evaluate(expr.operand, env)
            if expr.operator == '-': return -val
            if expr.operator == 'not': return not val
            return val
        elif isinstance(expr, BinaryOp):
            if expr.operator == '.':
                left = self.evaluate(expr.left, env)
                right_name = expr.right.name
                if isinstance(left, ZRLInstance):
                    return left.get(right_name)
                return getattr(left, right_name)
            left = self.evaluate(expr.left, env)
            right = self.evaluate(expr.right, env)
            return self.apply_binary_op(left, expr.operator, right)
        elif isinstance(expr, FuncCall):
            func = self.evaluate(expr.func, env)
            args = [self.evaluate(arg, env) for arg in expr.args]
            if hasattr(func, 'call'):
                return func.call(self, args)
            return func(*args)
        return None

    def apply_binary_op(self, left, op, right):
        ops = {
            '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
            '%': operator.mod, '**': operator.pow, '==': operator.eq, '!=': operator.ne,
            '<': operator.lt, '>': operator.gt, '<=': operator.le, '>=': operator.ge,
            'and': lambda a, b: a and b, 'or': lambda a, b: a or b, 'in': lambda a, b: a in b
        }
        return ops[op](left, right)
