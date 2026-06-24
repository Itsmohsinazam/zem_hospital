import pymysql
from tkinter import messagebox

def connt_db():
    global mycursor, connt
    try:
        connt = pymysql.connect(host='localhost', user='root', password='1234')
        mycursor = connt.cursor()
        mycursor.execute('CREATE DATABASE IF NOT EXISTS patients_data')
        mycursor.execute('USE patients_data')
        mycursor.execute('CREATE TABLE IF NOT EXISTS data (Id VARCHAR(50), Name VARCHAR(50), Phone VARCHAR(12), Age VARCHAR(50), Gender VARCHAR(50), Medicine VARCHAR(50))')
    except Exception as e:
        messagebox.showerror('Error', f'Something went wrong while connecting to the database: {e}')

def insert(id, name, phone, age, gender, medicine):
    try:
        query = 'INSERT INTO data (Id, Name, Phone, Age, Gender, Medicine) VALUES (%s, %s, %s, %s, %s, %s)'
        mycursor.execute(query, (id, name, phone, age, gender, medicine))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert data: {e}")

def id_exists(id):
    mycursor.execute('SELECT COUNT(*) FROM data WHERE Id=%s', (id,))
    result = mycursor.fetchone()
    return result[0] > 0

def fetch_pat_data():
    try:
        mycursor.execute('SELECT * FROM data ORDER BY Id ASC')
        return mycursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return []

def update_db(id, new_name, new_phone, new_age, new_gender, new_medicine):
    try:
        query = 'UPDATE data SET Name=%s, Phone=%s, Age=%s, Gender=%s, Medicine=%s WHERE Id=%s'
        mycursor.execute(query, (new_name, new_phone, new_age, new_gender, new_medicine, id))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update data: {e}")

def del_db(id):
    try:
        mycursor.execute('DELETE FROM data WHERE Id=%s', (id,))
        connt.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete data: {e}")
        
def search_db(option, value):
        mycursor.execute(f'SELECT * FROM data  WHERE {option}=%s', value)
        result=mycursor.fetchall()
        return result

connt_db()