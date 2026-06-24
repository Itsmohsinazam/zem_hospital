# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:33:59 2024

@author: Administrator
"""

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
        self.token_queue = []  # Queue for emergency tokens
        self.opd_token_queue = []  # Queue for OPD tokens

        self.navigation_stack = []  # Stack for navigation history

        self.main_menu()

    def main_menu(self):
        self.save_current_section(self.main_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Welcome to 318-LC Hospital Management System",
                  font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        ttk.Button(self.root, text="Patient", command=self.patient_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Visitor", command=self.visitor_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Feedback", command=self.feedback_menu, width=20, style="TButton").pack(pady=10)

    def save_current_section(self, section_function):
        """Save the current section to the navigation stack."""
        if not self.navigation_stack or self.navigation_stack[-1] != section_function:
            self.navigation_stack.append(section_function)

    def go_previous_section(self):
        """Go to the previous section by popping from the navigation stack."""
        if len(self.navigation_stack) > 1:
            self.navigation_stack.pop()  # Remove the current section
            previous_section = self.navigation_stack[-1]
            previous_section()

    def patient_menu(self):
        self.save_current_section(self.patient_menu)

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
        ttk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, style="TButton").pack(pady=5)

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
        self.ask_emergency_or_opd(patient_id, name)

    def ask_emergency_or_opd(self, patient_id, name):
        self.save_current_section(lambda: self.ask_emergency_or_opd(patient_id, name))

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text=f"Patient: {name}", font=("Arial", 16), background="#f0f0f0").pack(pady=20)
        ttk.Label(self.root, text="Choose Service Type:", font=("Arial", 14), background="#f0f0f0").pack(pady=10)

        ttk.Button(self.root, text="Emergency", command=lambda: self.register_emergency(patient_id, name), width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="OPD", command=lambda: self.show_opd_services(patient_id, name), width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, style="TButton").pack(pady=5)

    def register_emergency(self, patient_id, name):
        waiting_number = len(self.token_queue) + 1
        token = f"Token: {waiting_number}\nPatient ID: {patient_id}\nName: {name}"
        self.token_queue.append(token)

        messagebox.showinfo("Emergency Token", token)
        self.main_menu()

    def show_opd_services(self, patient_id, name):
        self.save_current_section(lambda: self.show_opd_services(patient_id, name))

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="OPD Services", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        opd_services = [
            "Consultation", "Day Care Treatment", "Investigations", "Referrals", "Admissions",
            "Post Discharge Follow Up", "Health Check Ups", "Immunizations", "Physio-Therapy"
        ]

        frame = ttk.Frame(self.root, style="TFrame")
        frame.pack(pady=10)

        for i, service in enumerate(opd_services):
            button = ttk.Button(frame, text=service, command=lambda s=service: self.schedule_opd(patient_id, name, s), width=30, style="TButton")
            button.grid(row=i//2, column=i%2, padx=10, pady=5)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, style="TButton").pack(pady=5)

    def schedule_opd(self, patient_id, name, service):
        doctor_name = "Dr. Smith"  # Example doctor
        room_number = "101"  # Example room
        token_number = len(self.opd_token_queue) + 1

        token_details = {
            "Patient ID": patient_id,
            "Name": name,
            "Service": service,
            "Doctor": doctor_name,
            "Room": room_number,
            "Token": token_number
        }

        self.opd_token_queue.append(token_details)

        token_message = (f"Token Number: {token_number}\n"
                         f"Patient ID: {patient_id}\n"
                         f"Name: {name}\n"
                         f"Service: {service}\n"
                         f"Doctor: {doctor_name}\n"
                         f"Room: {room_number}")

        messagebox.showinfo("OPD Token", token_message)
        self.main_menu()

    def visitor_menu(self):
        self.save_current_section(self.visitor_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Visitor Management", font=("Arial", 16), background="#f0f0f0").pack(pady=20)
        ttk.Label(self.root, text="Visitor feature is under construction.", font=("Arial", 14), background="#f0f0f0").pack(pady=20)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, style="TButton").pack(pady=5)

    def feedback_menu(self):
        self.save_current_section(self.feedback_menu)

        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Feedback", font=("Arial", 16), background="#f0f0f0").pack(pady=20)

        frame = ttk.Frame(self.root, padding="10", style="TFrame")
        frame.pack(pady=10)

        ttk.Label(frame, text="Enter your feedback:", background="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.feedback_entry = ttk.Entry(frame, width=50)
        self.feedback_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Submit", command=self.submit_feedback, width=20, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20, style="TButton").pack(pady=5)
        ttk.Button(self.root, text="Previous", command=self.go_previous_section, width=20, style="TButton").pack(pady=5)

    def submit_feedback(self):
        feedback = self.feedback_entry.get()
        if feedback.strip():
            messagebox.showinfo("Feedback", "Thank you for your feedback!")
            self.main_menu()
        else:
            messagebox.showerror("Error", "Feedback cannot be empty!")

# Create the main window
root = tk.Tk()

# Create and run the Hospital Management System GUI
app = HospitalManagementGUI(root)
root.mainloop()
