"""
doc_adj.py — Doctor Panel (adjusment.py entry)
================================================
QA-13 FIX: All functions are closures inside run() — no undefined globals.
QA-36 FIX: prev_pat() navigates to correct home screen (adjusment.py user_screen).
QA-19 FIX: next_pat() reads from selected Treeview row (DB-backed).
"""

from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk
import adj_db as ad


def run():
    """Doctor panel for adjusment.py entry point."""

    global window

    def data_view():
        pat_data = ad.fetch_pat_data()
        tree.delete(*tree.get_children())
        for pat in pat_data:
            tree.insert('', 'end', values=pat)

    def clear_data():
        for entry in [cnicEntry, nameEntry, phoneEntry, ageEntry, cityEntry]:
            entry.delete(0, END)
        gender_Box.set('Please Select')
        medicine_Box.set('Please Select')

    def selection(event):
        select_item = tree.selection()
        if select_item:
            row = tree.item(select_item[0])['values']
            clear_data()
            cnicEntry.insert(0, row[1]); nameEntry.insert(0, row[2])
            phoneEntry.insert(0, row[3]); ageEntry.insert(0, row[4])
            cityEntry.insert(0, row[5])
            gender_Box.set(row[6]); medicine_Box.set(row[7])

    def search_pat():
        if searchEntry.get() == '':
            messagebox.showerror('ERROR', 'Enter value to search')
        elif search_Box.get() == 'Please Select':
            messagebox.showerror('ERROR', 'Please select a search option')
        else:
            results = ad.search_db(search_Box.get(), searchEntry.get())
            tree.delete(*tree.get_children())
            if results:
                for pat in results:
                    tree.insert('', 'end', values=pat)
            else:
                messagebox.showinfo('No Results', 'No matching records found.')

    def showall():
        data_view()
        searchEntry.delete(0, END)
        search_Box.set('Please Select')

    def add_pat():
        fields = [cnicEntry.get(), nameEntry.get(), phoneEntry.get(),
                  ageEntry.get(), cityEntry.get()]
        if any(f == '' for f in fields) \
                or gender_Box.get() == 'Please Select' \
                or medicine_Box.get() == 'Please Select':
            messagebox.showerror('Error', 'All fields are required')
            return
        ad.insert(cnicEntry.get(), nameEntry.get(), phoneEntry.get(),
                  ageEntry.get(), cityEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view(); clear_data()

    def up_pat():
        select_item = tree.selection()
        if not select_item:
            messagebox.showerror("Error", 'Select a patient record to update')
            return
        row = tree.item(select_item[0])['values']
        ad.update_db(row[0], cnicEntry.get(), nameEntry.get(), phoneEntry.get(),
                     ageEntry.get(), cityEntry.get(), gender_Box.get(), medicine_Box.get())
        data_view(); clear_data()

    def del_pat():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete")
            return
        row = tree.item(selected_item[0])['values']
        if messagebox.askyesno("Confirm Delete",
                               f"Delete patient '{row[2]}' (CNIC: {row[1]})?"):
            ad.del_db(row[0]); clear_data(); data_view()

    def admit_pat():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to admit")
            return
        row = tree.item(selected_item[0])['values']
        if messagebox.askyesno("Confirm Admission",
                               f"Admit '{row[2]}' (CNIC: {row[1]}) to the ward?"):
            ad.admit_patient(row[1], row[0])
            messagebox.showinfo("Success", f"Patient '{row[2]}' admitted successfully.")

    def next_pat():
        """QA-19 FIX: reads patient info from selected tree row."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a patient to mark as next")
            return
        row = tree.item(selected_item[0])['values']
        messagebox.showinfo(
            "Next Patient",
            f"Processing patient:\n"
            f"  Name  : {row[2]}\n"
            f"  CNIC  : {row[1]}\n"
            f"  Age   : {row[4]}\n"
            f"  City  : {row[5]}\n"
            f"  Gender: {row[6]}\n"
        )

    def prev_pat():
        """QA-36 FIX: go back to adjusment.py user_screen, not ZEM_HMS."""
        window.destroy()
        import adjusment
        adjusment.navigation_list.seek("User Screen")
        adjusment.user_screen()

    # ── UI ─────────────────────────────────────────────────────────────────────
    window = CTk()
    window.geometry("1020x620")
    window.resizable(False, False)
    window.title("Doctor Panel — ZEM Hospital")

    image = CTkImage(Image.open('hms.jpg'), size=(950, 150))
    CTkLabel(window, image=image, text="").grid(row=0, column=0, columnspan=2, sticky="ew")

    leftFrame = CTkFrame(window, fg_color="black")
    leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    lf = dict(font=('Arial', 18, 'bold'), text_color="white")
    ef = dict(font=('Arial', 18, 'bold'), text_color="white", width=180)

    CTkLabel(leftFrame, text='CNIC:',     **lf).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    cnicEntry = CTkEntry(leftFrame, **ef); cnicEntry.grid(row=0, column=1, sticky='ew')

    CTkLabel(leftFrame, text='Name:',     **lf).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    nameEntry = CTkEntry(leftFrame, **ef); nameEntry.grid(row=1, column=1, sticky='ew')

    CTkLabel(leftFrame, text='Phone:',    **lf).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    phoneEntry = CTkEntry(leftFrame, **ef); phoneEntry.grid(row=2, column=1, sticky='ew')

    CTkLabel(leftFrame, text='Age:',      **lf).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    ageEntry = CTkEntry(leftFrame, **ef); ageEntry.grid(row=3, column=1, sticky='ew')

    CTkLabel(leftFrame, text='City:',     **lf).grid(row=4, column=0, padx=10, pady=10, sticky='w')
    cityEntry = CTkEntry(leftFrame, **ef); cityEntry.grid(row=4, column=1, sticky='ew')

    CTkLabel(leftFrame, text='Gender:',   **lf).grid(row=5, column=0, padx=10, pady=10, sticky='w')
    gender_Box = CTkComboBox(leftFrame, values=['Male', 'Female', 'Others'], font=('Arial', 18, 'bold'))
    gender_Box.grid(row=5, column=1, sticky='ew'); gender_Box.set('Please Select')

    CTkLabel(leftFrame, text='Medicine:', **lf).grid(row=6, column=0, padx=10, pady=10, sticky='w')
    medicine_Box = CTkComboBox(leftFrame, values=[
        'Paracetamol', 'Amoxicillin', 'Ibuprofen', 'Metformin',
        'Omeprazole', 'Atorvastatin', 'Amlodipine', 'Other'
    ], font=('Arial', 18, 'bold'))
    medicine_Box.grid(row=6, column=1, sticky='ew'); medicine_Box.set('Please Select')

    rightFrame = CTkFrame(window, fg_color="black")
    rightFrame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    search_Box = CTkComboBox(rightFrame, values=['ID', 'CNIC', 'Name', 'Phone', 'City'],
                             font=('Arial', 18, 'bold'))
    search_Box.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    search_Box.set('Please Select')

    searchEntry = CTkEntry(rightFrame, font=('Arial', 18, 'bold'), text_color="white", width=180)
    searchEntry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    CTkButton(rightFrame, text='Search',   width=80, command=search_pat).grid(row=0, column=2, padx=5, pady=5)
    CTkButton(rightFrame, text='Show All', width=80, command=showall).grid(row=0, column=3, padx=5, pady=5)
    CTkButton(rightFrame, text='Logout',   width=80, command=prev_pat).grid(row=0, column=4, padx=5, pady=5)

    tree = ttk.Treeview(rightFrame, height=15)
    tree.grid(row=1, column=0, columnspan=5, sticky='nsew')
    tree['columns'] = ['Id', 'CNIC', 'Name', 'Phone', 'Age', 'City', 'Gender', 'Medicine']
    for col in tree['columns']:
        tree.heading(col, text=col)
    tree.config(show='headings')
    tree.column('Id', width=50); tree.column('CNIC', width=100); tree.column('Name', width=110)
    tree.column('Phone', width=90); tree.column('Age', width=40); tree.column('City', width=70)
    tree.column('Gender', width=60); tree.column('Medicine', width=140)

    ttk.Style().configure('Treeview.Heading', font=('Arial', 12, 'bold'))
    sb = ttk.Scrollbar(rightFrame, orient='vertical', command=tree.yview)
    sb.grid(row=1, column=5, sticky='ns')
    tree.config(yscrollcommand=sb.set)

    CTkButton(rightFrame, text='Admit Patient', font=('Arial', 15, 'bold'), width=150,
              corner_radius=15, command=admit_pat).grid(row=3, column=0, pady=10, padx=5)
    CTkButton(rightFrame, text='Delete Patient', font=('Arial', 15, 'bold'), width=150,
              corner_radius=15, command=del_pat).grid(row=3, column=1, pady=5, padx=5)
    CTkButton(rightFrame, text='Refer To OPD', font=('Arial', 15, 'bold'), width=150,
              corner_radius=15, command=prev_pat).grid(row=3, column=2, pady=10, padx=5)

    buttonFrame = CTkFrame(window)
    buttonFrame.grid(row=2, column=0, columnspan=2)

    for col, (txt, cmd) in enumerate([
        ('Previous Patient', prev_pat),
        ('Add Patient',      add_pat),
        ('Update Patient',   up_pat),
        ('Clear Fields',     clear_data),
        ('Next Patient',     next_pat),
    ]):
        CTkButton(buttonFrame, text=txt, font=('Arial', 15, 'bold'), width=180,
                  corner_radius=15, command=cmd).grid(row=0, column=col, pady=5, padx=5)

    data_view()
    tree.bind('<<TreeviewSelect>>', selection)
    window.mainloop()


if __name__ == '__main__':
    run()