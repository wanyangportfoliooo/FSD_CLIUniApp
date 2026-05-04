import getpass
import authenticator
from controllers import database_controller
from classes.account import Account
from classes.student import Student
import controllers.student_controller as student_controller

db_controller = database_controller.DatabaseController()

# ---------- Register ----------

def register():

    email = input("Enter email: ")

    print("Password must start with uppercase, contain 5 letters and end with 3+ digits.")
    password = getpass.getpass("Enter password: ")

    if not authenticator.validate_email(email):
        print("Invalid email format.")
        return

    if not authenticator.validate_password(password):
        print("Invalid password format.")
        return

    if db_controller.check_dup_email(email):
        print("Student already exists.")
        return
    
    print("Email and password format valid. Creating account...")

    name = input("Enter your name: ")

    hashed_password = authenticator.hash_password(password)
    db_controller.create_account(Account(email=email, password=hashed_password))

    new_student = Student(email=email, name=name)
    while db_controller.check_dup_id(new_student.id):
        new_student.regenerate_id()

    print("Enrolling student " + name)
    
    db_controller.create_student(new_student)
    print("Registration successful.")


# ---------- Login ----------

def login():

    email = input("Email: ")
    password = getpass.getpass("Password: ")

    if authenticator.authenticate(email, password):
        print("Login successful.")

        student_controller.student_menu(db_controller.get_student(email))
    else:
        print("Invalid credentials.")



# ----------- Menu -----------

def login_menu():
    while True:
        print("\nStudent Menu:")
        print("(l)ogin")
        print("(r)egister")
        print("(x)exit")

        choice = input("Choice: ")

        if choice == "l":
            login()

        elif choice == "r":
            register()

        elif choice == "x":
            print("Exiting...")
            break

        else:
            print("Invalid option")