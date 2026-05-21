import getpass
from controllers import database_controller
import authenticator

db_controller = database_controller.DatabaseController()
_MAX_SUBJECTS = 4

def __change_password(student):
    print("Updating Password")
    new_password = getpass.getpass("New Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")

    while new_password != confirm_password:
        print("Password does not match - try again")
        confirm_password = getpass.getpass("Confirm Password: ")

    new_password = authenticator.hash_password(new_password)
    db_controller.update_password(student.email, new_password)

def __remove_subject(student):
    if not student.subjects:
        print("No subjects to remove.")
        return

    sid = int(input("Remove Subject by ID: "))

    if student.remove_subject(sid):
        db_controller.update_subjects(student)
        print(f"Droping Subject-{sid}")
        print(f"You are now enrolled in {len(student.subjects)} out of {_MAX_SUBJECTS} subjects")
    else:
        print(f"Subject {sid} not found")

def enrol_subject(student):
    if len(student.subjects) >= _MAX_SUBJECTS:
        print("Students are allowed to enrol in 4 subjects only")
        return

    new_subject = student.enrol_subject()
    db_controller.update_subjects(student)

    print(f"Enrolling in Subject-{new_subject.id}")
    print(f"You are now enrolled in {len(student.subjects)} out of {_MAX_SUBJECTS} subjects")

def show_subjects(student):
    print(f"Showing {len(student.subjects)} subjects")

    for subject in student.subjects:
        print(f"[ Subject::{subject.id:03d} -- mark = {subject.mark} -- grade = {subject.grade:>4} ]")

def student_menu(student):
    while True:
        choice = input("\nStudent Course Menu (c/e/r/s/x): ").lower()

        if choice == "c":
            __change_password(student)
        elif choice == "e":
            enrol_subject(student)
        elif choice == "r":
            __remove_subject(student)
        elif choice == "s":
            show_subjects(student)
        elif choice == "x":
            break
        else:
            print("Invalid option.")
