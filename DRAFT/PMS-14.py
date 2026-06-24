from customtkinter import *
from PIL import Image
from tkinter import messagebox

# Define a Node for the double circular linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Define the double circular linked list
class DoubleCircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
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

    def go_forward(self):
        if self.head:
            self.head = self.head.next
        return self.head.data if self.head else None

    def go_previous(self):
        if self.head:
            self.head = self.head.prev
        return self.head.data if self.head else None

# Queue to store emergency data
class EmergencyQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

# Initialize navigation list and emergency queue
navigation_list = DoubleCircularLinkedList()
navigation_list.append("Login")
navigation_list.append("Patient Details")
navigation_list.append("Emergency")
navigation_list.append("OPD")

emergency_queue = EmergencyQueue()

# Initialize the main application window
window = CTk()
window.geometry("930x580")
window.resizable(False, False)
window.title("Hospital Management System")
window.configure(fg_color='black')

# Configure the grid layout for the window
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Define screen frames
screens = {}

def show_screen(screen_name):
    for frame_name, frame in screens.items():
        if frame_name == screen_name:
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame.grid_forget()

# Create Login Screen
loginFrame = CTkFrame(window, fg_color="black")
screens["Login"] = loginFrame

loginLabel = CTkLabel(loginFrame, text="Welcome to Hospital Management System", font=("Arial", 24, "bold"), text_color="white")
loginLabel.pack(pady=20)

visitorButton = CTkButton(loginFrame, text="Visitor", command=lambda: show_screen("Patient Details"))
visitorButton.pack(pady=10)

# Create Patient Details Screen
patientDetailsFrame = CTkFrame(window, fg_color="black")
screens["Patient Details"] = patientDetailsFrame

patientLabel = CTkLabel(patientDetailsFrame, text="Patient Details", font=("Arial", 24, "bold"), text_color="white")
patientLabel.pack(pady=20)

nextButton = CTkButton(patientDetailsFrame, text="Emergency", command=lambda: show_screen("Emergency"))
nextButton.pack(pady=10)

# Create Emergency Screen
emergencyFrame = CTkFrame(window, fg_color="black")
screens["Emergency"] = emergencyFrame

emergencyLabel = CTkLabel(emergencyFrame, text="Emergency", font=("Arial", 24, "bold"), text_color="white")
emergencyLabel.pack(pady=20)

saveButton = CTkButton(emergencyFrame, text="Save and Generate Token", command=lambda: show_screen("OPD"))
saveButton.pack(pady=10)

# Create OPD Screen
opdFrame = CTkFrame(window, fg_color="black")
screens["OPD"] = opdFrame

opdLabel = CTkLabel(opdFrame, text="Outpatient Department (OPD)", font=("Arial", 24, "bold"), text_color="white")
opdLabel.pack(pady=20)

backToLoginButton = CTkButton(opdFrame, text="Back to Login", command=lambda: show_screen("Login"))
backToLoginButton.pack(pady=10)

# Show the Login screen initially
show_screen("Login")

# Run the application
window.mainloop()