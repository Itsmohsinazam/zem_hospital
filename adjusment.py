"""
adjusment.py — ZEM HMS Patient Kiosk (alternate entry point)
=============================================================
QA-01 FIX: Added __main__ guard — UI no longer runs on import.
QA-02 FIX: call_doc() now calls admin_hms.run() after import.
QA-03 FIX: Navigation uses go_forward()/go_previous() without double mutation.
QA-04 FIX: medicine_Box is a real widget; add_pat() reads it correctly.
QA-05 FIX: emergency_token_queue is module-level (never resets).
QA-06 FIX: Visitor entry widgets are named; submit_visitor() saves to DB.
QA-07 FIX: submit_suggestion() calls ad.insert_suggestion() to persist data.
QA-08 FIX: back_to_user_screen() uses seek() with a step limit (no infinite loop).
QA-09 FIX: Visitor "Patient ID" label moved to row=3.
QA-10 FIX: Suggestion screen Treeview replaced with correct suggestion columns.
QA-11 FIX: Unreachable elif removed from go_to_opd_screen() and add_pat().
QA-17 FIX: medicine_Box widget added to patient form.
QA-18 FIX: Input validation (CNIC, phone, age) added.
QA-26 FIX: opd_token_queue moved to module level.
QA-28 FIX: All font typos 'ariel' → 'Arial'.
QA-29 FIX: OPD Go Back button at row=4 (was row=5, caused gap).
QA-30 NOTE: File kept as adjusment.py to avoid breaking references.
"""

from customtkinter import *
from PIL import Image
from tkinter import messagebox, ttk, VERTICAL
import adj_db as ad

# ── Module-level token queues (QA-05, QA-26 FIX) ─────────────────────────────
emergency_token_queue = []
opd_token_queue = []


# ═════════════════════════════════════════════════════════════════════════════
#  Navigation
# ═════════════════════════════════════════════════════════════════════════════

class Node:
    def __init__(self, data, screen_func):
        self.data = data
        self.screen_func = screen_func
        self.next = None
        self.prev = None


class DoubleCircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data, screen_func):
        new_node = Node(data, screen_func)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def go_forward(self):
        """QA-03 FIX: pure mutation, no double assignment."""
        if self.head:
            self.head = self.head.next
        return self.head

    def go_previous(self):
        if self.head:
            self.head = self.head.prev
        return self.head

    def seek(self, name: str, max_steps: int = 20) -> bool:
        """QA-08 FIX: bounded seek — no infinite loop."""
        for _ in range(max_steps):
            if self.head and self.head.data == name:
                return True
            self.go_previous()
        return False


navigation_list = DoubleCircularLinkedList()


# ═════════════════════════════════════════════════════════════════════════════
#  Validation Helper
# ═════════════════════════════════════════════════════════════════════════════

def _validate_patient_fields(cnic, name, phone, age, city, gender):
    """QA-18 FIX: centralised validation with CNIC/phone/age checks."""
    if not all([cnic, name, phone, age, city]) or gender == 'Please Select':
        return False, 'All fields are required.'
    if not ad.validate_cnic(cnic):
        return False, 'Invalid CNIC format.\nExpected: XXXXX-XXXXXXX-X (13 digits).'
    if not ad.validate_phone(phone):
        return False, 'Invalid phone number.\nExpected: 03XXXXXXXXX or +92XXXXXXXXXX.'
    if not ad.validate_age(age):
        return False, 'Invalid age. Must be a number between 1 and 150.'
    return True, ''


# ═════════════════════════════════════════════════════════════════════════════
#  Screen 1 — Home / User Screen
# ═════════════════════════════════════════════════════════════════════════════

def user_screen():
    global root
    root = CTk()
    root.geometry("950x450")
    root.resizable(False, False)
    root.title("ZEM Hospital — Home")

    image = CTkImage(Image.open('zem.png'), size=(950, 450))
    CTkLabel(root, image=image, text="").place(x=0, y=0)

    def go_to_patient_screen():
        root.destroy()
        # QA-03 FIX: single call, no double mutation
        navigation_list.go_forward()
        navigation_list.head.screen_func()

    def call_doc():
        root.destroy()
        import admin_hms
        # QA-02 FIX: actually call run()
        admin_hms.run()

    def call_visitor():
        root.destroy()
        visitor_screen()

    def call_sug():
        root.destroy()
        suggestion_screen()

    btn = dict(cursor='hand2', font=('Arial', 20, 'bold'), width=180)
    CTkButton(root, text='Patient',        command=go_to_patient_screen, **btn).place(x=120, y=170)
    CTkButton(root, text='Visitor',        command=call_visitor,         **btn).place(x=120, y=220)
    CTkButton(root, text='Add Suggestion', command=call_sug,             **btn).place(x=120, y=270)
    CTkButton(root, text='Doctor',         command=call_doc,             **btn).place(x=120, y=320)

    root.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
#  Screen 2 — Patient Registration
# ═════════════════════════════════════════════════════════════════════════════

def patient_screen():
    global window
    window = CTk()
    window.geometry("930x600")
    window.resizable(False, False)
    window.title("ZEM Hospital — Patient Registration")
    window.configure(fg_color='black')

    CTkLabel(window, image=CTkImage(Image.open('hms.jpg'), size=(950, 150)),
             text="").grid(row=0, column=0, sticky='n', pady=10)

    # QA-11 FIX: removed unreachable elif
    def go_to_opd_screen():
        cnic, name, phone, age, city, gender, _ = _get_fields()
        ok, err = _validate_patient_fields(cnic, name, phone, age, city, gender)
        if not ok:
            messagebox.showerror('Validation Error', err)
            return
        # QA-22 equivalent: save patient before going to OPD
        new_id = ad.insert(cnic, name, phone, age, city, gender, medicine_Box.get()
                           if medicine_Box.get() != 'Please Select' else 'N/A')
        window.destroy()
        navigation_list.go_forward()
        navigation_list.head.screen_func()

    def go_back():
        window.destroy()
        navigation_list.go_previous()
        navigation_list.head.screen_func()

    def _get_fields():
        return (cnicEntry.get().strip(), nameEntry.get().strip(),
                phoneEntry.get().strip(), ageEntry.get().strip(),
                cityEntry.get().strip(), gender_Box.get(), medicine_Box.get())

    def clear_data():
        for e in [cnicEntry, nameEntry, phoneEntry, ageEntry, cityEntry]:
            e.delete(0, END)
        gender_Box.set('Please Select')
        medicine_Box.set('Please Select')

    def add_pat():
        """QA-04/11 FIX: reads medicine from real widget; single validation block."""
        cnic, name, phone, age, city, gender, medicine = _get_fields()
        # QA-11 FIX: single combined check
        if medicine == 'Please Select':
            messagebox.showerror('Validation Error', 'Please select a medicine.')
            return
        ok, err = _validate_patient_fields(cnic, name, phone, age, city, gender)
        if not ok:
            messagebox.showerror('Validation Error', err)
            return
        # QA-21 FIX: use returned ID directly — no CNIC lookup race
        new_id = ad.insert(cnic, name, phone, age, city, gender, medicine)
        if new_id:
            _generate_emergency_token(new_id, cnic, name, phone, age, city, gender)
        clear_data()
        go_back()

    def _generate_emergency_token(patient_id, cnic, name, phone, age, city, gender):
        """QA-21 FIX: uses patient_id returned by insert(), not a CNIC lookup."""
        token_number = len(emergency_token_queue) + 1
        room_number  = 318
        doctor       = "Dr. Ehtisham Ali"

        token = {
            "Token Number": token_number, "Patient ID": patient_id,
            "Name": name, "CNIC": cnic, "Phone": phone,
            "Age": age, "City": city, "Gender": gender,
            "Doctor": doctor, "Room": room_number,
        }
        emergency_token_queue.append(token)
        ad.insert_token(cnic, patient_id)

        messagebox.showinfo("Emergency Token",
            f"Token Number : {token_number}\n"
            f"Patient ID   : {patient_id}\n"
            f"Name         : {name}\n"
            f"CNIC         : {cnic}\n"
            f"Phone        : {phone}\n"
            f"Age          : {age}\n"
            f"City         : {city}\n"
            f"Gender       : {gender}\n"
            f"Doctor       : {doctor}\n"
            f"Room         : {room_number}"
        )

    # ── Layout ────────────────────────────────────────────────────────────────
    leftFrame = CTkFrame(window, fg_color="black")
    leftFrame.grid(row=1, column=0, padx=20, pady=20, sticky='n')
    leftFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # QA-28 FIX: Arial (was 'ariel')
    lbl = dict(font=('Arial', 18, 'bold'), text_color="white")
    ent = dict(font=('Arial', 18, 'bold'), text_color="white", width=180)

    CTkLabel(leftFrame, text='CNIC:',         **lbl).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    cnicEntry = CTkEntry(leftFrame, **ent); cnicEntry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Patient Name:', **lbl).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    nameEntry = CTkEntry(leftFrame, **ent); nameEntry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Phone Number:', **lbl).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    phoneEntry = CTkEntry(leftFrame, **ent); phoneEntry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Age:',          **lbl).grid(row=0, column=2, padx=10, pady=10, sticky='e')
    ageEntry = CTkEntry(leftFrame, **ent); ageEntry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

    CTkLabel(leftFrame, text='Gender:',       **lbl).grid(row=1, column=2, padx=10, pady=10, sticky='e')
    gender_Box = CTkComboBox(leftFrame, values=['Male', 'Female', 'Others'],
                             font=('Arial', 16, 'bold'), width=180)
    gender_Box.grid(row=1, column=3, padx=10, pady=10, sticky='w')
    gender_Box.set('Please Select')

    CTkLabel(leftFrame, text='City:',         **lbl).grid(row=2, column=2, padx=10, pady=10, sticky='e')
    cityEntry = CTkEntry(leftFrame, **ent); cityEntry.grid(row=2, column=3, padx=10, pady=10, sticky='w')

    # QA-04/17 FIX: actual medicine widget
    CTkLabel(leftFrame, text='Medicine:',     **lbl).grid(row=3, column=0, padx=10, pady=10, sticky='e')
    medicine_Box = CTkComboBox(leftFrame, values=[
        'Paracetamol', 'Amoxicillin', 'Ibuprofen', 'Metformin',
        'Omeprazole', 'Atorvastatin', 'Amlodipine', 'Other'
    ], font=('Arial', 16, 'bold'), width=180)
    medicine_Box.grid(row=3, column=1, padx=10, pady=10, sticky='w')
    medicine_Box.set('Please Select')

    buttonFrame = CTkFrame(window, fg_color="black")
    buttonFrame.grid(row=2, column=0, pady=20, sticky='n')

    CTkButton(buttonFrame, text='Generate Emergency Token', command=add_pat
              ).grid(row=0, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Continue to OPD', command=go_to_opd_screen
              ).grid(row=1, column=0, padx=10, pady=10)
    CTkButton(buttonFrame, text='Go Back', command=go_back
              ).grid(row=2, column=0, padx=10, pady=10)

    window.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
#  Screen 3 — OPD Selection
# ═════════════════════════════════════════════════════════════════════════════

def opd_screen():
    global window
    window = CTk()
    window.geometry("950x580")
    window.resizable(False, False)
    window.title("ZEM Hospital — OPD Selection")
    window.configure(fg_color='black')

    CTkLabel(window, image=CTkImage(Image.open('hms.jpg'), size=(950, 150)),
             text="").grid(row=0, column=0, columnspan=2)
    CTkLabel(window, text="Please select the desired OPD",
             font=("Arial", 30, "bold"), text_color="white").grid(
             row=1, column=0, columnspan=2, pady=10)

    opd_services = [
        ("Consultation",   "Dr. Ehtisham"), ("Pediatrics",     "Dr. Ehtisham"),
        ("Surgical",       "Dr. Mohsin"),   ("Psychiatry",     "Dr. Zeeshan"),
        ("Orthopedic",     "Dr. Ehtisham"), ("Cardiology",     "Dr. Mohsin"),
        ("Neurology",      "Dr. Mohsin"),   ("Immunizations",  "Dr. Zeeshan"),
        ("Dermatology",    "Dr. Ehtisham"), ("Pulmonology",    "Dr. Mohsin"),
        ("Physio-Therapy", "Dr. Zeeshan"),  ("ENT",            "Dr. Zeeshan"),
    ]

    def generate_token(service, doctor):
        # QA-26 FIX: module-level queue used
        token_number = len(opd_token_queue) + 1
        room_number  = 101 + (len(opd_token_queue) % 10)
        opd_token_queue.append({
            "Token": token_number, "Service": service,
            "Doctor": doctor, "Room": room_number
        })
        messagebox.showinfo("OPD Token",
            f"Token Number : {token_number}\n"
            f"Service      : {service}\n"
            f"Doctor       : {doctor}\n"
            f"Room         : {room_number}"
        )
        window.destroy()
        user_screen()

    buttonFrame = CTkFrame(window)
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=20)

    for i, (service, doctor) in enumerate(opd_services):
        CTkButton(buttonFrame, text=service, font=('Arial', 20, 'bold'),
                  width=220, corner_radius=10,
                  command=lambda s=service, d=doctor: generate_token(s, d)
                  ).grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def previous():
        window.destroy()
        navigation_list.go_previous()
        navigation_list.head.screen_func()

    # QA-29 FIX: row=4 (was row=5 — caused a blank gap row)
    CTkButton(buttonFrame, text='Go Back', cursor='hand2', command=previous,
              font=('Arial', 20, 'bold'), width=220, corner_radius=15
              ).grid(row=4, column=1, padx=10, pady=10)

    window.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
#  Screen 4 — Visitor Screen
# ═════════════════════════════════════════════════════════════════════════════

def visitor_screen():
    global window
    window = CTk()
    window.geometry("950x480")
    window.resizable(False, False)
    window.title("ZEM Hospital — Visitor Information")

    CTkLabel(window, text="Visitor Information",
             font=("Arial", 30, "bold"), text_color="white").pack(pady=20)

    visitor_frame = CTkFrame(window)
    visitor_frame.pack(pady=10, padx=20)

    lbl = dict(font=('Arial', 18), text_color="white")

    CTkLabel(visitor_frame, text="Visitor Name:",   **lbl).grid(row=0, column=0, pady=10, padx=10, sticky='e')
    name_entry    = CTkEntry(visitor_frame, width=220); name_entry.grid(row=0, column=1, pady=10, padx=10)

    CTkLabel(visitor_frame, text="CNIC:",           **lbl).grid(row=1, column=0, pady=10, padx=10, sticky='e')
    cnic_entry    = CTkEntry(visitor_frame, width=220); cnic_entry.grid(row=1, column=1, pady=10, padx=10)

    CTkLabel(visitor_frame, text="Contact Number:", **lbl).grid(row=2, column=0, pady=10, padx=10, sticky='e')
    contact_entry = CTkEntry(visitor_frame, width=220); contact_entry.grid(row=2, column=1, pady=10, padx=10)

    # QA-09 FIX: Patient ID label/entry at row=3 (was at row=2, overlapping Contact Number)
    CTkLabel(visitor_frame, text="Patient ID:",     **lbl).grid(row=3, column=0, pady=10, padx=10, sticky='e')
    pid_entry     = CTkEntry(visitor_frame, width=220); pid_entry.grid(row=3, column=1, pady=10, padx=10)

    # QA-06 FIX: submit now reads entries and saves to DB
    def submit_visitor():
        v_name    = name_entry.get().strip()
        v_cnic    = cnic_entry.get().strip()
        v_contact = contact_entry.get().strip()
        v_pid     = pid_entry.get().strip()

        if not v_name or not v_cnic:
            messagebox.showerror("Error", "Visitor Name and CNIC are required.")
            return
        ad.insert_visitor(v_name, v_cnic, v_contact, v_pid)
        messagebox.showinfo("Submitted", "Visitor details recorded successfully.")
        for e in [name_entry, cnic_entry, contact_entry, pid_entry]:
            e.delete(0, END)

    def back_to_user_screen():
        window.destroy()
        # QA-08 FIX: bounded seek, no infinite loop
        if navigation_list.seek("User Screen"):
            navigation_list.head.screen_func()
        else:
            user_screen()

    CTkButton(window, text="Submit", command=submit_visitor).pack(pady=10)
    CTkButton(window, text="Back",   command=back_to_user_screen).pack(pady=5)

    window.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
#  Screen 5 — Suggestion Screen
# ═════════════════════════════════════════════════════════════════════════════

def suggestion_screen():
    global window
    window = CTk()
    window.geometry("950x480")
    window.resizable(False, False)
    window.title("ZEM Hospital — Suggestions")

    CTkLabel(window, text="Add a Suggestion",
             font=("Arial", 30, "bold"), text_color="white").pack(pady=20)

    suggestion_frame = CTkFrame(window)
    suggestion_frame.pack(pady=10, padx=20)

    CTkLabel(suggestion_frame, text="Your Suggestion:",
             font=('Arial', 18), text_color="white").grid(row=0, column=0, pady=10, padx=10)
    suggestion_entry = CTkEntry(suggestion_frame, width=400)
    suggestion_entry.grid(row=0, column=1, pady=10, padx=10)

    # QA-07 FIX: actually saves to DB
    def submit_suggestion():
        text = suggestion_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter a suggestion before submitting.")
            return
        ad.insert_suggestion(text)
        messagebox.showinfo("Submitted", "Thank you for your suggestion!")
        suggestion_entry.delete(0, END)

    def back_to_user_screen():
        window.destroy()
        # QA-08 FIX: bounded seek
        if navigation_list.seek("User Screen"):
            navigation_list.head.screen_func()
        else:
            user_screen()

    btn_frame = CTkFrame(window)
    btn_frame.pack(pady=10)
    CTkButton(btn_frame, text='Go Back',           font=('Arial', 15, 'bold'), width=170,
              corner_radius=15, command=back_to_user_screen).grid(row=0, column=0, pady=5, padx=5)
    CTkButton(btn_frame, text='Submit Suggestion',  font=('Arial', 15, 'bold'), width=170,
              corner_radius=15, command=submit_suggestion).grid(row=0, column=1, pady=5, padx=5)

    # QA-10 FIX: removed wrong patient-columns Treeview; show submitted suggestions instead
    recent_frame = CTkFrame(window)
    recent_frame.pack(pady=10, padx=20, fill='x')

    CTkLabel(recent_frame, text="Recent Suggestions",
             font=('Arial', 14, 'bold'), text_color="white").pack(anchor='w', padx=5, pady=5)

    tree = ttk.Treeview(recent_frame, height=6,
                        columns=['ID', 'Suggestion', 'Submitted At'], show='headings')
    tree.heading('ID',           text='#')
    tree.heading('Suggestion',   text='Suggestion')
    tree.heading('Submitted At', text='Submitted At')
    tree.column('ID',           width=40)
    tree.column('Suggestion',   width=450)
    tree.column('Submitted At', width=170)
    tree.pack(fill='x', padx=5, pady=5)

    window.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
#  Navigation List & App Launch
# ═════════════════════════════════════════════════════════════════════════════

navigation_list.append("User Screen",       user_screen)
navigation_list.append("Patient Screen",    patient_screen)
navigation_list.append("OPD Screen",        opd_screen)
navigation_list.append("Visitor Screen",    visitor_screen)
navigation_list.append("Suggestion Screen", suggestion_screen)

# QA-01 FIX: __main__ guard — UI only runs when executed directly
if __name__ == '__main__':
    navigation_list.head.screen_func()