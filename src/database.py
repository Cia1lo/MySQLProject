import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host="localhost", user="root", password="114514Abc", database="resource_reservation"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(prepared=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False

    def disconnect(self):
        if self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()

    def execute_query(self, query, params=()):
        if self.connection is None or not self.connection.is_connected():
            if not self.connect():
                print("Failed to connect to database")
                return None
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                if "INSERT" in query.upper():
                    return self.cursor.lastrowid
                else:
                    return self.cursor.rowcount
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    # User Management
    def add_user(self, username, password, user_type, contact, email):
        query = "INSERT INTO users (username, password, user_type, contact, email) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_query(query, (username, password, user_type, contact, email))

    def get_user(self, user_id, is_admin=False):
        query = "SELECT * FROM users WHERE user_id = %s" if is_admin else "SELECT user_id, username, user_type FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,))
        return result[0] if result else None

    def get_user_by_username(self, username, is_admin=False):
        query = "SELECT * FROM users WHERE username = %s" if is_admin else "SELECT user_id, username, user_type FROM users WHERE username = %s"
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    def search_users(self, search_term, search_by='username', is_admin=False):
        if search_by not in ['username', 'email', 'contact']:
            return []
        query = f"SELECT * FROM users WHERE {search_by} LIKE %s" if is_admin else f"SELECT user_id, username, user_type FROM users WHERE {search_by} LIKE %s"
        result = self.execute_query(query, (f'%{search_term}%',))
        return result if result else []

    def get_user_with_reservations(self, username):
        query = """
        SELECT u.user_id, u.username, u.user_type, u.contact, u.email,
               r.reservation_id, r.start_time, r.end_time, res.name AS resource_name, res.category, res.location
        FROM users u
        LEFT JOIN reservations r ON u.user_id = r.user_id
        LEFT JOIN resources res ON r.resource_id = res.resource_id
        WHERE u.username = %s
        """
        return self.execute_query(query, (username,))

    def get_users_by_category_and_time(self, category, start_time, end_time):
        query = """
        SELECT DISTINCT u.username
        FROM users u
        WHERE u.user_id IN (
            SELECT r.user_id
            FROM reservations r
            WHERE r.resource_id IN (
                SELECT res.resource_id
                FROM resources res
                WHERE res.category = %s
            )
            AND r.start_time BETWEEN %s AND %s
        )
        """
        return self.execute_query(query, (category, start_time, end_time))

    # Resource Management
    def add_resource(self, name, category, location, is_available=True):
        query = "INSERT INTO resources (name, category, location, is_available) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (name, category, location, is_available))

    def get_resource(self, resource_id):
        query = "SELECT * FROM resources WHERE resource_id = %s"
        result = self.execute_query(query, (resource_id,))
        return result[0] if result else None

    def get_all_resources(self):
        query = "SELECT * FROM resources"
        return self.execute_query(query)

    def update_resource(self, resource_id, name, category, location, is_available):
        query = "UPDATE resources SET name = %s, category = %s, location = %s, is_available = %s WHERE resource_id = %s"
        return self.execute_query(query, (name, category, location, is_available, resource_id))

    # Reservation Management
    def add_reservation(self, user_id, resource_id, start_time, end_time, is_recurring=False, recurrence_pattern=""):
        query = "INSERT INTO reservations (user_id, resource_id, start_time, end_time, is_recurring, recurrence_pattern) VALUES (%s, %s, %s, %s, %s, %s)"
        return self.execute_query(query, (user_id, resource_id, start_time, end_time, is_recurring, recurrence_pattern))

    def get_user_reservations(self, user_id):
        query = """
        SELECT reservation_id, start_time, end_time, resource_name, category, location
        FROM user_reservations_view
        WHERE user_id = %s
        """
        return self.execute_query(query, (user_id,))

    def delete_reservation(self, reservation_id, user_id):
        query = "DELETE FROM reservations WHERE reservation_id = %s AND user_id = %s"
        return self.execute_query(query, (reservation_id, user_id))

    def check_conflict(self, resource_id, start_time, end_time, reservation_id=None):
        query = """
        SELECT * FROM reservations 
        WHERE resource_id = %s 
        AND ((start_time <= %s AND end_time >= %s) OR (start_time <= %s AND end_time >= %s))
        """
        params = (resource_id, start_time, start_time, end_time, end_time)
        if reservation_id:
            query += " AND reservation_id != %s"
            params += (reservation_id,)
        result = self.execute_query(query, params)
        return len(result) > 0

    # Classified Query
    def get_resource_usage_admin(self, resource_id):
        query = """
        SELECT reservation_id, start_time, end_time, username, user_type, contact, email
        FROM resource_usage_admin_view
        WHERE resource_id = %s
        """
        return self.execute_query(query, (resource_id,))

    def get_resource_usage_regular(self, resource_id):
        query = """
        SELECT reservation_id, start_time, end_time, status
        FROM resource_usage_regular_view
        WHERE resource_id = %s
        """
        return self.execute_query(query, (resource_id,))

    def get_reservations_by_date_range(self, start_time, end_time, resource_id=None):
        query = """
        SELECT r.*, res.name AS resource_name, res.category, res.location, u.username
        FROM reservations r
        JOIN resources res ON r.resource_id = res.resource_id
        JOIN users u ON r.user_id = u.user_id
        WHERE r.start_time BETWEEN %s AND %s
        """
        params = (start_time, end_time)
        if resource_id:
            query += " AND r.resource_id = %s"
            params += (resource_id,)
        return self.execute_query(query, params)
