import json
import os
from dataclasses import asdict
from typing import Any
from classes.student import Student
from classes.subject import Subject

class Database:
    _instance = None
    _DATA_FILE = "students.data"
    _data = None
    _BLANK_DATA = {
        "accounts": [],
        "students": []
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_data(self):
        if self._data is None:
            self.init_data()
            
        return self._data

    def init_data(self):
        if not os.path.exists(self._DATA_FILE):
            self.reset_data()
            return
    
        with open(self._DATA_FILE, 'r') as f:
            self._data = json.load(f)

    def update(self):
        with open(self._DATA_FILE, "w") as f:
            json.dump(self._data, f, indent = 4)

    def reset_data(self):
        self._data = self._BLANK_DATA
        self.update()


class DatabaseController:
    _instance = None
    __db: Any = None
    __data: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.__db = Database()
            cls.__data = cls.__db.get_data()
        return cls._instance
    
    def get_password(self, email):
        for account in self.__data["accounts"]:
            if account["email"] == email:
                return account["password"]
        return None
    
    def check_dup_email(self, email):
        for account in self.__data["accounts"]:
            if account["email"] == email:
                return True
        return False
    
    def check_dup_id(self, id):
        for student in self.__data["students"]:
            if student["id"] == id:
                return True
        return False
    
    def create_account(self, account):
        self.__data["accounts"].append(account._asdict())
        self.__db.update()

    def create_student(self, student):
        self.__data["students"].append(asdict(student))
        self.__db.update()

    def get_student(self, email):
        for student in self.__data["students"]:
            if student["email"] == email:
                subjects = [Subject(**s) for s in student["subjects"]]
                return Student(email=student["email"], name=student["name"], id=student["id"], mark=student["mark"], subjects=subjects)
        return None
    
    #GET ALL STUDENTS (for admin)
    def get_students(self):
        students = []
        for student in self.__data["students"]:
            subjects = [Subject(**s) for s in student["subjects"]]
            students.append(Student(email=student["email"], name=student["name"], id=student["id"], mark=student["mark"], subjects=subjects))
        return students
    
    def remove_student(self, id):
        email = None
        for student in self.__data["students"]:
            if student["id"] == id:
                email = student["email"]
                self.__data["students"].remove(student)
                break
        
        if email:
            self.__data["accounts"] = [acc for acc in self.__data["accounts"] if acc["email"] != email]
            self.__db.update()
    
    def update_subjects(self, student):
        for s in self.__data["students"]:
            if s["id"] == student.id:
                s["subjects"] = [asdict(sub) for sub in student.subjects]
                s["mark"] = student.mark
                self.__db.update()
                return
            
    def update_password(self, email, new_password):
        for account in self.__data["accounts"]:
            if account["email"] == email:
                account["password"] = new_password
                self.__db.update()
                return


