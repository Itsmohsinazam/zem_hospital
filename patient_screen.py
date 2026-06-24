from customtkinter import *
from PIL import Image
from tkinter import messagebox

#functions
def emergency():
    messagebox.showinfo("Emergency", 'Emergency button clicked')
    window.destroy()

def opd():
    messagebox.showinfo("OPD", 'OPD button clicked')
    window.destroy()

def previous():
    window.destroy()
    import user_screen

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

# Button frame
buttonFrame = CTkFrame(window, fg_color="black")
buttonFrame.grid(row=2, column=0, pady=20, sticky='n')

emergencyButton = CTkButton(buttonFrame, text='Generate token for Emergency', 
                            cursor='hand2', 
                            command=emergency,
                            font=('ariel', 15,'bold'), 
                            width=170, 
                            corner_radius=15)
emergencyButton.grid(row=0, column=0, padx=10, pady=10)

opdButton = CTkButton(buttonFrame, text='Continue to OPD', 
                            cursor='hand2', 
                            command=opd, 
                            font=('ariel', 15,'bold'), 
                            width=170, 
                            corner_radius=15)
opdButton.grid(row=1, column=0, padx=10, pady=10)

previousButton = CTkButton(buttonFrame, text='Go to Main Meanu', 
                           cursor='hand2', 
                           command=previous, 
                           font=('ariel', 15,'bold'), 
                           width=170, 
                           corner_radius=15)
previousButton.grid(row=2, column=0, padx=10, pady=10)

# Run the application
window.mainloop()