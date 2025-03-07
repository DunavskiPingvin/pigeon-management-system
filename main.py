import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import plotly.express as px
import webbrowser
import os

# Database setup
DB_FILE = "pigeons.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pigeons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        breed TEXT,
                        age INTEGER,
                        weight REAL
                     )''')
    conn.commit()
    conn.close()

setup_database()

class PigeonManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Pigeon Management System")
        self.root.geometry("700x500")

        # Title
        ttk.Label(root, text="Pigeon Management System", font=("Arial", 16)).pack(pady=10)

        # Form Inputs
        form_frame = ttk.Frame(root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Breed:").grid(row=1, column=0, padx=5, pady=5)
        self.breed_entry = ttk.Entry(form_frame)
        self.breed_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5)
        self.age_entry = ttk.Entry(form_frame)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Weight (kg):").grid(row=3, column=0, padx=5, pady=5)
        self.weight_entry = ttk.Entry(form_frame)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Pigeon", command=self.add_pigeon).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_pigeon).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_pigeon).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Show Stats", command=self.show_stats).grid(row=0, column=3, padx=5)

        # Data Table
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Breed", "Age", "Weight"), show="headings")
        self.tree.pack(pady=10)

        for col in ("ID", "Name", "Breed", "Age", "Weight"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.select_pigeon)
        self.load_pigeons()

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()

    def add_pigeon(self):
        name, breed, age, weight = self.get_input_values()
        if not name or not breed or not age or not weight:
            messagebox.showerror("Error", "All fields are required!")
            return
        self.execute_db_query("INSERT INTO pigeons (name, breed, age, weight) VALUES (?, ?, ?, ?)", (name, breed, age, weight))
        self.load_pigeons()
        self.clear_inputs()

    def update_pigeon(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a pigeon to update!")
            return
        pigeon_id = self.tree.item(selected[0])["values"][0]
        name, breed, age, weight = self.get_input_values()
        self.execute_db_query("UPDATE pigeons SET name=?, breed=?, age=?, weight=? WHERE id=?", (name, breed, age, weight, pigeon_id))
        self.load_pigeons()
        self.clear_inputs()

    def delete_pigeon(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a pigeon to delete!")
            return
        pigeon_id = self.tree.item(selected[0])["values"][0]
        self.execute_db_query("DELETE FROM pigeons WHERE id=?", (pigeon_id,))
        self.load_pigeons()

    def load_pigeons(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pigeons")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

    def select_pigeon(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])["values"]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item[1])
        self.breed_entry.delete(0, tk.END)
        self.breed_entry.insert(0, item[2])
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, item[3])
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, item[4])

    def get_input_values(self):
        return self.name_entry.get(), self.breed_entry.get(), self.age_entry.get(), self.weight_entry.get()

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

    def show_stats(self):
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM pigeons", conn)
        conn.close()

        if df.empty:
            messagebox.showerror("Error", "No data available!")
            return

        fig1 = px.pie(df, names="breed", title="Pigeon Breed Distribution")
        fig2 = px.histogram(df, x="weight", title="Pigeon Weight Distribution")
        fig3 = px.bar(df, x="name", y="age", title="Pigeon Age Distribution")

        fig1.write_html("breed_distribution.html")
        fig2.write_html("weight_distribution.html")
        fig3.write_html("age_distribution.html")

        webbrowser.open("breed_distribution.html")
        webbrowser.open("weight_distribution.html")
        webbrowser.open("age_distribution.html")

if __name__ == "__main__":
    root = tk.Tk()
    app = PigeonManager(root)
    root.mainloop()