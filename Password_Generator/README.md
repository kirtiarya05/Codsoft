# Secure Password Generator

A strong, customizable, and visually modern password generator with a GUI interface, built for the **Codsoft Internship - Task 3**.

## 🚀 Features
- **Modern GUI**: Built with Tkinter in a dark theme matching the Scientific Calculator.
- **Adjustable Length**: Use the slider to set password length (6-32 characters).
- **Complexity Control**: Toggle Uppercase, Numbers, and Symbols.
- **Strength Indicator**: Visual feedback (Red/Yellow/Green) based on entropy.
- **Secure Randomness**: Uses Python's `secrets` module for cryptographically strong generation.
- **One-Click Copy**: Easily copy your new password to the clipboard.

## 🛠️ Installation

1. Ensure you have Python installed.
2. Navigate to the project directory:
   ```bash
   cd Task3_PasswordGenerator
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the generator using:
```bash
python main.py
```

## 🔒 Security
This tool uses the `secrets` module which provides access to the most secure source of randomness that your operating system provides. Unlike the `random` module, `secrets` is suitable for managing secrets such as passwords and account authentication.

---
*Developed as part of the Codsoft Internship.*
