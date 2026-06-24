from customtkinter import CTk, CTkButton, CTkLabel, CTkImage
from PIL import Image

# Initialize the main application window
root = CTk()
root.geometry("950x450")  
root.resizable(False, False)  # Non-resizable window
root.title("Login Page")

# Load and configure the background image
try:
    image = CTkImage(Image.open('zem.png'), size=(950, 450))
    imageLabel = CTkLabel(root, image=image, text="")  # Use text="" to avoid overlap
    imageLabel.place(x=0, y=0)
except FileNotFoundError:
    print("Error: 'zem.png' not found. Please ensure the file exists in the correct path.")

# Run the application
root.mainloop()
