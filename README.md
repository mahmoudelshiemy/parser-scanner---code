Compiler Project – Scanner & Recursive Descent Parser
Overview:
This project implements:
1. Lexical Analyzer (Scanner)
2. Recursive Descent Parser
For a simplified C-like language. The system detects syntax errors with line & column numbers.
Features:
Scanner:
- Tokenizes KEYWORD, IDENTIFIER, NUMBER, OPERATOR, SPECIAL
- Supports // and /* */ comments
- Tracks line and column
Parser:
- Implements grammar for: int main(), declarations, assignments, if/else, while, for, return
- Recursive Descent functions for each rule
- Detailed syntax errors with line & column
Grammar Summary:
FUNC ® int main ( ) BLOCK
BLOCK ® { STMT_LIST }
STMT_LIST ® STMT STMT_LIST | e
STMT ® DECL | IF | WHILE | FOR | RETURN | EXPR ;
DECL ® DATATYPE ID_LIST [ = VALUE ] ;
DATATYPE ® int | float | double | char
IF ® if ( EXPR ) ST_OR_BLOCK [ else ST_OR_BLOCK ]
WHILE ® while ( EXPR ) ST_OR_BLOCK
FOR ® for ( INIT ; EXPR ; EXPR ) ST_OR_BLOCK
RETURN ® return EXPR ;
EXPR ® VALUE ( OP VALUE )*
VALUE ® id | number
Project Structure:
scanner.py – Lexical Analyzer
parser.py – Recursive Descent Parser
main.py – GUI and integration
README.md – Documentation
Run Instructions:
python main.py
Example Valid Code:
int main() {
int x, y;
if (x == 10) {
y = x + 5;
} else {
y = 3.1;
}
return y;
}
Example Invalid Code:
int main() {
if (x == 10 {
y = 5;
}
}
Error Output:
Expected SPECIAL ) but found SPECIAL:{ at line 2, col 17
