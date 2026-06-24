import tkinter as tk
from tkinter import messagebox
import json
import os

class Node:
    def __init__(self, patient_id, details):
        self.patient_id = patient_id
        self.details = details
        self.next = None
        self.prev = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, patient_id, details):
        new_node = Node(patient_id, details)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def find(self, patient_id):
        if not self.head:
            return None
        current = self.head
        while True:
            if current.patient_id == patient_id:
                return current
            current = current.next
            if current == self.head:
                break
        return None

class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The ZEM Hospital")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.patients = CircularLinkedList()
        self.current_patient = None
        self.token_queue = []  # Queue for emergency tokens
        self.opd_token_queue = []  # Queue for OPD tokens

        self.visitors = []  # List to store visitor information
        self.feedbacks = []  # List to store feedback information

        self.navigation_stack = []  # Stack for navigation history

        self.load_data()
        self.main_menu()

    def save_data(self):
        data = {
            "patients": [],
            "token_queue": self.token_queue,
            "opd_token_queue": self.opd_token_queue,
            "visitors": self.visitors,
            "feedbacks": self.feedbacks
        }

        current = self.patients.head
        if current:
            while True:
                data["patients"].append({"patient_id": current.patient_id, "details": current.details})
                current = current.next
                if current == self.patients.head:
                    break

        with open("hospital_data.json", "w") as file:
            json.dump(data, file)

    def load_data(self):
        if os.path.exists("hospital_data.json"):
            with open("hospital_data.json", "r") as file:
                data = json.load(file)
                for patient in data["patients"]:
                    self.patients.append(patient["patient_id"], patient["details"])
                self.token_queue = data["token_queue"]
                self.opd_token_queue = data["opd_token_queue"]
                self.visitors = data["visitors"]
                self.feedbacks = data["feedbacks"]

    def main_menu(self):
        self.save_current_section(self.main_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="The ZEM Hospital", font=("Arial", 20), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text="Welcome to 318-LC Hospital Management System", font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=10)

        tk.Button(self.root, text="Patient", command=self.patient_menu, width=20, font=("Arial", 12), bg="#4CAF50", activebackground="#3e8e41", fg="black").pack(pady=10)
        tk.Button(self.root, text="Visitor", command=self.visitor_menu, width=20, font=("Arial", 12), bg="#4CAF50", activebackground="#3e8e41", fg="black").pack(pady=10)
        tk.Button(self.root, text="Feedback", command=self.feedback_menu, width=20, font=("Arial", 12), bg="#4CAF50", activebackground="#3e8e41", fg="black").pack(pady=10)

    def save_current_section(self, section_function):
        if not self.navigation_stack or self.navigation_stack[-1] != section_function:
            self.navigation_stack.append(section_function)

    def go_previous_section(self):
        if len(self.navigation_stack) > 1:
            self.navigation_stack.pop()
            previous_section = self.navigation_stack[-1]
            previous_section()

    def visitor_menu(self):
        self.save_current_section(self.visitor_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="The ZEM Hospital", font=("Arial", 20), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text="Visitor Log", font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="Name:", bg="#f0f0f0", fg="black").grid(row=0, column=0, padx=5, pady=5)
        self.visitor_name_entry = tk.Entry(frame, width=30)
        self.visitor_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Purpose:", bg="#f0f0f0", fg="black").grid(row=1, column=0, padx=5, pady=5)
        self.visitor_purpose_entry = tk.Entry(frame, width=30)
        self.visitor_purpose_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text="Log Visitor", command=self.log_visitor, width=20, font=("Arial", 12), bg="#0000FF", activebackground="#3333FF", fg="black").grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)
        tk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)

    def log_visitor(self):
        name = self.visitor_name_entry.get()
        purpose = self.visitor_purpose_entry.get()

        if not name or not purpose:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.visitors.append({"name": name, "purpose": purpose})
        self.save_data()
        messagebox.showinfo("Visitor Log", f"Visitor {name} logged successfully.")
        self.main_menu()

    def feedback_menu(self):
        self.save_current_section(self.feedback_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="The ZEM Hospital", font=("Arial", 20), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text="Feedback", font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="Feedback:", bg="#f0f0f0", fg="black").grid(row=0, column=0, padx=5, pady=5)
        self.feedback_entry = tk.Entry(frame, width=50)
        self.feedback_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="Submit Feedback", command=self.submit_feedback, width=20, font=("Arial", 12), bg="#0000FF", activebackground="#3333FF", fg="black").grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)
        tk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)

    def submit_feedback(self):
        feedback = self.feedback_entry.get()

        if not feedback:
            messagebox.showerror("Error", "Feedback cannot be empty!")
            return

        self.feedbacks.append(feedback)
        self.save_data()
        messagebox.showinfo("Feedback", "Thank you for your feedback!")
        self.main_menu()

    def patient_menu(self):
        self.save_current_section(self.patient_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="The ZEM Hospital", font=("Arial", 20), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text="Patient Details", font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="Patient ID:", bg="#f0f0f0", fg="black").grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry = tk.Entry(frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Name:", bg="#f0f0f0", fg="black").grid(row=1, column=0, padx=5, pady=5)
        self.patient_name_entry = tk.Entry(frame, width=30)
        self.patient_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Age:", bg="#f0f0f0", fg="black").grid(row=2, column=0, padx=5, pady=5)
        self.patient_age_entry = tk.Entry(frame, width=30)
        self.patient_age_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Next", command=self.patient_next_options, width=20, font=("Arial", 12), bg="#0000FF", activebackground="#3333FF", fg="black").grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)
        tk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)

    def patient_next_options(self):
        patient_id = self.patient_id_entry.get()
        name = self.patient_name_entry.get()
        age = self.patient_age_entry.get()

        if not patient_id or not name or not age:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number!")
            return

        self.patients.append(patient_id, {"name": name, "age": age})
        self.current_patient = self.patients.find(patient_id)
        self.save_data()
        self.ask_emergency_or_opd(patient_id, name)

    def ask_emergency_or_opd(self, patient_id, name):
        self.save_current_section(lambda: self.ask_emergency_or_opd(patient_id, name))

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="The ZEM Hospital", font=("Arial", 20), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text=f"Patient: {name}", font=("Arial", 16), bg="#f0f0f0", fg="black").pack(pady=20)
        tk.Label(self.root, text="Choose Service Type:", font=("Arial", 14), bg="#f0f0f0", fg="black").pack(pady=10)

        tk.Button(self.root, text="Emergency", command=lambda: self.register_emergency(patient_id, name), width=20, font=("Arial", 12), bg="#4CAF50", activebackground="#3e8e41", fg="black").pack(pady=5)
        tk.Button(self.root, text="OPD", command=lambda: self.show_opd_services(patient_id, name), width=20, font=("Arial", 12), bg="#4CAF50", activebackground="#3e8e41", fg="black").pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=10)
        tk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, font=("Arial", 12), bg="#FF0000", activebackground="#CC0000", fg="black").pack(pady=5)

    def register_emergency(self, patient_id, name):
        self.token_queue.append(patient_id)
        self.save_data()
        messagebox.showinfo("Emergency", f"Emergency token issued for {name}.")
        self.main_menu()

    def show_opd_services(self, patient_id, name):
        self.opd_token_queue.append(patient_id)
        self.save_data()
        messagebox.showinfo("OPD", f"OPD token issued for {name}.")
        self.main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementGUI(root)
    root.mainloop()
