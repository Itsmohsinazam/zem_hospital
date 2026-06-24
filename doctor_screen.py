from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk
import patient_db as ad
import queue

# Functions
def search_pat():
    if searchEntry.get() == '':
        messagebox.showerror('ERROR', 'Enter value to search')
    elif search_Box.get() == 'Please Select':
        messagebox.showerror('ERROR', 'Please, select an option')
    else:
        print(f"Searching for {search_Box.get()} with value {searchEntry.get()}")  # Debug log
        search_data = ad.search_db(search_Box.get(), searchEntry.get())
        tree.delete(*tree.get_children())
        if search_data:
            for pat in search_data:
                tree.insert('', 'end', values=pat)
        else:
            messagebox.showinfo('No Results', 'No matching records found.')

def showall():
    data_view()
    searchEntry.delete(0, END)
    search_Box.set('Please Select')

def data_view():
    pat_data = ad.fetch_pat_data()
    tree.delete(*tree.get_children())
    for pat in pat_data:
        tree.insert('', 'end', values=pat)

def clear_data():
    cnicEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    ageEntry.delete(0, END)
    cityEntry.delete(0, END)
    gender_Box.set('Please Select')
    medicine_Box.set('Please Select')

def selection(event):
    select_item = tree.selection()
    if select_item:
        row = tree.item(select_item[0])['values']
        clear_data()
        cnicEntry.insert(0, row[1])
        nameEntry.insert(0, row[2])
        phoneEntry.insert(0, row[3])
        ageEntry.insert(0, row[4])
        cityEntry.insert(0, row[5])
        gender_Box.set(row[6])
        medicine_Box.set(row[7])
    else:
        messagebox.showerror("Error", "No row selected")

def prev_pat():
    window.destroy()
    import ZEM_HMS

def add_pat():
    if any(entry.get() == '' for entry in [cnicEntry, phoneEntry, nameEntry, ageEntry, cityEntry]) or gender_Box.get() == 'Please Select' or medicine_Box.get() == 'Please Select':
        messagebox.showerror('Error', 'All fields are required')
    else:
        ad.insert(cnicEntry.get(), nameEntry.get(), phoneEntry.get(), ageEntry.get(), cityEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view()
        clear_data()

def up_pat():
    select_item = tree.selection()
    if not select_item:
        messagebox.showerror("Error", 'Select data to update')
    else:
        row = tree.item(select_item[0])['values']
        ad.update_db(row[0], cnicEntry.get(), nameEntry.get(), phoneEntry.get(), ageEntry.get(), cityEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view()
        clear_data()

def del_pat():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient to remove")
    else:
        row = tree.item(selected_item[0])['values']
        ad.del_db(row[0])
        clear_data()
        data_view()

def admit_pat():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient to admit")
    else:
        messagebox.showinfo("Success", "Patient Admitted Successfully")


# Function to pop the first emergency token
def pop_first_emergency_token():
    """
    queue = zem.get_emergency_token_queue()
    if queue:
        return queue.pop(0)  # Pop the first element
    else:
        raise IndexError("The emergency token queue is empty!")
    """
    
def next_pat():
    select_item = tree.selection()
    if not select_item:
        messagebox.showerror("Error", 'Select data to update')
    else:
        row = tree.item(select_item[0])['values']
        ad.update_db(row[0], cnicEntry.get(), nameEntry.get(), phoneEntry.get(), ageEntry.get(), cityEntry.get(), gender_Box.get(), medicine_Box.get())
        pop_first_emergency_token()

# Initialize the main application window
window = CTk()
window.geometry("1020x620")
window.resizable(False, False)

# Load and configure the background image
image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
imageLabel = CTkLabel(window, image=image, text="")  # Use text="" to avoid overlap
imageLabel.grid(row=0, column=0, columnspan=2, sticky="ew")  # Span across both left and right frames

# Left Frame for patient details
leftFrame = CTkFrame(window, fg_color="black")
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# CNIC
cnicLabel = CTkLabel(leftFrame, text='CNIC:', font=('ariel', 18, 'bold'), text_color="white")
cnicLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')
cnicEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
cnicEntry.grid(row=0, column=1, sticky='ew')

# Patient Name
nameLabel = CTkLabel(leftFrame, text='Name:', font=('ariel', 18, 'bold'), text_color="white")
nameLabel.grid(row=1, column=0, padx=10, pady=10, sticky='w')
nameEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
nameEntry.grid(row=1, column=1, sticky='ew')

# Phone Number
phoneLabel = CTkLabel(leftFrame, text='Phone:', font=('ariel', 18, 'bold'), text_color="white")
phoneLabel.grid(row=2, column=0, padx=10, pady=10, sticky='w')
phoneEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
phoneEntry.grid(row=2, column=1, sticky='ew')

# Age
ageLabel = CTkLabel(leftFrame, text='Age:', font=('ariel', 18, 'bold'), text_color="white")
ageLabel.grid(row=3, column=0, padx=10, pady=10, sticky='w')
ageEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
ageEntry.grid(row=3, column=1, sticky='ew')

# City
cityLabel = CTkLabel(leftFrame, text='City:', font=('ariel', 18, 'bold'), text_color="white")
cityLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')
cityEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
cityEntry.grid(row=4, column=1, sticky='ew')

# Gender
genderLabel = CTkLabel(leftFrame, text='Gender:', font=('ariel', 18, 'bold'), text_color="white")
genderLabel.grid(row=5, column=0, padx=10, pady=10, sticky='w')
genders = ['Male', 'Female', 'Others']
gender_Box = CTkComboBox(leftFrame, values=genders, font=('ariel', 18, 'bold'))
gender_Box.grid(row=5, column=1, sticky='ew')
gender_Box.set('Please Select')

# Medicine
medicineLabel = CTkLabel(leftFrame, text='Medicine:', font=('ariel', 18, 'bold'), text_color="white")
medicineLabel.grid(row=6, column=0, padx=10, pady=10, sticky='w')
medicine_available = ['Geratology', 'Hayology', 'Tameezology']
medicine_Box = CTkComboBox(leftFrame, values=medicine_available, font=('ariel', 18, 'bold'))
medicine_Box.grid(row=6, column=1, sticky='ew')
medicine_Box.set('Please Select')

# Right Frame for actions and search functionality
rightFrame = CTkFrame(window, fg_color="black")
rightFrame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Search Options
search_options = ['ID', 'CNIC','Name', 'Phone', 'City']
search_Box = CTkComboBox(rightFrame, values=search_options, font=('ariel', 18, 'bold'))
search_Box.grid(row=0, column=0, padx=5, pady=5, sticky='ew')  # Expand horizontally with padding
search_Box.set('Please Select')

# Search Entry
searchEntry = CTkEntry(rightFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
searchEntry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')  # Expand horizontally with padding

# Search Button
searchButton = CTkButton(rightFrame, text='Search', width=80, command=search_pat)
searchButton.grid(row=0, column=2, padx=5, pady=5, sticky='ew')  # Expand horizontally with padding

# Show All Button
showallButton = CTkButton(rightFrame, text='Show All', width=80, command=showall)
showallButton.grid(row=0, column=3, padx=5, pady=5, sticky='ew')  # Expand horizontally with padding

# Logout Button
logoutButton = CTkButton(rightFrame, text='Logout', width=80, command=prev_pat)
logoutButton.grid(row=0, column=4, padx=5, pady=5, sticky='ew')  # Expand horizontally with padding

# Treeview
tree = ttk.Treeview(rightFrame, height=15)
tree.grid(row=1, column=0, columnspan=5, sticky='nsew')

tree['columns'] = ['Id', 'CNIC', 'Name', 'Phone', 'Age', 'City', 'Gender', 'Medicine']

tree.heading('Id', text='Id')
tree.heading('CNIC', text='CNIC')  
tree.heading('Name', text='Name')
tree.heading('Phone', text='Phone')
tree.heading('Age', text='Age')
tree.heading('City', text='City')
tree.heading('Gender', text='Gender')
tree.heading('Medicine', text='Medicine')

tree.config(show='headings')
tree.column('Id', width=70)
tree.column('CNIC', width=80) 
tree.column('Name', width=100)
tree.column('Phone', width=80)
tree.column('Age', width=40)
tree.column('City', width=70)
tree.column('Gender', width=55)
tree.column('Medicine', width=140)

style = ttk.Style()
style.configure('Treeview.Heading', font=('ariel', 12, 'bold'))

# Scrollbar
scroll_bar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scroll_bar.grid(row=1, column=5, sticky='ns')
tree.config(yscrollcommand=scroll_bar.set)

# Admit Button
admitButton = CTkButton(rightFrame, text='Admit Patient', font=('ariel', 15, 'bold'), width=150, corner_radius=15, command=admit_pat)
admitButton.grid(row=3, column=0, pady=10, padx=5, sticky='ew')

# Delete Button
delButton = CTkButton(rightFrame, text='Delete Patient', font=('ariel', 15, 'bold'), width=170, corner_radius=15, command=del_pat)
delButton.grid(row=3, column=1, pady=5, padx=5, sticky='ew')

# Refer To OPD Button
referButton = CTkButton(rightFrame, text='Refer To OPD', font=('ariel', 15, 'bold'), width=150, corner_radius=15, command=prev_pat)
referButton.grid(row=3, column=2, pady=10, padx=5, sticky='ew')

# Button Frame for Previous, Add, Update, Next Buttons
buttonFrame = CTkFrame(window)
buttonFrame.grid(row=2, column=0, columnspan=2)

# Previous Button
prevButton = CTkButton(buttonFrame, text='Previous Patient', font=('ariel', 15, 'bold'), width=180, corner_radius=15, command=prev_pat)
prevButton.grid(row=0, column=0, pady=5, padx=5)

# Add Button
addButton = CTkButton(buttonFrame, text='Add Patient', font=('ariel', 15, 'bold'), width=180, corner_radius=15, command=add_pat)
addButton.grid(row=0, column=1, pady=5, padx=5)

# Update Button
updateButton = CTkButton(buttonFrame, text='Update Patient Data', font=('ariel', 15, 'bold'), width=180, corner_radius=15, command=up_pat)
updateButton.grid(row=0, column=2, pady=5, padx=5)

# clear data
clearButton = CTkButton(buttonFrame, text='Clear Fields', font=('ariel', 15, 'bold'), width=180, corner_radius=15, command=clear_data)
clearButton.grid(row=0, column=3, pady=5, padx=5)

# Next Button
nextButton = CTkButton(buttonFrame, text='Next Patient', font=('ariel', 15, 'bold'), width=180, corner_radius=15, command=next_pat)
nextButton.grid(row=0, column=4, pady=5, padx=5)

# Binding the selection function to the Treeview
data_view()
tree.bind('<<TreeviewSelect>>', selection)
window.mainloop()