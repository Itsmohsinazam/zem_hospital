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


def patient():
    root.destroy()
    import patient_screen

def visitor():
    messagebox.showinfo("Success", 'Login is successful')
    root.destroy()

def suggestion():
    messagebox.showinfo("Success", 'Login is successful')
    root.destroy()

def doctor():
    root.destroy()
    import admin_hms


# Initialize the main application window
root = CTk()
root.geometry("950x450")  
root.resizable(False, False)  
root.title("Login Page")

# Load and configure the background image
image = CTkImage(Image.open('zem.png'), size=(950, 450))
imageLabel = CTkLabel(root, image=image, text="")  # Use text="" to avoid overlap
imageLabel.place(x=0, y=0)


# Heading label with a specific background color
headinglabel = CTkLabel(root, text="Welcome to ZEM Hospital", 
                        fg_color="#097999",  # Background color
                        text_color="white",  # Text color
                        font=("Goudy Old Style", 30, "bold"))  # Custom font
headinglabel.place(x=30, y=150)


patientButton = CTkButton(root, text='Patient', cursor='hand2', command=patient)
patientButton.place(x=120, y=200)

visitorButton = CTkButton(root, text='Visitor', cursor='hand2', command=visitor)
visitorButton.place(x=120, y=240)

SuggestionButton = CTkButton(root, text='Add Suggestion', cursor='hand2', command=suggestion)
SuggestionButton.place(x=120, y=280)

doctorButton = CTkButton(root, text='Doctor', cursor='hand2', command=doctor)
doctorButton.place(x=120, y=320)




root.mainloop()