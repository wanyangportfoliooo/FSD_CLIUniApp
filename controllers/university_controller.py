import controllers.login_controller as login_controller
import controllers.admin_controller as admin_controller

def uni_menu():
    while True:
        choice = input("\nUniversity System: (A)dmin, (S)tudent, or X : ")

        if choice == "A":
            admin_controller.admin_menu()

        elif choice == "S":
            login_controller.login_menu()

        elif choice == "X":
            print("Thank You")
            break

        else:
            print("Invalid option")