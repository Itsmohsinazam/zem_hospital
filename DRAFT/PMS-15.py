from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk

# Initialize the main application window
window = CTk()
window.title("Hospital Management System")
window.configure(fg_color='black')

# Load and configure the background image
image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
imageLabel = CTkLabel(window, image=image, text="")  # Use text="" to avoid overlap
imageLabel.grid(row=0, column=0, columnspan=2, sticky='nsew')  # Span across both left and right frames

# Left Frame for patient details
leftFrame = CTkFrame(window, fg_color="black")
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# Patient ID
idLabel = CTkLabel(leftFrame, text='Patient ID:', font=('ariel', 18, 'bold'), text_color="white")
idLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')
idEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
idEntry.grid(row=0, column=1, sticky='w')

# Patient Name
nameLabel = CTkLabel(leftFrame, text='Patient Name:', font=('ariel', 18, 'bold'), text_color="white")
nameLabel.grid(row=1, column=0, padx=10, pady=10, sticky='w')
nameEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
nameEntry.grid(row=1, column=1, sticky='w')

# Phone Number
phoneLabel = CTkLabel(leftFrame, text='Phone Number:', font=('ariel', 18, 'bold'), text_color="white")
phoneLabel.grid(row=2, column=0, padx=10, pady=10, sticky='w')
phoneEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
phoneEntry.grid(row=2, column=1, sticky='w')

# Age
ageLabel = CTkLabel(leftFrame, text='Age:', font=('ariel', 18, 'bold'), text_color="white")
ageLabel.grid(row=3, column=0, padx=10, pady=10, sticky='w')
ageEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
ageEntry.grid(row=3, column=1, sticky='w')

# Gender
genderLabel = CTkLabel(leftFrame, text='Gender:', font=('ariel', 18, 'bold'), text_color="white")
genderLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')
genders = ['Male', 'Female', 'Others']
gender_Box = CTkComboBox(leftFrame, values=genders, font=('ariel', 18, 'bold'))
gender_Box.grid(row=4, column=1, sticky='w')
gender_Box.set('Please Select')

# Medicine
medicineLabel = CTkLabel(leftFrame, text='Medicine:', font=('ariel', 18, 'bold'), text_color="white")
medicineLabel.grid(row=5, column=0, padx=10, pady=10, sticky='w')
medicine_available = ['Geratology', 'Hayology', 'Tameezology']
medicine_Box = CTkComboBox(leftFrame, values=medicine_available, font=('ariel', 18, 'bold'))
medicine_Box.grid(row=5, column=1, sticky='w')
medicine_Box.set('Please Select')

# Right Frame for actions and search functionality
rightFrame = CTkFrame(window, fg_color="black")
rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Search Label
searchLabel = CTkLabel(rightFrame, text='Search:', font=('ariel', 18, 'bold'), text_color="white")
searchLabel.grid(row=0, column=0, padx=10, pady=10, sticky='n')

# Search Options
search_options = ['ID', 'Name', 'Phone']
search_Box = CTkComboBox(rightFrame, values=search_options, font=('ariel', 18, 'bold'))
search_Box.grid(row=0, column=0)
search_Box.set('Please Select')

searchEntry = CTkEntry(rightFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
searchEntry.grid(row=0, column=1)

searchButton = CTkButton(rightFrame, text='Search', width=100)
searchButton.grid(row=0, column=2)

showallButton = CTkButton(rightFrame, text='Show All', width=100)
showallButton.grid(row=0, column=3, pady=5)

# Configure Treeview
tree = ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=4, sticky='nsew')

tree['columns'] = ['Id', 'Name', 'Phone Number', 'Age', 'Gender', 'Medicine']

tree.heading('Id', text='Id')
tree.heading('Name', text='Name')
tree.heading('Phone Number', text='Phone Number')
tree.heading('Age', text='Age')
tree.heading('Gender', text='Gender')
tree.heading('Medicine', text='Medicine')

tree.config(show='headings')
tree.column('Id', width=80)
tree.column('Name', width=150)
tree.column('Phone Number', width=120)
tree.column('Age', width=50)
tree.column('Gender', width=100)
tree.column('Medicine', width=150)

style = ttk.Style()
style.configure('Treeview.Heading', font=('ariel', 15, 'bold'))

window.mainloop()
