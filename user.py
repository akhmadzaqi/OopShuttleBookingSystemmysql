from prettytable import PrettyTable
from database import Database
import inquirer


def user_menu():
    questions = [
        inquirer.List('action',
                      message="Select an option:",
                      choices=[
                          ('Login', 'login'),
                          ('Register', 'register'),
                          ('Check Shuttle Availability', 'check_availability'),
                          ('Make Reservation', 'make_reservation'),
                          ('View Reservation', 'view_reservation'),
                          ('Exit', 'exit'),
                      ],
                      ),
    ]

    answers = inquirer.prompt(questions)
    return answers['action']

class User(Database):
    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def register(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.conn.commit()

    def make_reservation(self, user_id, shuttle_id, num_tickets):
        query_select = "SELECT available_slots, price FROM shuttle_availability WHERE id = %s"
        self.cursor.execute(query_select, (shuttle_id,))
        result = self.cursor.fetchone()

        if result:
            available_slots, shuttle_price = result[0], result[1]

            if num_tickets <= available_slots:
                total_price = num_tickets * shuttle_price

                query_insert = "INSERT INTO reservations (user_id, shuttle_id, num_tickets, total_price) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query_insert, (user_id, shuttle_id, num_tickets, total_price))
                self.conn.commit()

                # Update the number of available slots
                new_available_slots = available_slots - num_tickets
                query_update = "UPDATE shuttle_availability SET available_slots = %s WHERE id = %s"
                self.cursor.execute(query_update, (new_available_slots, shuttle_id))
                self.conn.commit()

                print(f"Reservation successful. Total Price: Rp.{total_price:.2f}")
            else:
                print("Insufficient available slots for the requested number of tickets.")
        else:
            print("Invalid shuttle ID.")


    def check_shuttle_availability(self, departure_date):
        query = "SELECT * FROM shuttle_availability WHERE departure_date = %s"
        self.cursor.execute(query, (departure_date,))
        return self.cursor.fetchall()
    
    def view_reservations(self, user_id):
        # Fetch user details
        user_query = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(user_query, (user_id,))
        user_info = self.cursor.fetchone()

        # Fetch reservations for the user
        reservations_query = """
            SELECT r.id, sa.departure_date, sa.departure_time, sa.shuttle_number, sa.destination, r.num_tickets, r.total_price
            FROM reservations r
            JOIN shuttle_availability sa ON r.shuttle_id = sa.id
            WHERE r.user_id = %s
        """
        self.cursor.execute(reservations_query, (user_id,))
        reservations = self.cursor.fetchall()

        if user_info and reservations:
            # Display user information
            print("User Information:")
            print(f"User ID: {user_info[0]}")
            print(f"Username: {user_info[1]}")
            print("+----------------+---------------+")

            # Display reservations
            for reservation in reservations:
                reservation_id, departure_date, departure_time, shuttle_number, destination, num_tickets, total_price = (
                    reservation[0],
                    reservation[1] or "N/A",
                    reservation[2] or "N/A",
                    reservation[3] or "N/A",
                    reservation[4] or "N/A",
                    reservation[5] or 0,
                    reservation[6] or 0.0,
                )

                # Create a PrettyTable for each reservation
                table = PrettyTable()
                table.field_names = ["Item", "Details"]
                table.add_row(["Reservation ID", reservation_id])
                table.add_row(["Departure Date", departure_date])
                table.add_row(["Departure Time", departure_time])
                table.add_row(["Shuttle Number", shuttle_number])
                table.add_row(["Destination", destination])
                table.add_row(["Num Tickets", num_tickets])
                table.add_row(["Total Price", f"Rp.{total_price:.2f}"])

                # Print the PrettyTable for each reservation
                print("+----------------+---------------+")
                print("        TICKET RESERVATION      ")
                print("+----------------+---------------+")
                print(table)
                print("+----------------+---------------+\n")

        elif not user_info:
            print("User not found.")
        else:
            print("No ticket reservations found for the user.")
