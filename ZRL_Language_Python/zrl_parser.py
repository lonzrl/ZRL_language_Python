from zrl_lexer import Lexer, Token

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, name, value, is_const=False):
        self.name = name
        self.value = value
        self.is_const = is_const

class Assignment(ASTNode):
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class DictLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs  # list of (key, value) tuples

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class IfStmt(ASTNode):
    def __init__(self, condition, then_block, elif_blocks=None, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.elif_blocks = elif_blocks or []
        self.else_block = else_block

class WhileStmt(ASTNode):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class ForStmt(ASTNode):
    def __init__(self, item, iterable, block):
        self.item = item
        self.iterable = iterable
        self.block = block

class FuncDef(ASTNode):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block

class ClassDef(ASTNode):
    def __init__(self, name, parent, methods):
        self.name = name
        self.parent = parent
        self.methods = methods

class FuncCall(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class ReturnStmt(ASTNode):
    def __init__(self, value):
        self.value = value

class TryStmt(ASTNode):
    def __init__(self, try_block, except_blocks, else_block=None, finally_block=None):
        self.try_block = try_block
        self.except_blocks = except_blocks  # list of (exception_type, alias, block)
        self.else_block = else_block
        self.finally_block = finally_block

class ImportStmt(ASTNode):
    def __init__(self, module_name, alias=None, from_import=None):
        self.module_name = module_name
        self.alias = alias
        self.from_import = from_import

class PrintStmt(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type} at line {token.line}")
        if expected_value and token.value != expected_value:
            raise SyntaxError(f"Expected value {expected_value}, got {token.value} at line {token.line}")
        self.pos += 1
        return token

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            if self.peek().type == 'NEWLINE':
                self.consume()
                continue
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.peek()
        if token.type == 'KEYWORD':
            if token.value == 'var' or token.value == 'const':
                return self.parse_var_decl()
            elif token.value == 'if':
                return self.parse_if()
            elif token.value == 'while':
                return self.parse_while()
            elif token.value == 'for':
                return self.parse_for()
            elif token.value == 'func':
                return self.parse_func_def()
            elif token.value == 'class':
                return self.parse_class_def()
            elif token.value == 'return':
                return self.parse_return()
            elif token.value == 'import' or token.value == 'from':
                return self.parse_import()
            elif token.value == 'print':
                return self.parse_print()
            elif token.value == 'try':
                return self.parse_try()
        
        expr = self.parse_expression()
        if self.peek() and self.peek().type == 'OP_ASSIGN':
            op = self.consume().value
            value = self.parse_expression()
            if isinstance(expr, Identifier):
                return Assignment(expr.name, op, value)
            elif isinstance(expr, BinaryOp) and expr.operator == '.':
                return Assignment(expr, op, value)
        return expr

    def parse_var_decl(self):
        is_const = self.consume().value == 'const'
        name = self.consume('ID').value
        value = None
        if self.peek() and self.peek().type == 'OP_ASSIGN' and self.peek().value == '=':
            self.consume()
            value = self.parse_expression()
        return VarDecl(name, value, is_const)

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'or':
            op = self.consume().value
            right = self.parse_logical_and()
            node = BinaryOp(node, op, right)
        return node

    def parse_logical_and(self):
        node = self.parse_comparison()
        while self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'and':
            op = self.consume().value
            right = self.parse_comparison()
            node = BinaryOp(node, op, right)
        return node

    def parse_comparison(self):
        node = self.parse_arithmetic()
        while self.peek() and self.peek().type == 'OP_COMP':
            op = self.consume().value
            right = self.parse_arithmetic()
            node = BinaryOp(node, op, right)
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.peek() and self.peek().type == 'OP_ARITH' and self.peek().value in ('+', '-'):
            op = self.consume().value
            right = self.parse_term()
            node = BinaryOp(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type == 'OP_ARITH' and self.peek().value in ('*', '/', '%', '**'):
            op = self.consume().value
            right = self.parse_factor()
            node = BinaryOp(node, op, right)
        return node

    def parse_factor(self):
        token = self.peek()
        if token.type == 'OP_ARITH' and token.value in ('+', '-'):
            op = self.consume().value
            return UnaryOp(op, self.parse_factor())
        elif token.type == 'KEYWORD' and token.value == 'not':
            op = self.consume().value
            return UnaryOp(op, self.parse_factor())
        return self.parse_primary()

    def parse_primary(self):
        token = self.consume()
        if token.type == 'NUMBER':
            node = Literal(token.value)
        elif token.type == 'STRING':
            node = Literal(token.value)
        elif token.type == 'KEYWORD':
            if token.value == 'true': node = Literal(True)
            elif token.value == 'false': node = Literal(False)
            elif token.value == 'null': node = Literal(None)
            elif token.value == 'self': node = Identifier('self')
            else: raise SyntaxError(f"Unexpected keyword {token.value}")
        elif token.type == 'ID':
            node = Identifier(token.value)
        elif token.type == 'LPAREN':
            node = self.parse_expression()
            self.consume('RPAREN')
        elif token.type == 'LBRACKET':
            elements = []
            if self.peek().type != 'RBRACKET':
                elements.append(self.parse_expression())
                while self.peek().type == 'COMMA':
                    self.consume()
                    elements.append(self.parse_expression())
            self.consume('RBRACKET')
            node = ListLiteral(elements)
        elif token.type == 'LBRACE':
            pairs = []
            if self.peek().type != 'RBRACE':
                # 解析 key: value
                key = self.parse_expression()
                self.consume('COLON')
                value = self.parse_expression()
                pairs.append((key, value))
                while self.peek().type == 'COMMA':
                    self.consume()
                    key = self.parse_expression()
                    self.consume('COLON')
                    value = self.parse_expression()
                    pairs.append((key, value))
            self.consume('RBRACE')
            node = DictLiteral(pairs)
        else:
            raise SyntaxError(f"Unexpected token {token.type} ({token.value}) at line {token.line}")

        while self.peek():
            if self.peek().type == 'LPAREN':
                self.consume()
                args = []
                if self.peek().type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.peek().type == 'COMMA':
                        self.consume()
                        args.append(self.parse_expression())
                self.consume('RPAREN')
                node = FuncCall(node, args)
            elif self.peek().type == 'DOT':
                self.consume()
                attr = self.consume('ID').value
                node = BinaryOp(node, '.', Identifier(attr))
            else:
                break
        return node

    def parse_block(self):
        self.consume('COLON')
        statements = []
        if self.peek() and self.peek().type == 'NEWLINE':
            self.consume('NEWLINE')
            self.consume('INDENT')
            while self.peek() and self.peek().type != 'DEDENT':
                if self.peek().type == 'NEWLINE':
                    self.consume()
                    continue
                statements.append(self.parse_statement())
            self.consume('DEDENT')
        else:
            statements.append(self.parse_statement())
        return statements

    def parse_if(self):
        self.consume() # if
        condition = self.parse_expression()
        then_block = self.parse_block()
        elif_blocks = []
        else_block = None
        while self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'elif':
            self.consume() # elif
            elif_cond = self.parse_expression()
            elif_stmt = self.parse_block()
            elif_blocks.append((elif_cond, elif_stmt))
        if self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'else':
            self.consume() # else
            else_block = self.parse_block()
        return IfStmt(condition, then_block, elif_blocks, else_block)

    def parse_while(self):
        self.consume()
        condition = self.parse_expression()
        block = self.parse_block()
        return WhileStmt(condition, block)

    def parse_for(self):
        self.consume()
        item = self.consume('ID').value
        self.consume('KEYWORD', 'in')
        iterable = self.parse_expression()
        block = self.parse_block()
        return ForStmt(item, iterable, block)

    def parse_func_def(self):
        self.consume()
        name = self.consume('ID').value
        self.consume('LPAREN')
        params = []
        if self.peek().type == 'ID':
            params.append(self.consume().value)
            while self.peek().type == 'COMMA':
                self.consume()
                params.append(self.consume('ID').value)
        self.consume('RPAREN')
        block = self.parse_block()
        return FuncDef(name, params, block)

    def parse_class_def(self):
        self.consume()
        name = self.consume('ID').value
        parent = None
        if self.peek().type == 'LPAREN':
            self.consume()
            parent = self.consume('ID').value
            self.consume('RPAREN')
        self.consume('COLON')
        self.consume('NEWLINE')
        self.consume('INDENT')
        methods = {}
        while self.peek() and self.peek().type != 'DEDENT':
            if self.peek().type == 'NEWLINE':
                self.consume()
                continue
            if self.peek().type == 'KEYWORD' and self.peek().value == 'func':
                method = self.parse_func_def()
                methods[method.name] = method
            else:
                self.consume() # Skip other things in class for now
        self.consume('DEDENT')
        return ClassDef(name, parent, methods)

    def parse_return(self):
        self.consume()
        value = None
        if self.peek().type not in ('NEWLINE', 'DEDENT', None):
            value = self.parse_expression()
        return ReturnStmt(value)

    def parse_print(self):
        self.consume()
        self.consume('LPAREN')
        exprs = [self.parse_expression()]
        while self.peek() and self.peek().type == 'COMMA':
            self.consume()
            exprs.append(self.parse_expression())
        self.consume('RPAREN')
        return PrintStmt(exprs)

    def parse_try(self):
        self.consume()  # try
        try_block = self.parse_block()
        except_blocks = []
        
        # Parse except blocks
        while self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'except':
            self.consume()  # except
            exc_type = None
            exc_alias = None
            
            # Check for exception type
            if self.peek().type == 'ID':
                exc_type = self.consume().value
                # Check for alias
                if self.peek().type == 'ID' and self.peek().value == 'as':
                    self.consume()
                    exc_alias = self.consume('ID').value
            
            except_block = self.parse_block()
            except_blocks.append((exc_type, exc_alias, except_block))
        
        # Parse else block
        else_block = None
        if self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'else':
            self.consume()
            else_block = self.parse_block()
        
        # Parse finally block
        finally_block = None
        if self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'finally':
            self.consume()
            finally_block = self.parse_block()
        
        return TryStmt(try_block, except_blocks, else_block, finally_block)

    def parse_import(self):
        token = self.consume()
        if token.value == 'import':
            module_name = self.consume('ID').value
            alias = None
            if self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'as':
                self.consume()
                alias = self.consume('ID').value
            return ImportStmt(module_name, alias)
        else:
            module_name = self.consume('ID').value
            self.consume('KEYWORD', 'import')
            from_import = self.consume('ID').value
            alias = None
            if self.peek() and self.peek().type == 'KEYWORD' and self.peek().value == 'as':
                self.consume()
                alias = self.consume('ID').value
            return ImportStmt(module_name, alias, from_import)
