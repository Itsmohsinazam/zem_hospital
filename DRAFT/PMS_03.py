from tkinter import Tk, Label, RIDGE, Frame, LabelFrame
from tkinter import ttk  # Import ttk for Combobox

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")
        
        # Create the title label
        lbltitle = Label(self.root, 
                         bd=20, 
                         relief=RIDGE, 
                         text="ZEM HOSPITAL MANAGEMENT SYSTEM", 
                         fg="red", 
                         bg="white", 
                         font=("times new roman", 40, "bold"))
        lbltitle.pack(side="top", fill="x")
        
        # ====== DataFrame ======
        DataFrame = Frame(self.root, bd=20, padx=20, relief=RIDGE)
        DataFrame.place(x=0, y=130, width=1530, height=400)

        # Left DataFrame
        DataFrameLeft = LabelFrame(DataFrame, 
                                   bd=10, 
                                   padx=20, 
                                   relief=RIDGE, 
                                   font=("arial", 12, "bold"), 
                                   text="Patient Information")
        DataFrameLeft.place(x=0, y=5, width=980, height=350)
        
        # Right DataFrame
        DataFrameRight = LabelFrame(DataFrame, 
                                    bd=10, 
                                    padx=20, 
                                    relief=RIDGE, 
                                    font=("arial", 12, "bold"), 
                                    text="Prescription")
        DataFrameRight.place(x=990, y=5, width=460, height=350)
        
        # ===Button Frame=====
        ButtonFrame = Frame(self.root, bd=20, padx=20, relief=RIDGE)
        ButtonFrame.place(x=0, y=530, width=1530, height=70)
        
        # ===Details Frame=====
        DetailsFrame = Frame(self.root, bd=20, padx=20, relief=RIDGE)
        DetailsFrame.place(x=0, y=600, width=1530, height=190)

        # ===== DataFrameLeft Widgets ====
        lblNameTablet = Label(DataFrameLeft, text="Names of Tablet", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblNameTablet.grid(row=0, column=0)

        comNametablet = ttk.Combobox(DataFrameLeft, font=("times new roman", 12, "bold"), width=33)
        comNametablet["values"] = ("Nice", "Corona Vaccine", "Acetaminophen", "Adderall", "Amlodipine", "Ativan")
        comNametablet.grid(row=0, column=1)

root = Tk()
ob = Hospital(root)
root.mainloop()
