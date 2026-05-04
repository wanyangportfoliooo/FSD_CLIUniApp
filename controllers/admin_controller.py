def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("(c) clear database")
        print("(g) group students by grade")
        print("(p) partition students by PASS/FAIL")
        print("(r) remove student")
        print("(s) show students")
        print("(x) exit")

        choice = input("Choice: ")

        if choice == "c":
            print("clear database functionality not implemented yet.")

        elif choice == "g":
            print("group student functionality not implemented yet.")
        
        elif choice == "p":
            print("partition students functionality not implemented yet.")

        elif choice == "r":
            print("remove student functionality not implemented yet.")

        elif choice == "s":
            print("show students functionality not implemented yet.")

        elif choice == "x":
            break

        else:
            print("Invalid option")