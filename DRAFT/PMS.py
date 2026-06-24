import tkinter as tk
from tkinter import ttk, messagebox

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
        self.root.title("318-LC Hospital Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TFrame", background="#f0f0f0")

        self.patients = CircularLinkedList()
        self.current_patient = None

        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Welcome to 318-LC Hospital Management System",
                  font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        ttk.Button(self.root, text="Patient", command=self.patient_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Visitor", command=self.visitor_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Feedback", command=self.feedback_menu, width=20, style="TButton").pack(pady=10)

    def patient_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Patient Details", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        frame = ttk.Frame(self.root, padding="10", style="TFrame")
        frame.pack(pady=10)

        ttk.Label(frame, text="Patient ID:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry = ttk.Entry(frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name:", background="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.patient_name_entry = ttk.Entry(frame, width=30)
        self.patient_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Age:", background="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.patient_age_entry = ttk.Entry(frame, width=30)
        self.patient_age_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Next", command=self.patient_next_options, width=20, style="TButton").grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)

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
        self.show_patient_options()

    def show_patient_options(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text=f"Current Patient: {self.current_patient.details['name']}",
                  font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        ttk.Label(self.root, text=f"Age: {self.current_patient.details['age']}",
                  font=("Arial", 14), background="#f0f0f0").pack(pady=10)

        ttk.Button(self.root, text="Next Patient", command=self.next_patient, width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="Previous Patient", command=self.previous_patient, width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)

    def next_patient(self):
        if self.current_patient:
            self.current_patient = self.current_patient.next
            self.show_patient_options()

    def previous_patient(self):
        if self.current_patient:
            self.current_patient = self.current_patient.prev
            self.show_patient_options()

    def visitor_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Visitor Management", font=("Arial", 16), background="#f0f0f0").pack(pady=20)
        ttk.Label(self.root, text="Visitor feature is under construction.", font=("Arial", 14), background="#f0f0f0").pack(pady=20)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=10)

    def feedback_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Feedback", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        ttk.Label(self.root, text="Please provide your feedback below:", font=("Arial", 14), background="#f0f0f0").pack(pady=10)
        self.feedback_entry = ttk.Entry(self.root, width=50)
        self.feedback_entry.pack(pady=10)

        ttk.Button(self.root, text="Submit Feedback", command=self.submit_feedback, width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)

    def submit_feedback(self):
        feedback = self.feedback_entry.get()
        if not feedback:
            messagebox.showerror("Error", "Feedback cannot be empty!")
        else:
            messagebox.showinfo("Thank You", "Your feedback has been submitted.")
            self.feedback_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()

# Create and run the Hospital Management System GUI
app = HospitalManagementGUI(root)
root.mainloop()
