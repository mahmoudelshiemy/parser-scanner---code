from scanner import Token

class Parser:
    def __init__(self, tokens):
        """
        tokens: list[Token] coming from the scanner.
        Each token contains: type, value, line, col
        """
        self.tokens = list(tokens)

        # Add EOF token with the last known line/col
        if self.tokens:
            last = self.tokens[-1]
            eof_token = Token('EOF', 'EOF', last.line, last.col)
        else:
            eof_token = Token('EOF', 'EOF', 1, 1)

        self.tokens.append(eof_token)

        self.pos = 0
        self.current = self.tokens[0]

        # Supported datatypes
        self.datatypes = {'int', 'float', 'double', 'char'}

        # Supported operators inside expressions
        self.ops = {
            '+', '-', '*', '/', '=', '%', '<', '>', '|', '&',
            '>=', '<=', '==', '&&', '||',
            '+=', '-=', '*=', '/=', '%=', '|=', '&='
        }

    # ================== Helpers ==================

    def advance(self):
        """Move to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            # Safety: stay at last token (EOF)
            self.current = self.tokens[-1]

    def match(self, type_=None, value=None):
        """
        Try matching the current token with expected type/value.
        If match succeeds → consume token and return True.
        If match fails → return False without throwing errors.
        """
        if type_ is not None and self.current.type != type_:
            return False
        if value is not None and self.current.value != value:
            return False
        self.advance()
        return True

    def expect(self, type_=None, value=None):
        """
        Same as match() but throws SyntaxError if token does not match.
        Includes line/column for error reporting.
        """
        if not self.match(type_, value):
            raise SyntaxError(
                f"Expected {type_} {value}, but found "
                f"{self.current.type}:{self.current.value} "
                f"at line {self.current.line}, col {self.current.col}"
            )

    # ================== Entry Point ==================

    def parse(self):
        """Program → sequence of statements until EOF."""
        while self.current.type != 'EOF':
            self.statement()

    # ================== Statement Dispatcher ==================

    def statement(self):
        t, v = self.current.type, self.current.value

        # FUNC → int main() BLOCK
        if t == 'KEYWORD' and v == 'int' and self._is_func_main():
            self.func()

        # DECLARATION
        elif t == 'KEYWORD' and v in self.datatypes:
            self.declaration()

        # IF STATEMENT
        elif t == 'KEYWORD' and v == 'if':
            self.if_statement()

        # WHILE LOOP
        elif t == 'KEYWORD' and v == 'while':
            self.while_statement()

        # FOR LOOP
        elif t == 'KEYWORD' and v == 'for':
            self.for_statement()

        # RETURN STATEMENT
        elif t == 'KEYWORD' and v == 'return':
            self.return_statement()

        # BLOCK
        elif t == 'SPECIAL' and v == '{':
            self.block()

        # EXPRESSION statement: value or variable
        elif t in ('IDENTIFIER', 'NUMBER'):
            self.expression()
            self.expect('SPECIAL', ';')

        else:
            raise SyntaxError(
                f"Unexpected token {self.current.type}:{self.current.value} "
                f"at line {self.current.line}, col {self.current.col}"
            )

    def _is_func_main(self):
        """
        Look ahead to check if the pattern matches:
        int main ( ) {
        Used to distinguish function declaration from normal int usage.
        """
        if self.pos + 4 >= len(self.tokens):
            return False

        t1, v1 = self.tokens[self.pos + 1].type, self.tokens[self.pos + 1].value
        t2, v2 = self.tokens[self.pos + 2].type, self.tokens[self.pos + 2].value
        t3, v3 = self.tokens[self.pos + 3].type, self.tokens[self.pos + 3].value
        t4, v4 = self.tokens[self.pos + 4].type, self.tokens[self.pos + 4].value

        return (
            t1 == 'IDENTIFIER' and v1 == 'main' and
            t2 == 'SPECIAL' and v2 == '(' and
            t3 == 'SPECIAL' and v3 == ')' and
            t4 == 'SPECIAL' and v4 == '{'
        )

    # ================== Grammar Rules ==================

    def func(self):
        """FUNC → int main ( ) BLOCK"""
        self.expect('KEYWORD', 'int')
        self.expect('IDENTIFIER', 'main')
        self.expect('SPECIAL', '(')
        self.expect('SPECIAL', ')')
        self.block()

    def block(self):
        """BLOCK → { statements }"""
        self.expect('SPECIAL', '{')

        while not (self.current.type == 'SPECIAL' and self.current.value == '}'):
            if self.current.type == 'EOF':
                raise SyntaxError(
                    f"Unexpected EOF inside block at "
                    f"line {self.current.line}, col {self.current.col}"
                )
            self.statement()

        self.expect('SPECIAL', '}')

    def datatype(self):
        """DATATYPE → int | float | double | char"""
        if self.current.type == 'KEYWORD' and self.current.value in self.datatypes:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected datatype, found {self.current.type}:{self.current.value} "
                f"at line {self.current.line}, col {self.current.col}"
            )

    def value(self):
        """VALUE → IDENTIFIER | NUMBER"""
        if self.current.type in ('IDENTIFIER', 'NUMBER'):
            self.advance()
        else:
            raise SyntaxError(
                f"Expected identifier/number, found {self.current.type}:{self.current.value} "
                f"at line {self.current.line}, col {self.current.col}"
            )

    def declaration(self):
        """
        DECLARATION:
        DATATYPE id (',' id)* [ = VALUE ] ;
        """
        self.datatype()
        self.expect('IDENTIFIER')

        while self.match('SPECIAL', ','):
            self.expect('IDENTIFIER')

        # Optional initialization
        if self.match('OPERATOR', '='):
            self.value()

        self.expect('SPECIAL', ';')

    def op(self):
        """Operator used inside expressions."""
        if self.current.type == 'OPERATOR' and self.current.value in self.ops:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected operator, found {self.current.type}:{self.current.value} "
                f"at line {self.current.line}, col {self.current.col}"
            )

    def expression(self):
        """EXPRESSION → VALUE (OP VALUE)*"""
        self.value()
        while self.current.type == 'OPERATOR' and self.current.value in self.ops:
            self.op()
            self.value()

    # IF → if ( EXPR ) statement_or_block [ else statement_or_block ]
    def if_statement(self):
        self.expect('KEYWORD', 'if')
        self.expect('SPECIAL', '(')
        self.expression()
        self.expect('SPECIAL', ')')
        self.statement_or_block()

        # Optional else
        if self.match('KEYWORD', 'else'):
            self.statement_or_block()

    def statement_or_block(self):
        """Choose between single statement or block."""
        if self.current.type == 'SPECIAL' and self.current.value == '{':
            self.block()
        else:
            self.statement()

    # WHILE → while ( EXPR ) statement_or_block
    def while_statement(self):
        self.expect('KEYWORD', 'while')
        self.expect('SPECIAL', '(')
        self.expression()
        self.expect('SPECIAL', ')')
        self.statement_or_block()

    # FOR → for ( INIT ; COND ; UPDATE ) statement_or_block
    def for_statement(self):
        self.expect('KEYWORD', 'for')
        self.expect('SPECIAL', '(')

        # INIT
        if self.current.type == 'KEYWORD' and self.current.value in self.datatypes:
            self.declaration_in_for()
        else:
            self.simple_assignment_in_for()

        self.expect('SPECIAL', ';')

        # CONDITION
        self.expression()
        self.expect('SPECIAL', ';')

        # UPDATE
        self.expression()

        self.expect('SPECIAL', ')')
        self.statement_or_block()

    def declaration_in_for(self):
        """Datatype-based initialization inside for loop."""
        self.datatype()
        self.expect('IDENTIFIER')
        self.expect('OPERATOR', '=')
        self.value()

    def simple_assignment_in_for(self):
        """Simple assignment inside for loop."""
        self.expect('IDENTIFIER')
        self.expect('OPERATOR', '=')
        self.value()

    def return_statement(self):
        """RETURN → return EXPR ;"""
        self.expect('KEYWORD', 'return')
        self.expression()
        self.expect('SPECIAL', ';')
