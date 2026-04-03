import re
import collections

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.indents = [0]
        self.line_num = 1
        self.line_start = 0

    def tokenize(self):
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),
            ('STRING',   r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'),
            ('COMMENT',  r'#.*'),
            ('KEYWORD',  r'\b(if|else|elif|for|while|func|return|import|as|from|class|self|true|false|null|var|const|and|or|not|in|try|except|finally|raise)\b'),
            ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OP_COMP',  r'==|!=|<=|>=|<|>'),
            ('OP_ASSIGN',r'[+\-*/%]=|='),
            ('OP_ARITH', r'\*\*|\+|\-|\*|\/|%'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('LBRACE',   r'\{'),
            ('RBRACE',   r'\}'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COLON',    r':'),
            ('COMMA',    r','),
            ('DOT',      r'\.'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        lines = self.code.split('\n')
        
        for line_idx, line in enumerate(lines):
            self.line_num = line_idx + 1
            if not line.strip() or line.strip().startswith('#'):
                continue
                
            # Handle Indentation
            stripped_line = line.lstrip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            indent = len(line) - len(stripped_line)
            if indent > self.indents[-1]:
                self.indents.append(indent)
                self.tokens.append(Token('INDENT', indent, self.line_num, 1))
            elif indent < self.indents[-1]:
                while indent < self.indents[-1]:
                    self.indents.pop()
                    self.tokens.append(Token('DEDENT', indent, self.line_num, 1))
                if indent != self.indents[-1]:
                    raise SyntaxError(f"Inconsistent indentation at line {self.line_num}")

            self.line_start = 0
            for mo in re.finditer(tok_regex, line):
                kind = mo.lastgroup
                value = mo.group()
                column = mo.start() + 1
                if kind == 'NUMBER':
                    value = float(value) if '.' in value else int(value)
                elif kind == 'STRING':
                    # 正确处理转义字符
                    value = value[1:-1]
                    # 处理常见的转义序列
                    escape_map = {
                        '\\n': '\n',
                        '\\t': '\t',
                        '\\r': '\r',
                        '\\"': '"',
                        "\\'": "'",
                        '\\\\': '\\',
                    }
                    for escape, char in escape_map.items():
                        value = value.replace(escape, char)
                elif kind == 'SKIP' or kind == 'COMMENT':
                    continue
                elif kind == 'MISMATCH':
                    raise SyntaxError(f'Unexpected character {value!r} at line {self.line_num}, column {column}')
                
                self.tokens.append(Token(kind, value, self.line_num, column))
            self.tokens.append(Token('NEWLINE', '\n', self.line_num, len(line)+1))

        # Final Dedents
        while len(self.indents) > 1:
            self.indents.pop()
            self.tokens.append(Token('DEDENT', 0, self.line_num, 1))
            
        return self.tokens
