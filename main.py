import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import secrets
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        
        # Modern Dark Theme Colors (Matching your Calculator theme)
        self.bg_color = "#0F172A"      # Deep Navy
        self.card_bg = "#1E293B"       # Lighter Navy
        self.accent_color = "#9333EA"  # Purple
        self.secondary_accent = "#3B82F6" # Blue
        self.text_color = "#FFFFFF"
        self.text_dim = "#94A3B8"
        self.success_color = "#10B981" # Green
        
        self.root.configure(bg=self.bg_color)
        
        self._setup_ui()

    def _setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=30)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, text="PASSWORD GENERATOR", 
            bg=self.bg_color, fg=self.accent_color,
            font=("Outfit", 20, "bold")
        ).pack()
        
        tk.Label(
            header_frame, text="Generate strong, secure passwords instantly", 
            bg=self.bg_color, fg=self.text_dim,
            font=("Outfit", 10)
        ).pack()

        # Main Container
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=30)
        main_frame.pack(fill="both", expand=True)

        # Result Display Area
        self.result_var = tk.StringVar(value="Click Generate")
        result_container = tk.Frame(main_frame, bg=self.card_bg, padx=15, pady=20)
        result_container.pack(fill="x", pady=(0, 20))
        
        self.result_label = tk.Label(
            result_container, textvariable=self.result_var, 
            bg=self.card_bg, fg=self.text_color,
            font=("JetBrains Mono", 16, "bold"), wraplength=350
        )
        self.result_label.pack()

        # Strength Indicator
        self.strength_var = tk.StringVar(value="")
        self.strength_label = tk.Label(
            main_frame, textvariable=self.strength_var,
            bg=self.bg_color, font=("Outfit", 10, "bold")
        )
        self.strength_label.pack(pady=(0, 20))

        # Controls
        controls_frame = tk.Frame(main_frame, bg=self.bg_color)
        controls_frame.pack(fill="x")

        # Length Slider
        tk.Label(
            controls_frame, text="Password Length", 
            bg=self.bg_color, fg=self.text_color, font=("Outfit", 11)
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(
            controls_frame, from_=6, to_=32, orient="horizontal",
            variable=self.length_var, bg=self.bg_color, fg=self.text_color,
            highlightthickness=0, troughcolor=self.card_bg, activebackground=self.accent_color,
            font=("Outfit", 10)
        )
        self.length_slider.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        # Options (Checkboxes)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self._create_checkbox(controls_frame, "Include Uppercase (A-Z)", self.use_upper, 2)
        self._create_checkbox(controls_frame, "Include Numbers (0-9)", self.use_digits, 3)
        self._create_checkbox(controls_frame, "Include Symbols (!@#$)", self.use_symbols, 4)

        # Action Buttons
        btn_frame = tk.Frame(main_frame, bg=self.bg_color, pady=20)
        btn_frame.pack(fill="x", side="bottom")

        generate_btn = tk.Button(
            btn_frame, text="GENERATE PASSWORD", bg=self.accent_color, fg=self.text_color,
            font=("Outfit", 12, "bold"), borderwidth=0, cursor="hand2",
            activebackground="#7E22CE", activeforeground=self.text_color,
            padx=20, pady=12, command=self._generate
        )
        generate_btn.pack(fill="x", pady=(0, 10))

        copy_btn = tk.Button(
            btn_frame, text="COPY TO CLIPBOARD", bg=self.card_bg, fg=self.secondary_accent,
            font=("Outfit", 11, "bold"), borderwidth=1, highlightbackground=self.secondary_accent,
            cursor="hand2", activebackground="#2D3748", activeforeground=self.secondary_accent,
            padx=20, pady=10, command=self._copy
        )
        copy_btn.pack(fill="x")

    def _create_checkbox(self, parent, text, variable, row):
        cb = tk.Checkbutton(
            parent, text=text, variable=variable, bg=self.bg_color, fg=self.text_color,
            selectcolor=self.bg_color, activebackground=self.bg_color, activeforeground=self.text_color,
            font=("Outfit", 10), borderwidth=0, highlightthickness=0
        )
        cb.grid(row=row, column=0, sticky="w", pady=5)

    def _generate(self):
        length = self.length_var.get()
        chars = string.ascii_lowercase
        
        required_chars = [secrets.choice(string.ascii_lowercase)]
        
        if self.use_upper.get():
            chars += string.ascii_uppercase
            required_chars.append(secrets.choice(string.ascii_uppercase))
        if self.use_digits.get():
            chars += string.digits
            required_chars.append(secrets.choice(string.digits))
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            required_chars.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))

        # Fill the rest of the length
        remaining_length = length - len(required_chars)
        password_list = required_chars + [secrets.choice(chars) for _ in range(remaining_length)]
        
        # Shuffle result
        random.shuffle(password_list)
        password = "".join(password_list)
        
        self.result_var.set(password)
        self._update_strength(password)

    def _update_strength(self, password):
        score = 0
        if len(password) >= 12: score += 2
        elif len(password) >= 8: score += 1
        
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
        
        if score <= 2:
            self.strength_var.set("Strength: WEAK")
            self.strength_label.config(fg="#EF4444")
        elif score <= 4:
            self.strength_var.set("Strength: MODERATE")
            self.strength_label.config(fg="#F59E0B")
        else:
            self.strength_var.set("Strength: STRONG")
            self.strength_label.config(fg=self.success_color)

    def _copy(self):
        password = self.result_var.get()
        if password and password != "Click Generate":
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate a password first!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
