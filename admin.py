from database import Database
import inquirer

def admin_menu():
    questions = [
        inquirer.List('admin_choice',
                      message="Admin Menu:",
                      choices=[
                          "Create Shuttle Availability",
                          "Read Shuttle Availability",
                          "Update Shuttle Availability",
                          "Delete Shuttle Availability",
                          "Exit"
                      ],
        ),
    ]

    answer = inquirer.prompt(questions)
    return answer['admin_choice']

class Admin(Database):
    def login(self, username, password):
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def create_shuttle_availability(self, departure_date, departure_time, shuttle_number, destination, available_slots, price):
        query = "INSERT INTO shuttle_availability (departure_date, departure_time, shuttle_number, destination, available_slots, price) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (departure_date, departure_time, shuttle_number, destination, available_slots, price))
        self.conn.commit()

    def read_shuttle_availability(self, departure_date):
        query = "SELECT * FROM shuttle_availability WHERE departure_date = %s"
        self.cursor.execute(query, (departure_date,))
        return self.cursor.fetchall()

    def update_shuttle_availability(self, shuttle_id, new_available_slots):
        query = "UPDATE shuttle_availability SET available_slots = %s WHERE id = %s"
        self.cursor.execute(query, (new_available_slots, shuttle_id))
        self.conn.commit()

    def delete_shuttle_availability(self, shuttle_id):
        # Delete dependent records from reservations table first
        query_delete_reservations = "DELETE FROM reservations WHERE shuttle_id = %s"
        self.cursor.execute(query_delete_reservations, (shuttle_id,))
        self.conn.commit()

        # Now, delete the shuttle_availability record
        query_delete_shuttle = "DELETE FROM shuttle_availability WHERE id = %s"
        self.cursor.execute(query_delete_shuttle, (shuttle_id,))
        self.conn.commit()
