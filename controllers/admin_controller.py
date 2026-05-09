from controllers import database_controller

_INDENT = "        "

db_controller = database_controller.DatabaseController()


def __show_students():
    students = db_controller.get_students()
    print(f"{_INDENT}Student List")
    if not students:
        print(f"{_INDENT}< Nothing to Display >")
        return
    for student in students:
        print(f"{_INDENT}{student.name} :: {student.id} --> Email: {student.email}")


def __group_students():
    students = db_controller.get_students()
    print(f"{_INDENT}Grade Grouping")
    if not students:
        print(f"{_INDENT}< Nothing to Display >")
        return

    groups = {}
    for student in students:
        grade = student.get_grade()
        if grade not in groups:
            groups[grade] = []
        groups[grade].append(student)

    for grade in ["HD", "D", "C", "P", "F"]:
        if grade in groups:
            entries = [
                f"{s.name} :: {s.id} --> GRADE:{grade:>3} - MARK: {s.mark:.2f}"
                for s in groups[grade]
            ]
            print(f"{_INDENT}{grade:<2} --> [{', '.join(entries)}]")


def __partition_students():
    students = db_controller.get_students()
    print(f"{_INDENT}PASS/FAIL Partition")

    pass_list = []
    fail_list = []

    for student in students:
        grade = student.get_grade()
        entry = f"{student.name} :: {student.id} --> GRADE:{grade:>3} - MARK: {student.mark:.2f}"
        if student.mark >= 50:
            pass_list.append(entry)
        else:
            fail_list.append(entry)

    print(f"{_INDENT}FAIL --> [{', '.join(fail_list)}]")
    print(f"{_INDENT}PASS --> [{', '.join(pass_list)}]")


def __remove_student():
    student_id = input(f"{_INDENT}Remove by ID: ")

    students = db_controller.get_students()
    found = any(s.id == student_id for s in students)

    if not found:
        print(f"{_INDENT}Student {student_id} does not exist")
        return

    db_controller.remove_student(student_id)
    print(f"{_INDENT}Removing Student {student_id} Account")


def __clear_database():
    print(f"{_INDENT}Clearing students database")
    confirm = input(f"{_INDENT}Are you sure you want to clear the database (Y)ES/(N)O: ")
    if confirm.upper() == "Y":
        db_controller.clear_database()
        print(f"{_INDENT}Students data cleared")


def admin_menu():
    while True:
        choice = input(f"\n{_INDENT}Admin System (c/g/p/r/s/x): ")

        if choice == "c":
            __clear_database()
        elif choice == "g":
            __group_students()
        elif choice == "p":
            __partition_students()
        elif choice == "r":
            __remove_student()
        elif choice == "s":
            __show_students()
        elif choice == "x":
            break
