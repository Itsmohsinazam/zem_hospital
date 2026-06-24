import tkinter as tk
from tkinter import ttk, messagebox


class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("318-LC Hospital Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")  # Background color of the window

        # Define styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TFrame", background="#f0f0f0")

        # Initialize management systems
        self.patients = PatientManagement()
        self.visitors = VisitorManagement()
        self.feedback_records = []

        self.token_counter = 1  # Token counter for appointments

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

        self.patients.register_patient(patient_id, {"name": name, "age": int(age), "appointments": [], "history": {}})
        messagebox.showinfo("Success", f"Patient {name} registered successfully!")
        self.main_menu()

    def visitor_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Visitor Details", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        frame = ttk.Frame(self.root, padding="10", style="TFrame")
        frame.pack(pady=10)

        ttk.Label(frame, text="Visitor Name:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.visitor_name_entry = ttk.Entry(frame, width=30)
        self.visitor_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Purpose of Visit:", background="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.visitor_purpose_entry = ttk.Entry(frame, width=30)
        self.visitor_purpose_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Submit", command=self.save_visitor_details, width=20, style="TButton").grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)

    def save_visitor_details(self):
        name = self.visitor_name_entry.get()
        purpose = self.visitor_purpose_entry.get()

        if not name or not purpose:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.visitors.add_visitor({"name": name, "purpose": purpose})
        messagebox.showinfo("Success", "Visitor details saved!")
        self.main_menu()

    def feedback_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Submit Feedback", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        feedback_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        feedback_frame.pack(pady=10)

        ttk.Label(feedback_frame, text="Your Feedback:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.feedback_entry = tk.Text(feedback_frame, width=40, height=5)
        self.feedback_entry.grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(feedback_frame, text="Submit", command=self.save_feedback, width=20, style="TButton").grid(row=2, column=0, pady=10)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)

    def save_feedback(self):
        feedback = self.feedback_entry.get("1.0", tk.END).strip()
        if not feedback:
            messagebox.showerror("Error", "Feedback cannot be empty!")
            return

        self.feedback_records.append({"feedback": feedback})
        messagebox.showinfo("Success", "Thank you for your feedback!")
        self.main_menu()


class PatientManagement:
    def __init__(self):
        self.patients = {}  # Nested dictionary: patient_id -> {details}

    def register_patient(self, patient_id, details):
        self.patients[patient_id] = details

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, "Patient not found.")


class VisitorManagement:
    def __init__(self):
        self.visitors = []  # List of visitor records

    def add_visitor(self, visitor_details):
        self.visitors.append(visitor_details)


# Create the main window
root = tk.Tk()

# Create and run the Hospital Management System GUI
app = HospitalManagementGUI(root)
root.mainloop()

