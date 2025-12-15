import tkinter as tk
import sqlite3
from tkinter import messagebox

class CRUDApp:
    def __init__(self, root=None):
        if root:
            self.root = root
            self.root.title("Student CRUD Application")
            self.root.geometry("700x400")
            self.instantiate_ui()

    def instantiate_ui(self):
        # ===== DATABASE =====
        self.conn = sqlite3.connect("school.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                stclass TEXT,
                marks REAL
            )
        """)
        self.conn.commit()

        # ===== HEADER =====
        header = tk.Label(self.root, text="Student Management System",
                          font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # ===== MAIN FRAME =====
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10)

        # ===== FORM FRAME (LEFT) =====
        self.form_frame = tk.LabelFrame(main_frame, text="Student Form", padx=10, pady=10)
        self.form_frame.grid(row=0, column=0, sticky="n")

        tk.Label(self.form_frame, text="Name").grid(row=0, column=0, sticky="w")
        tk.Label(self.form_frame, text="Class").grid(row=1, column=0, sticky="w")
        tk.Label(self.form_frame, text="Marks").grid(row=2, column=0, sticky="w")

        self.name_entry = tk.Entry(self.form_frame, width=25)
        self.stclass_entry = tk.Entry(self.form_frame, width=25)
        self.marks_entry = tk.Entry(self.form_frame, width=25)

        self.name_entry.grid(row=0, column=1, pady=5)
        self.stclass_entry.grid(row=1, column=1, pady=5)
        self.marks_entry.grid(row=2, column=1, pady=5)

        # ===== FORM BUTTONS =====
        self.add_btn = tk.Button(self.form_frame, text="Create",
                                 bg="#4CAF50", fg="white",
                                 width=12, command=self.add_student)
        self.update_btn = tk.Button(self.form_frame, text="Update",
                                    bg="#2196F3", fg="white",
                                    width=12, command=self.update_student)

        self.add_btn.grid(row=3, column=0, pady=10)
        self.update_btn.grid(row=3, column=1, pady=10)

        # ===== LIST FRAME (RIGHT) =====
        list_frame = tk.LabelFrame(main_frame, text="Students List", padx=10, pady=10)
        list_frame.grid(row=0, column=1, padx=20, sticky="n")

        self.student_listbox = tk.Listbox(list_frame, width=40, height=12)
        self.student_listbox.pack()

        # ===== ACTION BUTTONS =====
        action_frame = tk.Frame(list_frame)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Load",
                  width=10, command=self.load_students).grid(row=0, column=0, padx=5)

        tk.Button(action_frame, text="Delete",
                  bg="#F44336", fg="white",
                  width=10, command=self.delete_student).grid(row=0, column=1, padx=5)

        self.load_students()

    # ===== CRUD FUNCTIONS (UNCHANGED LOGIC) =====
    def add_student(self, student_name=None, student_class = None, student_marks= None):
        
        if not (student_name and student_class and student_marks):
            name = self.name_entry.get()
            stclass = self.stclass_entry.get()
            marks = self.marks_entry.get()
        else:
            name = student_name
            stclass = student_class
            marks = student_marks

        if not hasattr(self, "cursor"):
            self.conn = sqlite3.connect("school.db")
            self.cursor = self.conn.cursor()
            
        if name and stclass and marks:
            self.cursor.execute(
                "INSERT INTO students (name, stclass, marks) VALUES (?, ?, ?)",
                (name, stclass, marks)
            )
            self.conn.commit()
            if not (student_name and student_class and student_marks):
                self.load_students()
                self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please fill all fields")

    def load_students(self):
        self.student_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM students")
        for row in self.cursor.fetchall():
            self.student_listbox.insert(
                tk.END, f"{row[0]:<3}  {row[1]:<15}  {row[2]:<10}  {row[3]}"
            )

    def update_student(self):
        selected = self.student_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return

        student_id = int(selected.split()[0])
        self.cursor.execute(
            "UPDATE students SET name=?, stclass=?, marks=? WHERE id=?",
            (self.name_entry.get(),
             self.stclass_entry.get(),
             self.marks_entry.get(),
             student_id)
        )
        self.conn.commit()
        self.load_students()
        self.clear_entries()

    def delete_student(self):
        selected = self.student_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return

        student_id = int(selected.split()[0])
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()
        self.load_students()
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.stclass_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    def show_ui(self):
        root = tk.Tk()
        CRUDApp(root)
        root.mainloop()
