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
        self.wardern = ''
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
        super().init__(id, pwd, type)
    
    def set_details(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address, research_area):
        self.research_area = research_area
        return super().set_details(name, dob, gender, department, phone, year_of_admission, cgpa, hall, address)
    

