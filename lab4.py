import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Ініціалізація БД
conn = sqlite3.connect('admissions.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, date_of_birth TEXT, 
                 high_school TEXT, exam_score INTEGER)''')
conn.commit()

# Функції для додавання, редагування, видалення, пошуку та виведення анкет
def add_application():
    name = entry_name.get().strip()
    address = entry_address.get().strip()
    dob = entry_dob.get().strip()
    high_school = entry_high_school.get().strip()
    exam_score = entry_exam_score.get().strip()

    if not name or not address or not dob or not high_school or not exam_score:
        messagebox.showerror("Помилка", "Всі поля повинні бути заповнені!")
        return

    try:
        cursor.execute("INSERT INTO applications (name, address, date_of_birth, high_school, exam_score) VALUES (?, ?, ?, ?, ?)",
                       (name, address, dob, high_school, exam_score))
        conn.commit()
        messagebox.showinfo("Успіх", "Анкета додана!")
        clear_entries()
    except sqlite3.IntegrityError:
        messagebox.showerror("Помилка", "Помилка при додаванні анкети!")

def edit_application():
    name = entry_name.get().strip()
    address = entry_address.get().strip()
    dob = entry_dob.get().strip()
    high_school = entry_high_school.get().strip()
    exam_score = entry_exam_score.get().strip()

    if not name or not address or not dob or not high_school or not exam_score:
        messagebox.showerror("Помилка", "Всі поля повинні бути заповнені!")
        return

    cursor.execute("SELECT id FROM applications WHERE name=?", (name,))
    if cursor.fetchone() is None:
        messagebox.showerror("Помилка", "Анкета з таким ім'ям не знайдена!")
        return

    cursor.execute("UPDATE applications SET address=?, date_of_birth=?, high_school=?, exam_score=? WHERE name=?",
                   (address, dob, high_school, exam_score, name))
    conn.commit()
    messagebox.showinfo("Успіх", "Анкета оновлена!")
    clear_entries()

def delete_application():
    name = entry_name.get().strip()

    if not name:
        messagebox.showerror("Помилка", "Поле ім'я повинно бути заповнене!")
        return

    cursor.execute("DELETE FROM applications WHERE name=?", (name,))
    if cursor.rowcount == 0:
        messagebox.showerror("Помилка", "Анкета з таким ім'ям не знайдена!")
    else:
        conn.commit()
        messagebox.showinfo("Успіх", "Анкета видалена!")
        clear_entries()

def search_application_by_name():
    name = entry_name.get().strip()

    if not name:
        messagebox.showerror("Помилка", "Поле ім'я повинно бути заповнене!")
        return

    cursor.execute("SELECT * FROM applications WHERE name LIKE ?", ('%' + name + '%',))
    applications = cursor.fetchall()
    output_text.delete(1.0, tk.END)
    if applications:
        for app in applications:
            output_text.insert(tk.END, f"Ім'я: {app[1]}\nАдреса: {app[2]}\nДата народження: {app[3]}\n"
                                       f"Школа: {app[4]}\nБали: {app[5]}\n\n")
    else:
        messagebox.showerror("Помилка", "Анкета не знайдена!")

def display_applications():
    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()
    output_text.delete(1.0, tk.END)
    if applications:
        for app in applications:
            output_text.insert(tk.END, f"Ім'я: {app[1]}\nАдреса: {app[2]}\nДата народження: {app[3]}\n"
                                       f"Школа: {app[4]}\nБали: {app[5]}\n\n")
    else:
        output_text.insert(tk.END, "Немає наявних анкет.")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_high_school.delete(0, tk.END)
    entry_exam_score.delete(0, tk.END)

# Створення GUI
root = tk.Tk()
root.title("Система Приймальної Комісії")

tk.Label(root, text="Ім'я").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, columnspan=2, sticky='ew')

tk.Label(root, text="Адреса").grid(row=1, column=0)
entry_address = tk.Entry(root)
entry_address.grid(row=1, column=1, columnspan=2, sticky='ew')

tk.Label(root, text="Дата народження").grid(row=2, column=0)
entry_dob = tk.Entry(root)
entry_dob.grid(row=2, column=1, columnspan=2, sticky='ew')

tk.Label(root, text="Школа").grid(row=3, column=0)
entry_high_school = tk.Entry(root)
entry_high_school.grid(row=3, column=1, columnspan=2, sticky='ew')

tk.Label(root, text="Бали").grid(row=4, column=0)
entry_exam_score = tk.Entry(root)
entry_exam_score.grid(row=4, column=1, columnspan=2, sticky='ew')

tk.Button(root, text="Додати", command=add_application).grid(row=5, column=0)
tk.Button(root, text="Редагувати", command=edit_application).grid(row=5, column=1)
tk.Button(root, text="Видалити", command=delete_application).grid(row=5, column=2)
tk.Button(root, text="Пошук за ім'ям", command=search_application_by_name).grid(row=6, column=0, columnspan=3, sticky='ew')
tk.Button(root, text="Показати всі анкети", command=display_applications).grid(row=7, column=0, columnspan=3, sticky='ew')

tk.Label(root, text="Наявні анкети:").grid(row=8, column=0, columnspan=3)
output_text = tk.Text(root, height=15, width=50)
output_text.grid(row=9, column=0, columnspan=3)

root.mainloop()
