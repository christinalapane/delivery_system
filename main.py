# Christina LaPane Student ID: 008207171

import truck
from truck import create_best_route, truck2, total_miles, deliver, truck3, secondRound, thirdRound, first_round, \
    allTimes


# user interface
def ui():
    print("ENTER WITH NUMBER KEY WHAT YOU WOULD LIKE TO DO")
    print("[1]: Load packages into system and see simulated day")
    print("[2]: Search for a package via package ID")
    print("[3]: Enter a time to view status of all packages")
    print('[0]: EXIT')
    response = input(">")

    # [0] Exit function
    if response == "0":
        print("GOODBYE!")
        SystemExit

    # [1] Load package and see simulated day and answers to G1 - G3
    if response == "1":
        print("------------------------------------------------------------------------------------------------------")
        print("TIME IS NOW 8:00 AND PACKAGES HAVE BEEN LOADED")
        create_best_route()
        # prints the total amount of packages in each truck (16 max each)
        print('---------------------------------------------------')
        print("Truck and package information after loading: ")
        print("Truck 1 has", len(truck.truck1.truckPackage), "packages ")
        print("Truck 2 has", len(truck2.truckPackage), "packages ")
        print("Truck 3 has", len(truck3.truckPackage), "packages ")
        print('---------------------------------------------------')

        print('OVERVIEW OF PROJECTED DAY: ')
        deliver()
        print("\nNEXT STEP:  \n"
              "[1]: SEE ROUND 1 DELIVERIES (8:35 AM - 9:25 AM) "
              "\n[0]: EXIT")
        status1 = input(">")
        print("------------------------------------------------------------------------------------------------------")

        if status1 == "0":
            print("GOODBYE!")
            SystemExit

        if status1 == "1":
            first_round()  # packages for g1

            print(
                '------------------------------------------------------------------------------------------------------')
            print("NEXT:\n[1]: SEE STATUS OF ROUND TWO (9:35 AM - 10:20 AM) \n[0]: EXIT")
            status2 = input(">")

            if status2 == "0":
                print("GOODBYE!")
                SystemExit
            if status2 == "1":
                print(
                    "------------------------------------------------------------------------------------------------------")

                secondRound()
                print(
                    "------------------------------------------------------------------------------------------------------")
                print(
                    "URGENT! TIME IS 10:20 AM-  PACKAGE 9 ADDRESS IS INCORRECT")  # after round 2, at 10:20, package 9 needs to be updated
                print("[1]: UPDATE ADDRESS \n[0]: EXIT")
                fix = input(">")
                print(
                    "------------------------------------------------------------------------------------------------------")

                if fix == "0":
                    print("GOODBYE!")
                    SystemExit

                if fix == "1":
                    print("ADDRESS HAS BEEN UPDATED! AND IS ON ITS WAY ")
                    print()
                print(
                    '------------------------------------------------------------------------------------------------------')
                print("NEXT: \n[1]: SEE STATUS OF FINAL ROUND (12:03 PM - 1:12 PM)\n[0]: EXIT")
                status3 = input(">")

                if status3 == "0":
                    print("GOODBYE!")
                    SystemExit
                if status3 == "1":

                    thirdRound()
                    print(
                        '\n------------------------------------------------------------------------------------------------------')
                    print("SEE SUMMARY OF DAY\n[1]: SUMMARY \n[0]: EXIT")
                    summary = input(">")

                    if summary == "0":
                        print("GOODBYE!")
                        SystemExit
                    if summary == "1":
                        total_miles()  # shows total miles of all trucks
                        print("All trucks back at HUB by {}".format(
                            truck3.currentTime))  # what time truck3 returns to HUB- last truck

    # [2] : Look at package status through package_id .
    if response == "2":
        create_best_route()
        check = '1'
        while check == "1":
            print("Check the status of a package by package ID (1-40)")
            search_string = input("Enter package ID: ")
            try:
                user_int = int(search_string)
                truck.search_id(user_int)
            except ValueError:  # invalid entry, can try again or exit
                print("You did not enter a valid package ID (1 - 40)")
            again = input("[1]: TRY AGAIN \n[0]: EXIT ")
            check = again
        ui()

    # [3] see status - enter time and will see all packages
    if response == "3":
        print('Enter time to check status of all packages on all trucks')
        print('Enter time as 12 hour format...Example: 1:30 PM')
        time_query = input('>')

        allTimes(time_query)


# main screen
print("------------------------------------------------------------------------------------------------------")
print("                               WELCOME TO WGUPS PROGRAM")
print("                                 CURRENT TIME IS 7:59")
print("------------------------------------------------------------------------------------------------------")
ui()


