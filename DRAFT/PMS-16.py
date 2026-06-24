from customtkinter import *
from PIL import Image
from tkinter import messagebox


# Define a Stack class for navigation history
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []


# Define a Queue class for screen transitions
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0


# Navigation data structures
navigation_stack = Stack()
screen_queue = Queue()


# Function to render a screen
def render_screen(screen_function):
    global current_screen
    if current_screen is not None:
        current_screen.destroy()

    navigation_stack.push(screen_function)
    screen_function()


# Function to go back to the previous screen
def go_back():
    if not navigation_stack.is_empty():
        navigation_stack.pop()  # Remove the current screen
        previous_screen = navigation_stack.pop()  # Get the previous screen
        if previous_screen:
            render_screen(previous_screen)


# User Screen
def user_screen():
    global current_screen
    current_screen = CTk()
    current_screen.geometry("950x450")
    current_screen.resizable(False, False)
    current_screen.title("Login Page")

    # Background image
    image = CTkImage(Image.open('zem.png'), size=(950, 450))
    imageLabel = CTkLabel(current_screen, image=image, text="")
    imageLabel.place(x=0, y=0)

    # Heading label
    headinglabel = CTkLabel(current_screen, text="Welcome to ZEM Hospital",
                            fg_color="#097999",
                            text_color="white",
                            font=("Goudy Old Style", 30, "bold"))
    headinglabel.place(x=30, y=150)

    # Buttons
    CTkButton(current_screen, text='Patient', cursor='hand2', 
              command=lambda: render_screen(patient_screen)).place(x=120, y=200)
    CTkButton(current_screen, text='Visitor', cursor='hand2',
              command=lambda: messagebox.showinfo("Sabar", 'Under construction')).place(x=120, y=240)
    CTkButton(current_screen, text='Add Suggestion', cursor='hand2',
              command=lambda: messagebox.showinfo("Sabar", 'Under construction')).place(x=120, y=280)
    CTkButton(current_screen, text='Doctor', cursor='hand2',
              command=lambda: messagebox.showinfo("Sabar", 'Under construction')).place(x=120, y=320)

    current_screen.mainloop()


# Patient Screen
def patient_screen():
    global current_screen
    current_screen = CTk()
    current_screen.geometry("930x580")
    current_screen.resizable(False, False)
    current_screen.title("Hospital Management System")
    current_screen.configure(fg_color='black')

    # Background image
    image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
    imageLabel = CTkLabel(current_screen, image=image, text="")
    imageLabel.grid(row=0, column=0, sticky='n', pady=10)

    # Left Frame
    leftFrame = CTkFrame(current_screen, fg_color="black")
    leftFrame.grid(row=1, column=0, padx=20, pady=20, sticky='n')
    leftFrame.grid_columnconfigure((0, 1), weight=1)

    # Entry Fields
    CTkLabel(leftFrame, text='Enter your Cnic:', font=('ariel', 18, 'bold'), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=0, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Patient name:', font=('ariel', 18, 'bold'), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=1, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Phone Number:', font=('ariel', 18, 'bold'), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Buttons
    buttonFrame = CTkFrame(current_screen, fg_color="black")
    buttonFrame.grid(row=2, column=0, pady=20, sticky='n')

    CTkButton(buttonFrame, text='Generate token for Emergency', 
              command=lambda: messagebox.showinfo("Emergency", 'Emergency button clicked')).grid(row=0, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Continue to OPD', 
              command=lambda: messagebox.showinfo("OPD", 'OPD button clicked')).grid(row=1, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Go to Main Menu', command=go_back).grid(row=2, column=0, padx=10, pady=10)

    current_screen.mainloop()


# Initialize the application
current_screen = None
render_screen(user_screen)
