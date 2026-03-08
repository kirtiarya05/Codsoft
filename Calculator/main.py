import tkinter as tk
from tkinter import ttk, messagebox
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # Modern Dark Theme Colors
        self.bg_color = "#0F172A"      # Deep Navy
        self.display_bg = "#000000"    # Black
        self.btn_num_bg = "#1E293B"    # Lighter Navy
        self.btn_op_bg = "#334155"     # Slate
        self.btn_sci_bg = "#1E294B"    # Subtle Blue
        self.accent_color = "#9333EA"  # Purple
        self.text_color = "#FFFFFF"
        self.text_dim = "#94A3B8"
        
        self.root.configure(bg=self.bg_color)
        
        self.current_expr = ""
        self.history_expr = ""
        
        self._setup_ui()
        self._bind_keys()

    def _setup_ui(self):
        # Display Area
        self.display_frame = tk.Frame(self.root, bg=self.bg_color, pady=20, padx=20)
        self.display_frame.pack(fill="x")
        
        self.history_label = tk.Label(
            self.display_frame, text="", bg=self.bg_color, fg=self.text_dim,
            font=("JetBrains Mono", 12), anchor="e"
        )
        self.history_label.pack(fill="x")
        
        self.result_label = tk.Label(
            self.display_frame, text="0", bg=self.bg_color, fg=self.text_color,
            font=("JetBrains Mono", 32, "bold"), anchor="e"
        )
        self.result_label.pack(fill="x")

        # Keypad Area
        self.keypad_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=10)
        self.keypad_frame.pack(expand=True, fill="both")

        # Define Buttons (Label, Column, Row, Color, Function)
        buttons = [
            # Row 0: Scientific
            ("sin", 0, 0, self.btn_sci_bg, lambda: self._append_func("sin")),
            ("cos", 1, 0, self.btn_sci_bg, lambda: self._append_func("cos")),
            ("tan", 2, 0, self.btn_sci_bg, lambda: self._append_func("tan")),
            ("log", 3, 0, self.btn_sci_bg, lambda: self._append_func("log")),
            
            # Row 1
            ("AC", 0, 1, "#EF4444", self._clear),
            ("DEL", 1, 1, self.btn_op_bg, self._delete),
            ("%", 2, 1, self.btn_op_bg, lambda: self._append_op("/100")),
            ("÷", 3, 1, self.btn_op_bg, lambda: self._append_op("/")),
            
            # Row 2
            ("7", 0, 2, self.btn_num_bg, lambda: self._append_num("7")),
            ("8", 1, 2, self.btn_num_bg, lambda: self._append_num("8")),
            ("9", 2, 2, self.btn_num_bg, lambda: self._append_num("9")),
            ("×", 3, 2, self.btn_op_bg, lambda: self._append_op("*")),
            
            # Row 3
            ("4", 0, 3, self.btn_num_bg, lambda: self._append_num("4")),
            ("5", 1, 3, self.btn_num_bg, lambda: self._append_num("5")),
            ("6", 2, 3, self.btn_num_bg, lambda: self._append_num("6")),
            ("-", 3, 3, self.btn_op_bg, lambda: self._append_op("-")),
            
            # Row 4
            ("1", 0, 4, self.btn_num_bg, lambda: self._append_num("1")),
            ("2", 1, 4, self.btn_num_bg, lambda: self._append_num("2")),
            ("3", 2, 4, self.btn_num_bg, lambda: self._append_num("3")),
            ("+", 3, 4, self.btn_op_bg, lambda: self._append_op("+")),
            
            # Row 5
            ("e", 0, 5, self.btn_sci_bg, lambda: self._append_num(str(math.e))),
            ("0", 1, 5, self.btn_num_bg, lambda: self._append_num("0")),
            (".", 2, 5, self.btn_num_bg, lambda: self._append_num(".")),
            ("xʸ", 3, 5, self.btn_sci_bg, lambda: self._append_op("**")),
            
            # Row 6
            ("π", 0, 6, self.btn_sci_bg, lambda: self._append_num(str(math.pi))),
            ("√", 1, 6, self.btn_sci_bg, lambda: self._append_func("sqrt")),
            ("=", 2, 6, self.accent_color, self._calculate, 2) # Span 2 columns
        ]

        for btn in buttons:
            text, col, row, color, cmd = btn[:5]
            colspan = btn[5] if len(btn) > 5 else 1
            
            button = tk.Button(
                self.keypad_frame, text=text, bg=color, fg=self.text_color,
                font=("Outfit", 14, "bold"), borderwidth=0, activebackground=color,
                activeforeground=self.text_color, cursor="hand2", command=cmd
            )
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        # Configure weights for grid
        for i in range(4):
            self.keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.keypad_frame.grid_rowconfigure(i, weight=1)

    def _append_num(self, val):
        if self.current_expr == "0":
            self.current_expr = val
        else:
            self.current_expr += val
        self._update_display()

    def _append_op(self, op):
        if self.current_expr:
            self.current_expr += op
            self._update_display()

    def _append_func(self, func):
        if func == "sqrt":
            self.current_expr += "math.sqrt("
        else:
            self.current_expr += f"math.{func}(math.radians("
        self._update_display()

    def _clear(self):
        self.current_expr = ""
        self.history_expr = ""
        self._update_display()

    def _delete(self):
        self.current_expr = self.current_expr[:-1]
        self._update_display()

    def _calculate(self):
        try:
            # Handle closing brackets if missing
            temp_expr = self.current_expr
            open_brackets = temp_expr.count("(")
            close_brackets = temp_expr.count(")")
            if open_brackets > close_brackets:
                temp_expr += ")" * (open_brackets - close_brackets)

            result = eval(temp_expr)
            self.history_expr = self.current_expr + " ="
            
            # Format result
            if isinstance(result, float):
                self.current_expr = f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                self.current_expr = str(result)
                
            self._update_display()
        except Exception:
            self.result_label.config(text="Error")
            self.root.after(1000, lambda: self._update_display())

    def _update_display(self):
        # Display readable text in label
        display_text = self.current_expr.replace("math.", "").replace("radians(", "")
        self.result_label.config(text=display_text if display_text else "0")
        self.history_label.config(text=self.history_expr.replace("math.", "").replace("radians(", ""))

    def _bind_keys(self):
        self.root.bind("<Return>", lambda e: self._calculate())
        self.root.bind("<BackSpace>", lambda e: self._delete())
        self.root.bind("<Escape>", lambda e: self._clear())
        for char in "0123456789.+-*/%":
            self.root.bind(char, lambda e, c=char: self._append_num(c) if c.isdigit() or c == "." else self._append_op(c))

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
