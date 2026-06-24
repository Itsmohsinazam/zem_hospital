from customtkinter import *
from PIL import Image
from tkinter import messagebox

def login():
    if userName.get() == '' or userPassword.get()=='':
        messagebox.showerror('Error', 'All fields are required')
    elif userName.get() =='abc' and userPassword.get()=='123':
        root.destroy()
        import doctor_screen
    else:
        messagebox.showerror('Error','Wrong credentials')


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

userName = CTkEntry(root, placeholder_text = 'Enter your Username')
userName.place(x=120, y=190)

userPassword = CTkEntry(root, placeholder_text = 'Enter your Password', show ='*')
userPassword.place(x=120, y=230)

loginButton = CTkButton(root, text='Login', cursor='hand2', command=login)
loginButton.place(x=120, y=270)


def previous():
    root.destroy()
    import user_screen

previousButton = CTkButton(root, text='Previous', cursor='hand2', command=previous)
previousButton.place(x=120, y=310)

root.mainloop()