import pymysql
from tkinter import messagebox

def connt_db():
    global mycursor, connt
    try:
        connt = pymysql.connect(host='localhost', user='root', password='1234')
        mycursor = connt.cursor()
        mycursor.execute('CREATE DATABASE IF NOT EXISTS hms_data')
        mycursor.execute('USE hms_data')
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS pat_data (
                Id INT AUTO_INCREMENT PRIMARY KEY, 
                CNIC VARCHAR(15), 
                Name VARCHAR(50), 
                Phone VARCHAR(12), 
                Age VARCHAR(50), 
                City VARCHAR(50), 
                Gender VARCHAR(50), 
                Medicine VARCHAR(50)
            )
        ''')

        # Create emergency tokens table
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_tokens (
                TokenID INT AUTO_INCREMENT PRIMARY KEY,
                CNIC VARCHAR(15),
                PatientID INT,
                FOREIGN KEY (PatientID) REFERENCES pat_data(Id)
            )
        ''')
    except Exception as e:
        messagebox.showerror('Database Error', str(e))

def insert(cnic, name, phone, age, city, gender, medicine):
    try:
        query = '''
            INSERT INTO pat_data (CNIC, Name, Phone, Age, City, Gender, Medicine) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        mycursor.execute(query, (cnic, name, phone, age, city, gender, medicine))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def insert_token(token_id, cnic, patient_id):
    try:
        query = '''
            INSERT INTO emergency_tokens (TokenID, CNIC, PatientID)
            VALUES (%s, %s, %s)
        '''
        mycursor.execute(query, (token_id, cnic, patient_id))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to insert token data: {str(e)}")


def fetch_pat_data():
    try:
        mycursor.execute('SELECT * FROM pat_data ORDER BY Id ASC')
        return mycursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

# Fetch patient data by CNIC
def fetch_patient_by_cnic(cnic):
    try:
        query = "SELECT * FROM pat_data WHERE CNIC = %s"
        mycursor.execute(query, (cnic,))
        result = mycursor.fetchone()  # Fetch the first matching record
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None


def update_db(id, cnic, name, phone, age, city, gender, medicine):
    try:
        query = '''
            UPDATE pat_data 
            SET CNIC=%s, Name=%s, Phone=%s, Age=%s, City=%s, Gender=%s, Medicine=%s 
            WHERE Id=%s
        '''
        mycursor.execute(query, (cnic, name, phone, age, city, gender, medicine, id))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def del_db(id):
    try:
        mycursor.execute('DELETE FROM pat_data WHERE Id=%s', (id,))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_db(option, value):
    # Map dropdown values to database column names
    column_mapping = {
        "ID": "Id",
        "CNIC": "CNIC",
        "Name": "Name",
        "Phone": "Phone",
        "City": "City"
    }

    # Validate the selected option
    column_name = column_mapping.get(option)
    if not column_name:
        messagebox.showerror("Error", f"Invalid search option: {option}")
        return []

    try:
        # Execute search query
        query = f"SELECT * FROM pat_data WHERE {column_name}=%s"
        mycursor.execute(query, (value,))
        return mycursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"MySQL error: {e}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search data: {e}")
        return []
    
# Initialize the database connection
connt_db()