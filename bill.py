from customtkinter import *
from PIL import Image
from tkinter import messagebox

# Initialize the main application window
root = CTk()
root.geometry("900x450")  
root.resizable(False, False)  
root.title("Login Page")

# Load and configure the background image
image = CTkImage(Image.open('bill.png'), size=(950, 450))
imageLabel = CTkLabel(root, image=image, text="")  # Use text="" to avoid overlap
imageLabel.place(x=0, y=0)

# id
patient_id = CTkLabel(root, text="Patient ID:", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_id.place(x=300, y=150)

# id value
patient_id = CTkLabel(root, text="1001", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_id.place(x=600, y=150)

# name
patient_name = CTkLabel(root, text="Name:", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_name.place(x=300, y=200)

# name value
patient_id = CTkLabel(root, text="1001", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_id.place(x=600, y=200)

# Examained By
examained_by = CTkLabel(root, text="Examained By:", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
examained_by.place(x=300, y=250)

# dr value
patient_id = CTkLabel(root, text="1001", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_id.place(x=600, y=250)

# Bill
examained_by = CTkLabel(root, text="Bill:", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
examained_by.place(x=300, y=300)

# bill value
patient_id = CTkLabel(root, text="1001", 
                        fg_color="white",  # Background color
                        text_color="black",  # Text color
                        font=("Goudy Old Style", 18, "bold"))  # Custom font
patient_id.place(x=600, y=300)

root.mainloop()