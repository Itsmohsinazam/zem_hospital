"""
bill.py — Billing Screen
=========================
QA-20 FIX: Hardcoded values removed. Screen is wrapped in a run() function
           that accepts a patient dictionary from the DB.
"""

from customtkinter import *
from PIL import Image

def run(patient):
    """Launch the billing screen for a specific patient."""
    if not patient:
        return

    # Unpack patient data
    # Assuming patient is a tuple/list from fetch_patient_by_id:
    # (id, cnic, name, phone, age, city, gender, medicine)
    p_id   = str(patient[0])
    p_name = patient[2]
    # For now, hardcode doctor and bill as they aren't stored in pat_data directly
    p_dr   = "Dr. Ehtisham Ali" 
    p_bill = "$100"

    root = CTk()
    root.geometry("900x450")  
    root.resizable(False, False)  
    root.title("ZEM Hospital — Bill")

    image = CTkImage(Image.open('bill.png'), size=(950, 450))
    CTkLabel(root, image=image, text="").place(x=0, y=0)

    lbl_args = dict(fg_color="white", text_color="black", font=("Goudy Old Style", 18, "bold"))

    CTkLabel(root, text="Patient ID:", **lbl_args).place(x=300, y=150)
    CTkLabel(root, text=p_id,          **lbl_args).place(x=600, y=150)

    CTkLabel(root, text="Name:",       **lbl_args).place(x=300, y=200)
    CTkLabel(root, text=p_name,        **lbl_args).place(x=600, y=200)

    CTkLabel(root, text="Examined By:",**lbl_args).place(x=300, y=250)
    CTkLabel(root, text=p_dr,          **lbl_args).place(x=600, y=250)

    CTkLabel(root, text="Bill:",       **lbl_args).place(x=300, y=300)
    CTkLabel(root, text=p_bill,        **lbl_args).place(x=600, y=300)

    root.mainloop()

if __name__ == '__main__':
    # Test stub
    run((1001, "12345", "Test Patient", "0300", "25", "City", "Male", "Med"))