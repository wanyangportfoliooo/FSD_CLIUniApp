import tkinter as tk
from tkinter import messagebox

import authenticator
from controllers.database_controller import DatabaseController
from classes.subject import Subject


class ExceptionWindow(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.title("Exception Window")
        self.geometry("350x150")
        self.configure(bg="#607b8d")

        tk.Label(
            self,
            text=message,
            bg="#607b8d",
            fg="#ffc107",
            font=("Arial", 11, "bold"),
            wraplength=300
        ).pack(expand=True, padx=20, pady=20)

        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)


class SubjectWindow(tk.Toplevel):
    def __init__(self, master, student):
        super().__init__(master)
        self.title("Subject Window")
        self.geometry("430x300")
        self.configure(bg="#607b8d")

        tk.Label(
            self,
            text="Enrolled Subjects",
            bg="#607b8d",
            fg="#ffc107",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.subject_list = tk.Listbox(self, width=60, height=10)
        self.subject_list.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        if len(student.subjects) == 0:
            self.subject_list.insert(tk.END, "< Nothing to Display >")
        else:
            for subject in student.subjects:
                self.subject_list.insert(
                    tk.END,
                    f"Subject::{subject.id:03d} -- mark = {subject.mark} -- grade = {subject.grade}"
                )

        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, master, student, database):
        super().__init__(master)

        self.student = student
        self.database = database

        self.title("Enrolment Window")
        self.geometry("420x300")
        self.configure(bg="#607b8d")

        tk.Label(
            self,
            text=f"Welcome {student.name}",
            bg="#607b8d",
            fg="#ffc107",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Button(
            self,
            text="Enrol Subject",
            width=20,
            command=self.enrol_subject
        ).pack(pady=8)

        tk.Button(
            self,
            text="Show Subjects",
            width=20,
            command=self.show_subjects
        ).pack(pady=8)

        tk.Button(
            self,
            text="Exit",
            width=20,
            command=self.destroy
        ).pack(pady=8)

    def enrol_subject(self):
        if len(self.student.subjects) >= 4:
            ExceptionWindow(self, "Students are allowed to enrol in 4 subjects only.")
            return

        subject = Subject()
        self.student.subjects.append(subject)
        self.student.calculate_average()

        self.database.update_subjects(self.student)

        messagebox.showinfo(
            "Enrolment",
            f"Enrolled in Subject-{subject.id:03d}\n"
            f"You are now enrolled in {len(self.student.subjects)} out of 4 subjects"
        )

    def show_subjects(self):
        SubjectWindow(self, self.student)


class LoginFrame(tk.LabelFrame):
    def __init__(self, master, database):
        super().__init__(
            master,
            text="Student Login",
            bg="#607b8d",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=20
        )

        self.master = master
        self.database = database

        self.email_text = tk.StringVar()
        self.password_text = tk.StringVar()

        tk.Label(
            self,
            text="Email:",
            bg="#607b8d",
            fg="#ffc107"
        ).grid(row=0, column=0, sticky="e", pady=5)

        tk.Entry(
            self,
            textvariable=self.email_text,
            width=28
        ).grid(row=0, column=1, pady=5)

        tk.Label(
            self,
            text="Password:",
            bg="#607b8d",
            fg="#ffc107"
        ).grid(row=1, column=0, sticky="e", pady=5)

        tk.Entry(
            self,
            textvariable=self.password_text,
            show="*",
            width=28
        ).grid(row=1, column=1, pady=5)

        tk.Button(
            self,
            text="Cancel",
            command=self.master.destroy
        ).grid(row=2, column=0, pady=15)

        tk.Button(
            self,
            text="Login",
            command=self.login
        ).grid(row=2, column=1, pady=15, sticky="e")

    def login(self):
        email = self.email_text.get().strip()
        password = self.password_text.get().strip()

        if email == "" or password == "":
            ExceptionWindow(self.master, "Email and password cannot be empty.")
            return

        if not authenticator.validate_email(email):
            ExceptionWindow(self.master, "Incorrect email format.")
            return

        if not authenticator.authenticate(email, password):
            ExceptionWindow(self.master, "Incorrect student credentials.")
            return

        student = self.database.get_student(email)

        if student is None:
            ExceptionWindow(self.master, "Student does not exist.")
            return

        self.clear()
        EnrolmentWindow(self.master, student, self.database)

    def clear(self):
        self.email_text.set("")
        self.password_text.set("")


class GUIUniApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUIUniApp")
        self.root.geometry("380x260")
        self.root.configure(bg="#607b8d")
        self.root.resizable(False, False)

        self.database = DatabaseController()

        frame = LoginFrame(self.root, self.database)
        frame.place(relx=0.5, rely=0.5, anchor="center")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUIUniApp()
    app.run()