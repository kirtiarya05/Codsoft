import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Modern Dark Theme Colors
        self.bg_color = "#0F172A"      # Deep Navy
        self.card_bg = "#1E293B"       # Lighter Navy
        self.accent_color = "#9333EA"  # Purple
        self.secondary_accent = "#3B82F6" # Blue
        self.text_color = "#FFFFFF"
        self.text_dim = "#94A3B8"
        self.error_color = "#F43F5E"   # Rose
        self.success_color = "#10B981" # Green
        
        self.root.configure(bg=self.bg_color)
        
        # File Path for Persistence
        self.data_file = "contacts.json"
        self.contacts = self._load_contacts()
        self.selected_contact_index = None

        self._setup_ui()
        self._refresh_list()

    def _load_contacts(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_contacts(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.bg_color, pady=20)
        header.pack(fill="x")
        
        tk.Label(
            header, text="CONTACT MANAGER", 
            bg=self.bg_color, fg=self.accent_color,
            font=("Outfit", 20, "bold")
        ).pack()

        # Main Layout Container
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=10)
        main_container.pack(fill="both", expand=True)

        # LEFT PANEL: Search and List
        left_panel = tk.Frame(main_container, bg=self.bg_color, width=400)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Search Bar
        search_frame = tk.Frame(left_panel, bg=self.card_bg, padx=10, pady=5)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="🔍", bg=self.card_bg, fg=self.text_dim).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._refresh_list())
        self.search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, 
            bg=self.card_bg, fg=self.text_color, borderwidth=0,
            insertbackground=self.text_color, font=("Outfit", 11)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Scrollable Contact List (Treeview)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
            background=self.card_bg, foreground=self.text_color, 
            fieldbackground=self.card_bg, borderwidth=0, font=("Outfit", 10))
        style.map("Treeview", background=[('selected', self.accent_color)])
        style.configure("Treeview.Heading", background=self.bg_color, foreground=self.text_dim, borderwidth=0, font=("Outfit", 10, "bold"))

        self.tree = ttk.Treeview(left_panel, columns=("Name", "Phone"), show="headings")
        self.tree.heading("Name", text="NAME")
        self.tree.heading("Phone", text="PHONE")
        self.tree.column("Name", width=200)
        self.tree.column("Phone", width=150)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # RIGHT PANEL: Details & Form
        self.right_panel = tk.Frame(main_container, bg=self.card_bg, padx=30, pady=30, width=400)
        self.right_panel.pack(side="right", fill="both")
        self.right_panel.pack_propagate(False)

        # Form Fields
        self.fields = {}
        for idx, (label, key) in enumerate([("Full Name", "name"), ("Phone Number", "phone"), ("Email Address", "email"), ("Physical Address", "address")]):
            tk.Label(self.right_panel, text=label, bg=self.card_bg, fg=self.text_dim, font=("Outfit", 9, "bold")).pack(anchor="w", pady=(10, 2))
            entry = tk.Entry(
                self.right_panel, bg=self.bg_color, fg=self.text_color, 
                borderwidth=0, insertbackground=self.text_color, font=("Outfit", 11)
            )
            # Add subtle padding/border simulation
            entry.pack(fill="x", ipady=8, pady=(0, 5))
            self.fields[key] = entry

        # Action Buttons
        btn_frame = tk.Frame(self.right_panel, bg=self.card_bg, pady=20)
        btn_frame.pack(fill="x", side="bottom")

        self.add_btn = tk.Button(
            btn_frame, text="ADD CONTACT", bg=self.accent_color, fg=self.text_color,
            font=("Outfit", 11, "bold"), borderwidth=0, cursor="hand2", pady=10,
            command=self._add_contact
        )
        self.add_btn.pack(fill="x", pady=5)

        self.update_btn = tk.Button(
            btn_frame, text="UPDATE CHANGES", bg=self.secondary_accent, fg=self.text_color,
            font=("Outfit", 11, "bold"), borderwidth=0, cursor="hand2", pady=10,
            command=self._update_contact
        )
        self.update_btn.pack(fill="x", pady=5)

        self.delete_btn = tk.Button(
            btn_frame, text="DELETE CONTACT", bg=self.error_color, fg=self.text_color,
            font=("Outfit", 11, "bold"), borderwidth=0, cursor="hand2", pady=10,
            command=self._delete_contact
        )
        self.delete_btn.pack(fill="x", pady=5)

    def _refresh_list(self):
        query = self.search_var.get().lower()
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for idx, contact in enumerate(self.contacts):
            if query in contact['name'].lower() or query in contact['phone']:
                self.tree.insert("", "end", iid=idx, values=(contact['name'], contact['phone']))

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        self.selected_contact_index = int(selected[0])
        contact = self.contacts[self.selected_contact_index]
        
        for key, entry in self.fields.items():
            entry.delete(0, tk.END)
            entry.insert(0, contact[key])

    def _get_form_data(self):
        return {key: entry.get().strip() for key, entry in self.fields.items()}

    def _clear_form(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.selected_contact_index = None
        self.tree.selection_remove(self.tree.selection())

    def _add_contact(self):
        data = self._get_form_data()
        if not data['name'] or not data['phone']:
            messagebox.showerror("Error", "Name and Phone are required!")
            return
            
        self.contacts.append(data)
        self._save_contacts()
        self._refresh_list()
        self._clear_form()
        messagebox.showinfo("Success", "Contact added successfully!")

    def _update_contact(self):
        if self.selected_contact_index is None:
            messagebox.showwarning("Warning", "Select a contact from the list first!")
            return
            
        data = self._get_form_data()
        if not data['name'] or not data['phone']:
            messagebox.showerror("Error", "Name and Phone cannot be empty!")
            return
            
        self.contacts[self.selected_contact_index] = data
        self._save_contacts()
        self._refresh_list()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def _delete_contact(self):
        if self.selected_contact_index is None:
            messagebox.showwarning("Warning", "Select a contact to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            self.contacts.pop(self.selected_contact_index)
            self._save_contacts()
            self._refresh_list()
            self._clear_form()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
