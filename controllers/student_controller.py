import getpass
from controllers import database_controller
import authenticator

db_controller = database_controller.DatabaseController()
_MAX_SUBJECTS = 4

def __change_password(student):
    new_password = getpass.getpass("Enter new password: ")
    confirm_password = getpass.getpass("Confirm new password: ")

    while new_password != confirm_password:
        print("Passwords do not match. Try again.")
        confirm_password = getpass.getpass("Confirm new password: ")

    new_password = authenticator.hash_password(new_password)

    db_controller.update_password(student.email, new_password)
    print("Password updated.")

def __remove_subject(student):
    if not student.subjects:
        print("No subjects to remove.")
        return

    sid = int(input("Enter subject ID to remove: "))

    student.remove_subject(sid)
    db_controller.update_subjects(student)

def enrol_subject(student):
    if len(student.subjects) >= _MAX_SUBJECTS:
        print("Cannot enrol in more than 4 subjects.")
        return

    new_subject = student.enrol_subject()
    db_controller.update_subjects(student)

    print("Subject enrolled successfully.")
    print(f"You are enrolled in subject {new_subject.id:03d}")

    print(
        f"You are enrolled in {len(student.subjects)} out of {_MAX_SUBJECTS} subjects.")
    
def show_subjects(student):
    if not student.subjects:
        print("No subjects enrolled.")
        return
    
    print("\nEnrolled Subjects:")
    print(f"Showing {len(student.subjects)} subjects")
    
    for subject in student.subjects:
        print(f"Subject ID: {subject.id:03d}, Mark: {subject.mark}, Grade: {subject.grade}")
        

def student_menu(student):
    while True:
        print("\nStudent Course Menu")
        print("(c) change password")
        print("(e) enrol subject")
        print("(r) remove subject")
        print("(s) show subjects")
        print("(x) exit")

        choice = input("Enter option: ").lower()

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
