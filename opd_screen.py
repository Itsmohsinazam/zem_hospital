from customtkinter import *
from PIL import Image
from tkinter import messagebox

# Initialize the main application window
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

#previous button
def previous():
    window.destroy()
    import user_screen

previousButton = CTkButton(buttonFrame, text='Go to Main Meanu', 
                           cursor='hand2', 
                           command=previous, 
                           font=('ariel', 30,'bold'), 
                           width=220, 
                           corner_radius=15)
previousButton.grid(row=5, column=1, padx=10, pady=10)

# Run the application
window.mainloop()
