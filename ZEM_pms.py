from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk, VERTICAL 


# Define a Node for the double circular linked list
class Node:
    def __init__(self, data, screen_func):
        self.data = data
        self.screen_func = screen_func
        self.next = None
        self.prev = None

class DoubleCircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data, screen_func):
        new_node = Node(data, screen_func)
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
        return self.head

    def go_previous(self):
        if self.head and self.head.prev:
            self.head = self.head.prev
        return self.head


# Navigation list
navigation_list = DoubleCircularLinkedList()

# User screen
def user_screen():
    global root
    root = CTk()
    root.geometry("950x450")
    root.resizable(False, False)
    root.title("Login Page")

    # Background image
    image = CTkImage(Image.open('zem.png'), size=(950, 450))
    imageLabel = CTkLabel(root, image=image, text="")
    imageLabel.place(x=0, y=0)

    # Heading label
    headinglabel = CTkLabel(root, text="Welcome to ZEM Hospital",
                            fg_color="#097999",
                            text_color="white",
                            font=("Goudy Old Style", 30, "bold"))
    headinglabel.place(x=30, y=150)

    def go_to_patient_screen():
        root.destroy()
        navigation_list.head = navigation_list.go_forward()
        navigation_list.head.screen_func()

    def call_doc():
        root.destroy()
        import admin_hms

    def call_visitor():
        root.destroy()
        visitor_screen()

    def call_sug():
        root.destroy()
        suggestion_screen()

    # Buttons
    CTkButton(root, text='Patient', cursor='hand2', command=go_to_patient_screen).place(x=120, y=200)
    CTkButton(root, text='Visitor', cursor='hand2',command=call_visitor).place(x=120, y=240)
    CTkButton(root, text='Add Suggestion', cursor='hand2',command=call_sug).place(x=120, y=280)
    CTkButton(root, text='Doctor', cursor='hand2',command=call_doc).place(x=120, y=320)

    root.mainloop()

# Patient screen
def patient_screen():
    global window
    window = CTk()
    window.geometry("930x580")
    window.resizable(False, False)
    window.title("Hospital Management System")
    window.configure(fg_color='black')

    # Background image
    image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
    imageLabel = CTkLabel(window, image=image, text="")
    imageLabel.grid(row=0, column=0, sticky='n', pady=10)

    # Left Frame
    leftFrame = CTkFrame(window, fg_color="black")
    leftFrame.grid(row=1, column=0, padx=20, pady=20, sticky='n')
    leftFrame.grid_columnconfigure((0, 1), weight=1)

    # Entry Fields
    CTkLabel(leftFrame, text='Enter your CNIC:', font=('ariel', 18, 'bold'), text_color="white").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=0, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Patient Name:', font=('ariel', 18, 'bold'), text_color="white").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=1, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Phone Number:', font=('ariel', 18, 'bold'), text_color="white").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180).grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Functions
    def go_to_opd_screen():
        window.destroy()
        navigation_list.head = navigation_list.go_forward()
        navigation_list.head.screen_func()

    def go_back_to_user_screen():
        window.destroy()
        navigation_list.head = navigation_list.go_previous()
        navigation_list.head.screen_func()

    # Buttons
    buttonFrame = CTkFrame(window, fg_color="black")
    buttonFrame.grid(row=2, column=0, pady=20, sticky='n')

    CTkButton(buttonFrame, text='Generate Token for Emergency', command=lambda: messagebox.showinfo("Emergency", 'Emergency button clicked')).grid(row=0, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Continue to OPD', command=go_to_opd_screen).grid(row=1, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Go Back', command=go_back_to_user_screen).grid(row=2, column=0, padx=10, pady=10)

    window.mainloop()

# Visitor screen
def visitor_screen():
    global window
    window = CTk()
    window.geometry("950x450")
    window.resizable(False, False)
    window.title("Visitor Page")

    # Heading
    CTkLabel(window, text="Visitor Information",
             font=("Arial", 30, "bold"),
             text_color="white").pack(pady=20)

    # Visitor Details Frame
    visitor_frame = CTkFrame(window)
    visitor_frame.pack(pady=10, padx=20)

    CTkLabel(visitor_frame, text="Visitor Name:", font=('Arial', 18), text_color="white").grid(row=0, column=0, pady=10, padx=10)
    CTkEntry(visitor_frame).grid(row=0, column=1, pady=10, padx=10)

    CTkLabel(visitor_frame, text="CNIC:", font=('Arial', 18), text_color="white").grid(row=1, column=0, pady=10, padx=10)
    CTkEntry(visitor_frame).grid(row=1, column=1, pady=10, padx=10)

    CTkLabel(visitor_frame, text="Contact Number:", font=('Arial', 18), text_color="white").grid(row=2, column=0, pady=10, padx=10)
    CTkEntry(visitor_frame).grid(row=2, column=1, pady=10, padx=10)

    def back_to_user_screen():
        window.destroy()
        # Ensure navigation list goes back to the User Screen (main menu)
        while navigation_list.head.data != "User Screen":
            navigation_list.head = navigation_list.go_previous()
        navigation_list.head.screen_func()

    # Buttons
    CTkButton(window, text="Submit", command=lambda: messagebox.showinfo("Submitted", "Visitor details recorded successfully")).pack(pady=10)
    CTkButton(window, text="Back", command=back_to_user_screen).pack(pady=10)

    window.mainloop()

# Suggestion Screen
def suggestion_screen():
    global window
    window = CTk()
    window.geometry("950x450")
    window.resizable(False, False)
    window.title("Suggestion Page")

    CTkLabel(window, text="Add Suggestion",
             font=("Arial", 30, "bold"),
             text_color="white").pack(pady=20)

    suggestion_frame = CTkFrame(window)
    suggestion_frame.pack(pady=10, padx=20)

    suggestion_label = CTkLabel(suggestion_frame, text="Your Suggestion:", font=('Arial', 18), text_color="white")
    suggestion_label.grid(row=0, column=0, pady=10, padx=10)

    suggestion_entry = CTkEntry(suggestion_frame, width=300)  # Suggestion entry field
    suggestion_entry.grid(row=0, column=1, pady=10, padx=10)

    def submit_suggestion():
        suggestion = suggestion_entry.get().strip()
        if suggestion:
            messagebox.showinfo("Submitted", "Thank you for your suggestion!")
        else:
            messagebox.showwarning("Warning", "Please enter a suggestion before submitting.")

    def back_to_user_screen():
        window.destroy()
        # Ensure navigation list goes back to the User Screen (main menu)
        while navigation_list.head.data != "User Screen":
            navigation_list.head = navigation_list.go_previous()
        navigation_list.head.screen_func()

    button_frame = CTkFrame(window)
    button_frame.pack(pady=10)

    # Back Button
    back_button = CTkButton(button_frame, text='Go Back', 
                            font=('Arial', 15, 'bold'), 
                            width=170, 
                            corner_radius=15,
                            command=back_to_user_screen)
    back_button.grid(row=0, column=0, pady=5, padx=5)

    # Submit Button
    submit_button = CTkButton(button_frame, text='Submit Suggestion', 
                               font=('Arial', 15, 'bold'), 
                               width=170, 
                               corner_radius=15,
                               command=submit_suggestion)
    submit_button.grid(row=0, column=1, pady=5, padx=5)

    # Add Treeview table for displaying suggestions
    tree_frame = CTkFrame(window)
    tree_frame.pack(pady=20, padx=20)

    tree = ttk.Treeview(tree_frame, height=13)
    tree.grid(row=0, column=0, columnspan=5)

    tree['columns'] = ['Id', 'Name', 'Phone', 'Age', 'Gender', 'Medicine']
    tree.heading('Id', text='Id')
    tree.heading('Name', text='Name')
    tree.heading('Phone', text='Phone')
    tree.heading('Age', text='Age')
    tree.heading('Gender', text='Gender')
    tree.heading('Medicine', text='Medicine')

    tree.config(show='headings')
    tree.column('Id', width=80)
    tree.column('Name', width=150)
    tree.column('Phone', width=120)
    tree.column('Age', width=80)
    tree.column('Gender', width=100)
    tree.column('Medicine', width=150)

    style = ttk.Style()
    style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))

    # Scroll bar
    scroll_bar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scroll_bar.grid(row=0, column=5, sticky='ns')
    tree.config(yscrollcommand=scroll_bar.set)

    window.mainloop()

# OPD screen
def opd_screen():
    global window
    window = CTk()
    window.geometry("950x580")
    window.resizable(False, False)
    window.title("Hospital Management System")
    window.configure(fg_color='black')

    # Load and configure the background image
    image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
    imageLabel = CTkLabel(window, image=image, text="")
    imageLabel.grid(row=0, column=0, columnspan=2)

    # Add title
    titleLabel = CTkLabel(
        window,
        text="Please select the desired OPD",
        font=("Arial", 30, "bold"),
        text_color="white"
    )
    titleLabel.grid(row=1, column=0, columnspan=2, pady=10)

    # OPD Services List
    opd_services = [
        ("Consultation", "Dr. Ehtisham"),
        ("Pediatrics", "Dr. Ehtisham"),
        ("Surgical", "Dr. Mohsin"),
        ("Psychiatry", "Dr. Zeeshan"),
        ("Orthopedic", "Dr. Ehtisham"),
        ("Cardiology", "Dr. Mohsin"),
        ("Neurology", "Dr. Mohsin"),
        ("Immunizations", "Dr. Zeeshan"),
        ("Dermatology", "Dr. Ehtisham"),
        ("Pulmonology", "Dr. Mohsin"),
        ("Physio-Therapy", "Dr. Zeeshan"),
        ("ENT", "Dr. Zeeshan")
    ]

    # Queue to track OPD tokens
    opd_token_queue = []

    # Function to generate a token
    def generate_token(service, doctor):
        # Token details
        token_number = len(opd_token_queue) + 1
        room_number = 101 + len(opd_token_queue) % 10  # Example room assignment
        token_details = {
            "Token": token_number,
            "Service": service,
            "Doctor": doctor,
            "Room": room_number
        }
        opd_token_queue.append(token_details)

        # Display token information
        token_message = (f"Token Number: {token_number}\n"
                         f"Service: {service}\n"
                         f"Doctor: {doctor}\n"
                         f"Room: {room_number}")
        messagebox.showinfo("OPD Token", token_message)

    # Create OPD Buttons
    buttonFrame = CTkFrame(window)
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=20)

    for i, (service, doctor) in enumerate(opd_services):
        button = CTkButton(
            buttonFrame,
            text=f"{service}",
            font=('Arial', 25, 'bold'),
            width=220,
            corner_radius=10,
            command=lambda s=service, d=doctor: generate_token(s, d)
        )
        button.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def previous():
        window.destroy()
        navigation_list.head = navigation_list.go_previous()
        navigation_list.head.screen_func()

    previousButton = CTkButton(buttonFrame, text='Go Back',
                               cursor='hand2',
                               command=previous,
                               font=('ariel', 30, 'bold'),
                               width=220,
                               corner_radius=15)
    previousButton.grid(row=5, column=1, padx=10, pady=10)

    window.mainloop()

# Populate navigation list
navigation_list.append("User Screen", user_screen)
navigation_list.append("Patient Screen", patient_screen)
navigation_list.append("OPD Screen", opd_screen)
navigation_list.append("Visitor Screen", visitor_screen)
navigation_list.append("Suggestion Screen", suggestion_screen)

# Start application
navigation_list.head.screen_func()