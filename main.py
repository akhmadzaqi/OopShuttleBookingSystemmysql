from admin import Admin, admin_menu
from user import User, user_menu
from getpass import getpass
import os
from pyfiglet import Figlet
import inquirer

def print_banner(text):
    custom_fig = Figlet()
    print(custom_fig.renderText(text))

def main():
    admin_obj = Admin()
    user_obj = User()

    logged_in_user = None  # Menyimpan informasi pengguna yang sudah login
    departure_date = ""  # Menyimpan informasi pengguna yang sudah login

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')  # Clear the console
        print_banner("Shuttle ")
        print("Booking System")

        questions = [
            inquirer.List('choice',
                          message="Select an option:",
                          choices=['Admin', 'User', 'Exit'],
            ),
        ]

        answers = inquirer.prompt(questions)

        choice = answers['choice']

        if choice == 'Admin':
            username = input("Enter admin username: ")
            password = getpass("Enter admin password: ")

            admin_login = admin_obj.login(username, password)
            if admin_login:
                print("Admin login successful.")

                while True:
                    admin_menu_options = [
                        "Create Shuttle Availability",
                        "Read Shuttle Availability",
                        "Update Shuttle Availability",
                        "Delete Shuttle Availability",
                        "Exit",
                    ]

                    admin_menu_question = [
                        inquirer.List('admin_choice',
                                    message="Select an option:",
                                    choices=admin_menu_options,
                        ),
                    ]

                    admin_menu_answer = inquirer.prompt(admin_menu_question)
                    admin_choice = admin_menu_answer['admin_choice']

                    if admin_choice == 'Create Shuttle Availability':
                        departure_date = input("Enter departure date (YYYY-MM-DD): ")
                        departure_time = input("Enter departure time (HH:MM): ")
                        shuttle_number = input("Enter shuttle number: ")
                        destination = input("Enter destination: ")
                        available_slots = int(input("Enter available slots: "))
                        price = float(input("Enter price per ticket: "))  # Assuming the price is a decimal number

                        admin_obj.create_shuttle_availability(departure_date, departure_time, shuttle_number, destination, available_slots, price)
                        print("Shuttle availability created successfully.")

                    elif admin_choice == 'Read Shuttle Availability':
                        departure_date = input("Enter departure date (YYYY-MM-DD): ")
                        availability = admin_obj.read_shuttle_availability(departure_date)
                        if availability:
                            print("Shuttle Availability:")
                            for shuttle in availability:
                                print(f"ID: {shuttle[0]}, Date: {shuttle[1]}, Time: {shuttle[2]}, Shuttle Number: {shuttle[3]}, Destination: {shuttle[4]}, Available Slots: {shuttle[5]}")
                        else:
                            print("No shuttle availability found for the given date.")

                    elif admin_choice == 'Update Shuttle Availability':
                        shuttle_id = input("Enter shuttle ID to update: ")
                        new_available_slots = int(input("Enter new available slots: "))
                        admin_obj.update_shuttle_availability(shuttle_id, new_available_slots)
                        print("Shuttle availability updated successfully.")

                    elif admin_choice == 'Delete Shuttle Availability':
                        shuttle_id = input("Enter shuttle ID to delete: ")
                        admin_obj.delete_shuttle_availability(shuttle_id)
                        print("Shuttle availability deleted successfully.")

                    elif admin_choice == 'Exit':
                        break

                    else:
                        print("Invalid choice. Please select a valid option.")

            else:
                print("Admin login failed.")

        elif choice == 'User':
            user_menu_options = [
                "User Login",
                "User Registration",
                "Check Shuttle Availability",
                "Make Reservation",
                "View Reservations",
                "Exit",
            ]

            while True:
                user_menu_question = [
                    inquirer.List('user_choice',
                                message="Select an option:",
                                choices=user_menu_options,
                    ),
                ]

                user_menu_answer = inquirer.prompt(user_menu_question)
                user_choice = user_menu_answer['user_choice']

                if user_choice == 'User Login':
                    username = input("Enter username: ")
                    password = getpass("Enter password: ")
                    user_login = user_obj.login(username, password)

                    if user_login:
                        print(f"Welcome, {user_login[1]}!")  # Display personalized greeting
                        logged_in_user = user_login
                    else:
                        print("User login failed.")

                elif user_choice == 'User Registration':
                    username = input("Enter username: ")
                    password = getpass("Enter password: ")
                    user_obj.register(username, password)
                    print("User registered successfully.")

                elif user_choice == 'Check Shuttle Availability':
                    departure_date = input("Enter departure date (YYYY-MM-DD): ")
                    availability = user_obj.check_shuttle_availability(departure_date)
                    if availability:
                        print("Shuttle Availability:")
                        for shuttle in availability:
                            print(f"ID: {shuttle[0]}, Date: {shuttle[1]}, Time: {shuttle[2]}, Shuttle Number: {shuttle[3]}, Destination: {shuttle[4]}, Available Slots: {shuttle[5]}")
                    else:
                        print("No shuttle availability found for the given date.")

                elif user_choice == 'Make Reservation':
                    if logged_in_user:
                        try:
                            shuttle_id = int(input("Enter the Shuttle ID to book: "))
                            num_tickets = int(input("Enter the number of tickets: "))
                            user_obj.make_reservation(logged_in_user[0], shuttle_id, num_tickets)
                        except ValueError:
                            print("Invalid input. Please enter valid numbers.")
                    else:
                        print("Please log in before making a reservation.")

                elif user_choice == 'View Reservations':
                    if logged_in_user:
                        user_obj.view_reservations(logged_in_user[0])
                    else:
                        print("Please log in before viewing reservations.")

                elif user_choice == 'Exit':
                    break

                else:
                    print("Invalid choice. Please select a valid option.")

        elif choice == 'Exit':
            admin_obj.close_connection()
            user_obj.close_connection()
            print("Exiting the System.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
