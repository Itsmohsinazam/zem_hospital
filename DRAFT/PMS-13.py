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
window.grid_rowconfigure(1, weight=1)

# Load and configure the background image
image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
imageLabel = CTkLabel(window, image=image, text="")
imageLabel.grid(row=0, column=0, sticky='n', pady=10)

# Left Frame
leftFrame = CTkFrame(window, fg_color="black")
leftFrame.grid(row=1, column=0, padx=20, pady=20, sticky='n')

# Configure the grid for the leftFrame
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_columnconfigure(1, weight=1)

# CNIC
cnicLabel = CTkLabel(leftFrame, text='Enter your Cnic:', font=('ariel', 18, 'bold'), text_color="white")
cnicLabel.grid(row=0, column=0, padx=10, pady=10, sticky='e')

cnicEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
cnicEntry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Patient Name
nameLabel = CTkLabel(leftFrame, text='Patient name:', font=('ariel', 18, 'bold'), text_color="white")
nameLabel.grid(row=1, column=0, padx=10, pady=10, sticky='e')

nameEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
nameEntry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# Phone Number
phoneLabel = CTkLabel(leftFrame, text='Phone Number:', font=('ariel', 18, 'bold'), text_color="white")
phoneLabel.grid(row=2, column=0, padx=10, pady=10, sticky='e')

phoneEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
phoneEntry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Age
ageLabel = CTkLabel(leftFrame, text='Age:', font=('ariel', 18, 'bold'), text_color="white")
ageLabel.grid(row=0, column=2, padx=10, pady=10, sticky='e')

ageEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
ageEntry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# Gender
genderLabel = CTkLabel(leftFrame, text='Gender:', font=('ariel', 18, 'bold'), text_color="white")
genderLabel.grid(row=1, column=2, padx=10, pady=10, sticky='e')

genders = ['Male', 'Female', 'Others']
gender_Box = CTkComboBox(leftFrame, values=genders)
gender_Box.grid(row=1, column=3, padx=10, pady=10, sticky='w')
gender_Box.set('Please Select')

# City
cityLabel = CTkLabel(leftFrame, text='City:', font=('ariel', 18, 'bold'), text_color="white")
cityLabel.grid(row=2, column=2, padx=10, pady=10, sticky='e')

cityEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
cityEntry.grid(row=2, column=3, padx=10, pady=10, sticky='w')

# Define button functions
def emergency():
    patient_data = {
        "CNIC": cnicEntry.get(),
        "Name": nameEntry.get(),
        "Phone": phoneEntry.get(),
        "Age": ageEntry.get(),
        "Gender": gender_Box.get(),
        "City": cityEntry.get()
    }
    emergency_queue.enqueue(patient_data)
    messagebox.showinfo("Emergency", 'Emergency data saved successfully!')
    window.destroy()

def opd():
    messagebox.showinfo("OPD", 'OPD button clicked')
    window.destroy()

def previous():
    previous_screen = navigation_list.go_previous()
    messagebox.showinfo("Navigation", f"Going to previous screen: {previous_screen}")

def forward():
    next_screen = navigation_list.go_forward()
    messagebox.showinfo("Navigation", f"Going to next screen: {next_screen}")

def patient():
    messagebox.showinfo("Patient", "Navigating to Patient screen")

def visitor():
    messagebox.showinfo("Visitor", 'Login is successful')

def suggestion():
    messagebox.showinfo("Suggestion", 'Login is successful')

def doctor():
    messagebox.showinfo("Doctor", "Navigating to Doctor screen")

# Buttons
buttonFrame = CTkFrame(window, fg_color="black")
buttonFrame.grid(row=2, column=0, pady=20, sticky='n')

emergencyButton = CTkButton(buttonFrame, text='Save and generate token for Emergency', cursor='hand2', command=emergency)
emergencyButton.grid(row=0, column=0, padx=10, pady=10)

opdButton = CTkButton(buttonFrame, text='Save and continue to OPD', cursor='hand2', command=opd)
opdButton.grid(row=1, column=0, padx=10, pady=10)

previousButton = CTkButton(buttonFrame, text='Previous', cursor='hand2', command=previous)
previousButton.grid(row=2, column=0, padx=10, pady=10)

forwardButton = CTkButton(buttonFrame, text='Forward', cursor='hand2', command=forward)
forwardButton.grid(row=3, column=0, padx=10, pady=10)

# Additional Buttons for Login Page
loginButtonFrame = CTkFrame(window, fg_color="black")
loginButtonFrame.grid(row=3, column=0, pady=10, sticky='n')

patientButton = CTkButton(loginButtonFrame, text='Patient', cursor='hand2', command=patient)
patientButton.grid(row=0, column=0, padx=10, pady=10)

visitorButton = CTkButton(loginButtonFrame, text='Visitor', cursor='hand2', command=visitor)
visitorButton.grid(row=0, column=1, padx=10, pady=10)

SuggestionButton = CTkButton(loginButtonFrame, text='Add Suggestion', cursor='hand2', command=suggestion)
SuggestionButton.grid(row=0, column=2, padx=10, pady=10)

doctorButton = CTkButton(loginButtonFrame, text='Doctor', cursor='hand2', command=doctor)
doctorButton.grid(row=0, column=3, padx=10, pady=10)

# Run the application
window.mainloop()
