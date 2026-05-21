import getpass
import authenticator
from controllers import database_controller
from classes.account import Account
from classes.student import Student
import controllers.student_controller as student_controller

db_controller = database_controller.DatabaseController()

# ---------- Register ----------

def register():
    print("Student Sign Up")

    email = input("Email: ")
    password = getpass.getpass("Password: ")

    if not authenticator.validate_email(email) or not authenticator.validate_password(password):
        print("Incorrect email or password format")
        return

    print("email and password formats acceptable")

    if db_controller.check_dup_email(email):
        name_part = email.split('@')[0]
        name = ' '.join(part.capitalize() for part in name_part.split('.'))
        print(f"Student {name} already exists")
        return

    name = input("Name: ")

    hashed_password = authenticator.hash_password(password)
    db_controller.create_account(Account(email=email, password=hashed_password))

    new_student = Student(email=email, name=name)
    while db_controller.check_dup_id(new_student.id):
        new_student.regenerate_id()

    print(f"Enrolling Student {name}")

    db_controller.create_student(new_student)


# ---------- Login ----------

def login():
    print("Student Sign In")

    email = input("Email: ")
    password = getpass.getpass("Password: ")

    if not authenticator.validate_email(email) or not authenticator.validate_password(password):
        print("Incorrect email or password format")
        return

    print("email and password formats acceptable")

    if authenticator.authenticate(email, password):
        student_controller.student_menu(db_controller.get_student(email))
    else:
        print("Student does not exist")


# ----------- Menu -----------

def login_menu():
    while True:
        choice = input("\nStudent System (l/r/x): ")

        if choice == "l":
            login()

        elif choice == "r":
            register()

        elif choice == "x":
            break

        else:
            print("Invalid option")