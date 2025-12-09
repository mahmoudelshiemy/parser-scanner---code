import re

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.col})"

class LexicalAnalyzer:
    def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0
        self.current_char = input_text[0] if input_text else None
        
        self.line = 1
        self.col = 1

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1

        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None

    def peek(self):
        nxt = self.position + 1
        if nxt < len(self.input):
            return self.input[nxt]
        return None

    def emit(self, type_, value):
        return Token(type_, value, self.line, self.col)

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            return True

        if self.current_char == '/' and self.peek() == '*':
            self.advance(); self.advance()
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance(); self.advance()
                    break
                self.advance()
            return True
        return False

    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char == '/' and self.peek() in ['/', '*']:
                self.skip_comment()
                continue

            # IDENTIFIER or KEYWORD
            if self.current_char.isalpha() or self.current_char == '_':
                start_line, start_col = self.line, self.col
                lexeme = ""

                while (
                    self.current_char is not None and 
                    (self.current_char.isalnum() or self.current_char == '_')
                ):
                    lexeme += self.current_char
                    self.advance()

                keywords = [
                    'int','float','double','char',
                    'if','else','while','for','return'
                ]

                if lexeme in keywords:
                    return Token('KEYWORD', lexeme, start_line, start_col)
                return Token('IDENTIFIER', lexeme, start_line, start_col)

            # NUMBER
            if self.current_char.isdigit() or (self.current_char == '.' and self.peek() and self.peek().isdigit()):
                start_line, start_col = self.line, self.col
                num = ""
                dot_count = 0

                while (
                    self.current_char is not None and 
                    (self.current_char.isdigit() or self.current_char == '.')
                ):
                    if self.current_char == '.':
                        dot_count += 1
                        if dot_count > 1:
                            break
                    num += self.current_char
                    self.advance()

                return Token('NUMBER', num, start_line, start_col)

            # OPERATORS
            if self.current_char in '+-*/%=<>!&|':
                start_line, start_col = self.line, self.col
                op = self.current_char
                self.advance()

                if op in ['<', '>', '!', '=', '+', '-', '*', '/', '%', '|', '&'] and self.current_char == '=':
                    op += self.current_char
                    self.advance()
                elif op in ['&', '|'] and self.current_char == op:
                    op += self.current_char
                    self.advance()
                elif op in ['+', '-'] and self.current_char == op:
                    op += self.current_char
                    self.advance()

                return Token('OPERATOR', op, start_line, start_col)

            # SPECIAL SYMBOL
            start_line, start_col = self.line, self.col
            char = self.current_char
            self.advance()
            return Token('SPECIAL', char, start_line, start_col)

        return Token('EOF', None, self.line, self.col)

