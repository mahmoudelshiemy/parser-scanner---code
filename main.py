import tkinter as tk
from tkinter import scrolledtext
from scanner import LexicalAnalyzer
from parser import Parser

def analyze():
    input_text = entry.get("1.0", tk.END)

    lexer = LexicalAnalyzer(input_text)
    tokens = []

    output_text.delete("1.0", tk.END)

    while True:
        tok = lexer.get_next_token()
        if tok.type == 'EOF':
            break
        tokens.append(tok)
        output_text.insert(tk.END, f"<Token {tok.type}, {tok.value}>\n")

    parser = Parser(tokens)
    try:
        parser.parse()
        output_text.insert(tk.END, "\nParse Result: VALID\n")
    except SyntaxError as e:
        output_text.insert(tk.END, f"\nParse Result: INVALID → {e}\n")


root = tk.Tk()
root.title("Scanner + Recursive Descent Parser")

entry = scrolledtext.ScrolledText(root, width=80, height=10)
entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze Code", command=analyze)
analyze_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=80, height=25)
output_text.pack(pady=10)

root.mainloop()
