import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re

class Address:
    def __init__(self, house, city, pincode, state):
        self.house = house
        self.city = city
        self.pincode = pincode
        self.state = state

class Person:
    number_of_people = 0
    def __init__(self, id, pwd, type):
        self.status = 0
        self.user_id = id
        self.password = pwd
        self.type = type
        self.name = ''
        self.dob = ''
        self.gender = -1
        self.department = ''
        self.phone = 0
        Person.number_of_people += 1
        
    def set_password(self, password):
        self.password = password
    
    def change_name(self, name):
        self.name = name
    
    def change_phone(self, phone):
        self.phone = phone

    def change_dob(self, dob):
        self.dob = dob
    def set_details(self, name, dob, gender, department, phone):
        self.status = 1
        self.name = name
        self.dob = dob
        self.gender = gender
        self.department = department
        self.phone = phone

    def self_deactivate(self):
        self.status = -1

class Teacher(Person):
    number_of_teachers = 0

    def __init__(self, id, pwd, type):
        self.warden = ''
        self.post = ''
        Teacher.number_of_teachers += 1
        super().__init__(id, pwd, type)

    def change_warden(self, warden):
        self.wardern = warden
    
    def change_post(self, post):
        self.post = post

    def set_details(self, name, dob, gender, department, phone, warden, post):
        self.warden = warden
        self.post  = post
        return super().set_details(name, dob, gender, department, phone)
    
class Student(Person):
    number_of_students = 0

    def __init__(self, id, pwd, type):
        self.year_of_admission = 0
        self.cgpa = 0
        self.hall = ''
        self.address = Address(0, '', 0, '')
        Student.number_of_students += 1
        super().__init__(id, pwd, type)

    def set_details(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address):
        self.year_of_admission = year_of_admission
        self.cgpa = cgpa
        self.hall = hall
        self.address = address
        return super().set_details(name, dob, gender, department, phone)
    
    def change_cgpa(self, cgpa):
        self.cgpa = cgpa

    def change_hall(self, hall):
        self.hall = hall

    def change_address(self, address):
        self.address = address

class UG(Student):
    number_of_ug = 0
    
    def __init__(self, id, pwd, type):
        UG.number_of_ug += 1
        self.eaa = ''
        super().__init__(id, pwd, type)
    
    def set_details(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address, eaa):
        self.eaa = eaa
        return super().set_details(name, dob, gender, department, phone, year_of_admission, cgpa, hall, address)
    
    def change_eaa(self, eaa):
        self.eaa = eaa

class PG(Student):
    number_of_pg = 0

    def __init__(self, id, pwd, type):
        self.research_area = ''
        PG.number_of_pg += 1
        super().__init__(id, pwd, type)
    
    def set_details(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address, research_area):
        self.research_area = research_area
        return super().set_details(name, dob, gender, department, phone, year_of_admission, cgpa, hall, address)
    

class User:
    def __init__(self, master):
        self.master  = master
        self.master.title("User System")
        self.user_id = tk.StringVar()
        self.password = tk.StringVar()
        self.user_type = tk.StringVar()

        tk.Label(master, text =  "User ID:").pack()
        tk.Entry(master, textvariable = self.user_id).pack()

        tk.Label(master, text = "Password:").pack()
        tk.Entry(master, textvariable = self.password, show  = "*").pack()

        tk.Label(master, text = "User Type:").pack()
        # tk.Entry(master, textvariable = self.user_type).pack()
        user_types = ["Teacher", "UG Student", "PG Student"]
        for user_type in user_types:
            ttk.Radiobutton(master, text = user_type, variable = self.user_type, value = user_type).pack()

        tk.Button(master, text = "Register", command = self.register_user).pack()
        tk.Button(master, text = "Login", command = self.login_user).pack()
        self.failed_login_attempts = {}

    def register_user(self):
        user_id = self.user_id.get()
        password = self.password.get()
        user_type = self.user_type.get()

        if self.check_user_exists(user_id):
            messagebox.showerror("Registration Failed", "User ID already exits. Choose a different one.")
        elif not self.validate_password(password):
            messagebox.showerror("Registration Failed", '''Invalid Password.\n
                                 a) It should be within 8 - 12 characters long.\n
                                 b) It should contain at least one upper case, one digit and one lower case.\n
                                 c) It should contain at least one or more special characters from the list [! @ # % & *]\n
                                 d) No blank space will be allowed.''')
        else:
            if user_type == "Teacher":
                new_user = Teacher(user_id, password, user_type)
            elif user_type == "UG Student":
                new_user = UG(user_id, password, user_type)
            elif user_type == "PG Student":
                new_user = PG(user_id, password, user_type)
            else:
                messagebox.showerror("Registration Failed", "Invalid User type")
            self.save_user_to_csv(new_user)
            messagebox.showinfo("Registration Successful", "User registered successfully!")
    
    def validate_password(self, password):
        if not (8 <= len(password) <= 12):
            return False
        if not re.search(r'[A-z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%&*]', password):
            return False
        if ' ' in password:
            return False
        return True
    
    def check_user_exists(self, user_id):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return True
        return False
    
    def save_user_to_csv(self, user):
        with open("user_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if user.type == 'Teacher':
                writer.writerow([user.user_id, user.password, user.type, user.status, user.name, user.dob,
                                  user.gender, user.department, user.phone, user.warden, user.post])
            elif user.type == "UG Student":
                writer.writerow([user.user_id, user.password, user.type, user.status, 
                                user.name, user.dob, user.gender, user.department, user.phone,
                                user.year_of_admission, user.cgpa, user.hall, user.address.house,
                                user.address.city, user.address.pincode, user.address.state, user.eaa])
            elif user.type == "PG Student":
                writer.writerow([user.user_id, user.password, user.type, user.status, 
                                user.name, user.dob, user.gender, user.department, user.phone,
                                user.year_of_admission, user.cgpa, user.hall, user.address.house,
                                user.address.city, user.address.pincode, user.address.state, user.research_area])
            else:
                messagebox.showerror("Error while Saving", "Invalid User type")
   
    def check_credential_match(self, user_id, password, user_type):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id  and row[1] == password and row[2] == user_type:
                    return True
        return False

    def login_user(self):
        user_id = self.user_id.get()
        password =  self.password.get()
        user_type = self.user_type.get()

        if not self.check_user_exists(user_id):
            messagebox.showerror("Login Failed", "User not found")
        else:
            attempts  = self.failed_login_attempts.get(user_id, 0)

            if(attempts >= 3):
                self.deactivate_user_account(user_id)
                messagebox.showinfo("Login Failed", "Account deactivated")
            elif self.check_credential_match(user_id, password, user_type):
                self.failed_login_attempts[user_id] = 0
                messagebox.showinfo("Login successful", "Welcome!")
                self.open_second_window(user_id)
            else:
                self.failed_login_attempts[user_id] = attempts + 1
                messagebox.showerror("Login Failed", "Incorrect credentials.")

    def deactivate_user_account(self, user_id):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = -1 
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
    
    def open_second_window(self, user_id):
        second_window = tk.Toplevel(self.master)
        status = self.get_user_status(user_id)
        user_type = self.user_type.get()

        if user_type == "Teacher":
            if status == 0:
                self.create_teacher_profile(second_window, user_id)
            elif status == 1:
                self.update_teacher_profile(second_window, user_id)
        elif user_type == "UG Student":
            if status == 0:
                self.create_ug_profile(second_window, user_id)
            elif status == 1:
                self.update_ug_profile(second_window, user_id)
        elif user_type == "PG Student":
            if status == 0:
                self.create_pg_profile(second_window, user_id)
            elif status == 1:
                self.update_pg_profile(second_window, user_id)
        else:
            messagebox.showerror("Error", "Invalid user type")
        deregister_button = tk.Button(second_window, text = "Deregister", command = lambda: self.deregister_user(user_id, second_window))
        deregister_button.pack()
    
    def deregister_user(self, user_id, window):
        confirmation = messagebox.askyesno("Deregister User", "Are you sure you want to deregister your account?")
        if confirmation:
            with open("user_data.csv", "r+", newline="") as file:
                lines = list(csv.reader(file))
                new_lines = [line for line in lines if line[0] != user_id]
                file.seek(0)
                file.truncate()
                writer = csv.write(file)
                writer.writerows(new_lines)
            messagebox.showinfo("Deregistration Successful", "User deregistered successfully!")
            window.destroy()
        else:
            messagebox.showinfo("Deregistation Canceled", "Deregistration process canceled" )

    def get_user_status(self, user_id):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return int(row[3])
        return -1
    
    def create_teacher_profile(self, window, user_id):
        tk.Label(window, text = "Teacher Profile Creation").pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()
        tk.Label(window, text = "Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()
        tk.Label(window, text = "Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()
        tk.Label(window, text = "Warden:").pack()
        warden_entry = tk.Entry(window)
        warden_entry.pack()
        tk.Label(window, text = "Post:").pack()
        post_entry = tk.Entry(window)
        post_entry.pack()
        tk.Button(window, text = "Save", command = lambda: self.save_teacher_profile(window, user_id, name_entry.get(), dob_entry.get(), gender_entry.get(), department_entry.get(), phone_entry.get(), warden_entry.get(), post_entry.get())).pack()
    
    def update_teacher_profile(self, window, user_id):
        tk.Label(window, text = "Update Teacher Profile").pack()
        tk.Label(window, text = "Password:").pack()
        password_entry = tk.Entry(window, show="*")
        password_entry.pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Button(window, text = "Update", command = lambda: self.update_teacher_details(window, user_id, password_entry.get(), name_entry.get(), phone_entry.get())).pack()
    def save_teacher_profile(self, window, user_id, name, dob, gender, department, phone, warden, post):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][9] = warden
                    lines[i][10] = post
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Creation Successful", "Teacher profile created successfully!")
        window.destroy()
    def update_teacher_details(self, window, user_id, password, name, phone):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][1] = password
                    lines[i][4] = name
                    lines[i][8] = phone
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Update Successful", "Teacher profile updated successfully!")
        window.destroy()

    def create_ug_profile(self, window, user_id):
        tk.Label(window, text = "UG Student Profile Creation").pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()
        tk.Label(window, text = "Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()
        tk.Label(window, text = "Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()
        tk.Label(window, text = "Year of Admission:").pack()
        year_entry = tk.Entry(window)
        year_entry.pack()
        tk.Label(window, text = "CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()
        tk.Label(window, text = "Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()
        tk.Label(window, text = "Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()
        tk.Label(window, text = "EAA:").pack()
        eaa_entry = tk.Entry(window)
        eaa_entry.pack()
        tk.Button(window, text = "Save", command = lambda: self.save_ug_profile(window, user_id, name_entry.get(), dob_entry.get(), gender_entry.get(), department_entry.get(), phone_entry.get(), year_entry.get(), cgpa_entry.get(), hall_entry.get(), address_entry.get(), eaa_entry.get())).pack()
   
    def update_ug_profile(self, window, user_id):
        tk.Label(window, text = "Update UG Profile").pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()
        tk.Label(window, text = "CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()
        tk.Label(window, text = "Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()
        tk.Label(window, text = "Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()
        tk.Button(window, text = "Update", command = lambda: self.update_ug_details(window, user_id, name_entry.get(), phone_entry.get(), cgpa_entry.get(), hall_entry.get(), address_entry.get())).pack()

    def save_ug_profile(self, window, user_id, name, dob, gender, department, phone, year, cgpa, hall, address , eaa):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][11] = year
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][15] = eaa
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Creation Successful", "UG student profile created successfully!")
        window.destroy()
    
    def update_ug_details(self, window, user_id, name, phone, cgpa, hall, address):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][4] = name
                    lines[i][8] = phone
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Update Successful", "UG student profile updated successfully!")
        window.destroy()
    
    def create_pg_profile(self, window, user_id):
        tk.Label(window, text = "PG Student Profile Creation").pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()
        tk.Label(window, text = "Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()
        tk.Label(window, text = "Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()
        tk.Label(window, text = "Year of Admission:").pack()
        year_entry = tk.Entry(window)
        year_entry.pack()
        tk.Label(window, text = "CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()
        tk.Label(window, text = "Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()
        tk.Label(window, text = "Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()
        tk.Label(window, text = "Research Area:").pack()
        research_area_entry = tk.Entry(window)
        research_area_entry.pack()
        tk.Button(window, text = "Save", command = lambda: self.save_pg_profile(window, user_id, name_entry.get(), dob_entry.get(), gender_entry.get(), department_entry.get(), phone_entry.get(), year_entry.get(), cgpa_entry.get(), hall_entry.get(), address_entry.get(), research_area_entry.get())).pack()
    def update_pg_profile(self, window, user_id):
        tk.Label(window, text = "Update PG Profile").pack()
        tk.Label(window, text = "Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text = "Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()
        tk.Label(window, text = "CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()
        tk.Label(window, text = "Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()
        tk.Label(window, text = "Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()
        tk.Label(window, text = "Research Area:").pack()
        research_area_entry = tk.Entry(window)
        research_area_entry.pack()
        tk.Button(window, text = "Update", command = lambda: self.update_pg_details(window, user_id, name_entry.get(), phone_entry.get(), cgpa_entry.get(), hall_entry.get(), address_entry.get(), research_area_entry.get())).pack()
    def save_pg_profile(self, window, user_id, name, dob, gender, department, phone, year, cgpa, hall, address, research_area):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][11] = year
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][16] = research_area
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Creation Successful", "PG student profile created successfully!")
        window.destroy()
    def update_pg_details(self, window, user_id, name, phone, cgpa, hall, address, research_area):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))
            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][4] = name
                    lines[i][8] = phone
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][16] = research_area
                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)
        messagebox.showinfo("Profile Update Successful", "PG student profile updated successfully!")
        window.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = User(root)
    root.mainloop()