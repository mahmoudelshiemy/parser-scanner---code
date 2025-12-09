import tkinter as tk
from tkinter import scrolledtext

from scanner import LexicalAnalyzer
from parser import Parser


def analyze():
    """Run scanner + parser on the code from the input box."""
    code = entry.get("1.0", tk.END)

    lexer = LexicalAnalyzer(code)
    tokens = []

    # Clear previous output
    output_text.delete("1.0", tk.END)

    # ---------- Scanner phase ----------
    output_text.insert(tk.END, "Tokens:\n")

    while True:
        tok = lexer.get_next_token()
        if tok.type == 'EOF':
            break

        tokens.append(tok)
        output_text.insert(
            tk.END,
            f"  Token(type={tok.type}, value={tok.value}, "
            f"line={tok.line}, col={tok.col})\n"
        )

    # ---------- Parser phase ----------
    output_text.insert(tk.END, "\nParser result:\n")

    parser = Parser(tokens)
    try:
        parser.parse()
        output_text.insert(tk.END, "  VALID (no syntax errors)\n")
    except SyntaxError as e:
        output_text.insert(tk.END, f"  INVALID → {e}\n")


def main():
    global entry, output_text

    root = tk.Tk()
    root.title("Scanner + Recursive Descent Parser")

    # Input code box
    entry = scrolledtext.ScrolledText(root, width=80, height=10)
    entry.pack(pady=10)

    # Analyze button
    analyze_button = tk.Button(root, text="Analyze Code", command=analyze)
    analyze_button.pack(pady=5)

    # Output box (tokens + parse result)
    output_text = scrolledtext.ScrolledText(root, width=100, height=25)
    output_text.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
