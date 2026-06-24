from customtkinter import *
from PIL import Image
from tkinter import messagebox

def patient():
    root.destroy()
    import patient_screen

def visitor():
    messagebox.showinfo("Sabar", 'Under construction')
    root.destroy()

def suggestion():
    messagebox.showinfo("Sabar", 'Under construction')
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