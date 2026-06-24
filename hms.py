from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk
import hms_db

# Functions
def search_pat():
    if searchEntry.get()=='':
        messagebox.showerror('ERROR', 'Enter value to search')
    elif search_Box.get()=='':
        messagebox.showerror('ERROR', 'Please, select an option')
    else:
        search_data=hms_db.search_db(search_Box.get(), searchEntry.get())
        tree.delete(*tree.get_children())  
        for pat in search_data:
            tree.insert('', 'end', values=pat)  

def showall():
    data_view()
    searchEntry.delete(0,END)
    search_Box.set('Search By')

def data_view():
    pat_data = hms_db.fetch_pat_data()
    tree.delete(*tree.get_children())  
    for pat in pat_data:
        tree.insert('', 'end', values=pat)  

def clear_data():
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    ageEntry.delete(0, END)
    gender_Box.set('Please Select')
    medicine_Box.set('Please Select')

def selection(event):
    select_item = tree.selection()
    if select_item:
        row = tree.item(select_item[0])['values']
        clear_data()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        phoneEntry.insert(0, row[2])
        ageEntry.insert(0, row[3])
        gender_Box.set(row[4])
        medicine_Box.set(row[5])

def prev_pat():
    window.destroy()
    import user_screen

def add_pat():
    if idEntry.get() == '' or phoneEntry.get() == '' or nameEntry.get() == '' or ageEntry.get() == '' or gender_Box.get() == '' or medicine_Box.get() == '':
        messagebox.showerror('Error', 'All fields are required')
        return  # Return to avoid further execution
    elif hms_db.id_exists(idEntry.get()):
        messagebox.showerror('Error', 'ID already exists')
    else:
        hms_db.insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), ageEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view()  # Refresh the data view after adding
        clear_data()

def up_pat():
    select_item=tree.selection()
    if not select_item:
        messagebox.ERROR("Error", 'Select data to update')
    else:
        hms_db.update_db(idEntry.get(), nameEntry.get(), phoneEntry.get(), ageEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view()
        clear_data()
        messagebox.showinfo("Success", 'Data Updated Successfully')

def del_pat():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a patient to remove")
        return
    else:
        hms_db.del_db(idEntry.get())  
        clear_data()
        messagebox.showinfo("Success", "Patient Data removed")
        data_view() 

def next_pat():
    window.destroy()

# Initialize the main application window
window = CTk()
window.geometry("950x580")
window.resizable(False, False)
window.title("Hospital Management System")
window.configure(fg_color='black')

# Load and configure the background image
image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
imageLabel = CTkLabel(window, image=image, text="")  # Use text="" to avoid overlap
imageLabel.grid(row=0, column=0, columnspan=2)  # Span across both left and right frames

# Left Frame for patient details
leftFrame = CTkFrame(window, fg_color="black")
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# Patient ID
idLabel = CTkLabel(leftFrame, text='ID:', font=('ariel', 18, 'bold'), text_color="white")
idLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')
idEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
idEntry.grid(row=0, column=1, sticky='w')

# Patient Name
nameLabel = CTkLabel(leftFrame, text='Name:', font=('ariel', 18, 'bold'), text_color="white")
nameLabel.grid(row=1, column=0, padx=10, pady=10, sticky='w')
nameEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
nameEntry.grid(row=1, column=1, sticky='w')

# Phone Number
phoneLabel = CTkLabel(leftFrame, text='Phone:', font=('ariel', 18, 'bold'), text_color="white")
phoneLabel.grid(row=2, column=0, padx=10, pady=10, sticky='w')
phoneEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
phoneEntry.grid(row=2, column=1, sticky='w')

# Age
ageLabel = CTkLabel(leftFrame, text='Age:', font=('ariel', 18, 'bold'), text_color="white")
ageLabel.grid(row=3, column=0, padx=10, pady=10, sticky='w')
ageEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
ageEntry.grid(row=3, column=1, sticky='w')

# city
cityLabel = CTkLabel(leftFrame, text='City:', font=('ariel', 18, 'bold'), text_color="white")
cityLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')
cityEntry = CTkEntry(leftFrame, font=('ariel', 18, 'bold'), text_color="white", width=180)
cityEntry.grid(row=4, column=1, sticky='w')

# Gender
genderLabel = CTkLabel(leftFrame, text='Gender:', font=('ariel', 18, 'bold'), text_color="white")
genderLabel.grid(row=5, column=0, padx=10, pady=10, sticky='w')
genders = ['Male', 'Female', 'Others']
gender_Box = CTkComboBox(leftFrame, values=genders, font=('ariel', 18, 'bold'))
gender_Box.grid(row=5, column=1, sticky='w')
gender_Box.set('Please Select')

# Medicine
medicineLabel = CTkLabel(leftFrame, text='Medicine:', font=('ariel', 18, 'bold'), text_color="white")
medicineLabel.grid(row=6, column=0, padx=10, pady=10, sticky='w')
medicine_available = ['Geratology', 'Hayology', 'Tameezology']
medicine_Box = CTkComboBox(leftFrame, values=medicine_available, font=('ariel', 18, 'bold'))
medicine_Box.grid(row=6, column=1, sticky='w')
medicine_Box.set('Please Select')

# Right Frame for actions and search functionality
rightFrame = CTkFrame(window, fg_color="black")
rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

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

searchButton=CTkButton(rightFrame, text='Search', width=100,
                       command=search_pat)
searchButton.grid(row=0, column=2)

showallButton=CTkButton(rightFrame, text='Show All', width=100,
                        command=showall)
showallButton.grid(row=0, column=3, pady=5)

tree=ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=6)

tree['columns']=['Id','Name','Phone','Age','Gender','Medicine']

tree.heading('Id',text='Id')
tree.heading('Name',text='Name')
tree.heading('Phone',text='Phone')
tree.heading('Age',text='Age')
tree.heading('Gender',text='Gender')
tree.heading('Medicine',text='Medicine')

tree.config(show='headings')
tree.column('Id', width=80)
tree.column('Name', width=150)
tree.column('Phone', width=120)
tree.column('Age', width=80)
tree.column('Gender', width=100)
tree.column('Medicine', width=150)

style=ttk.Style()
style.configure('Treeview.Heading', 
                font=('ariel', 12,'bold'))

#scroll bar
scroll_bar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scroll_bar.grid(row=1, column=5, sticky='ns')
tree.config(yscrollcommand=scroll_bar.set)

buttonFrame=CTkFrame(window)
buttonFrame.grid(row=2, column=0, columnspan=2)

#previous
prevButton=CTkButton(buttonFrame, text='Previous Patient', 
                    font=('ariel', 15,'bold'), 
                    width=170, 
                    corner_radius=15,
                    command=prev_pat)
prevButton.grid(row=0, column=0, pady=5, padx=5)

#add patient
addButton=CTkButton(buttonFrame, text='Add Patient', 
                    font=('ariel', 15,'bold'), 
                    width=170, 
                    corner_radius=15,
                    command=add_pat)
addButton.grid(row=0, column=1, pady=5, padx=5)

#update data
updateButton=CTkButton(buttonFrame, text='Update Patient Data', 
                    font=('ariel', 15,'bold'), 
                    width=170, 
                    corner_radius=15,
                    command=up_pat)
updateButton.grid(row=0, column=2, pady=5, padx=5)

#Delete button
delButton=CTkButton(buttonFrame, text='Delete Patient', 
                    font=('ariel', 15,'bold'), 
                    width=170, 
                    corner_radius=15,
                    command=del_pat)
delButton.grid(row=0, column=3, pady=5, padx=5)

#next patient
nextButton=CTkButton(buttonFrame, text='Next Patient', 
                    font=('ariel', 15,'bold'), 
                    width=170, 
                    corner_radius=15,
                    command=next_pat)
nextButton.grid(row=0, column=4, pady=5, padx=5)

data_view()
tree.bind('<ButtonRelease-1>', selection)
window.mainloop()