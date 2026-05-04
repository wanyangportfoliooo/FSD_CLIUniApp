import controllers.login_controller as login_controller
import controllers.admin_controller as admin_controller

def uni_menu():
    while True:
        print("\nUniversity System:")
        print("(A)dmin  ")
        print("(S)tudent")
        print("(X)exit")

        choice = input("Choice: ")

        if choice == "A":
            admin_controller.admin_menu()
            return

        elif choice == "S":
            login_controller.login_menu()

        elif choice == "X":
            print("Thank you")
            break

        else:
            print("Invalid option")