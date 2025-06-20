import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database

class ResourceReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource Reservation System")
        self.db = Database()
        self.current_user = None
        self.is_admin = False
        self.setup_login_screen()

    def setup_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Button(self.root, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get())).pack(pady=10)

    def login(self, username, password):
        user = self.db.get_user_by_username(username, is_admin=True)
        if user and user[2] == password:  # Simple password check (in real app, use hashing)
            self.current_user = user
            self.is_admin = user[3] == 'Admin'
            self.setup_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def setup_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_user[1]}", font=("Arial", 14)).pack(pady=10)
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # Tabs
        self.setup_resources_tab(notebook)
        self.setup_reservations_tab(notebook)
        self.setup_calendar_tab(notebook)
        if self.is_admin:
            self.setup_admin_tab(notebook)

        tk.Button(self.root, text="Logout", command=self.setup_login_screen).pack(pady=10)

    def setup_resources_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Resources")
        resources = self.db.get_all_resources()
        tree = ttk.Treeview(frame, columns=('ID', 'Name', 'Category', 'Location', 'Available'), show='headings')
        for col in ('ID', 'Name', 'Category', 'Location', 'Available'):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill='both')
        for res in resources:
            tree.insert('', tk.END, values=res)
        tk.Button(frame, text="View Usage", command=lambda: self.view_usage(tree.selection())).pack(pady=5)

    def setup_reservations_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="My Reservations")
        reservations = self.db.get_user_reservations(self.current_user[0])
        tree = ttk.Treeview(frame, columns=('ID', 'Resource', 'Start Time', 'End Time'), show='headings')
        for col in ('ID', 'Resource', 'Start Time', 'End Time'):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill='both')
        for res in reservations:
            tree.insert('', tk.END, values=(res[0], res[3], res[1], res[2]))
        tk.Button(frame, text="Make Reservation", command=self.make_reservation).pack(pady=5)
        tk.Button(frame, text="Cancel Reservation", command=lambda: self.cancel_reservation(tree.selection())).pack(pady=5)

    def setup_calendar_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Calendar View")
        tk.Label(frame, text="Select Date Range for Calendar View", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(frame, text="Start Date (YYYY-MM-DD):").pack()
        start_date_entry = tk.Entry(frame)
        start_date_entry.pack()
        start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(frame, text="End Date (YYYY-MM-DD):").pack()
        end_date_entry = tk.Entry(frame)
        end_date_entry.pack()
        end_date_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
        
        tk.Button(frame, text="Show Calendar", command=lambda: self.show_calendar_view(start_date_entry.get(), end_date_entry.get(), frame)).pack(pady=10)

    def show_calendar_view(self, start_date_str, end_date_str, frame):
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if start_date >= end_date:
                messagebox.showerror("Error", "End date must be after start date")
                return
                
            # Clear previous calendar view if any
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Treeview):
                    widget.destroy()
                    
            reservations = self.db.get_reservations_by_date_range(start_date, end_date)
            tree = ttk.Treeview(frame, columns=('ID', 'Resource', 'Username', 'Start Time', 'End Time'), show='headings')
            for col in ('ID', 'Resource', 'Username', 'Start Time', 'End Time'):
                tree.heading(col, text=col)
            tree.pack(expand=True, fill='both')
            
            for res in reservations:
                tree.insert('', tk.END, values=(res[0], res[7], res[10], res[3], res[4]))
                
            if not reservations:
                messagebox.showinfo("No Reservations", "No reservations found for the selected date range")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")

    def setup_admin_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Admin")
        tk.Button(frame, text="Add Resource", command=self.add_resource).pack(pady=5)
        tk.Button(frame, text="Add User", command=self.add_user).pack(pady=5)
        tk.Button(frame, text="Search Users", command=self.search_users).pack(pady=5)
        tk.Button(frame, text="View All Users", command=self.view_all_users).pack(pady=5)
        tk.Button(frame, text="Users by Category & Time", command=self.users_by_category_time).pack(pady=5)

    def view_usage(self, selection):
        if not selection:
            messagebox.showerror("Error", "Please select a resource")
            return
        resource_id = self.get_selected_id(selection[0])
        if self.is_admin:
            usage = self.db.get_resource_usage_admin(resource_id)
        else:
            usage = self.db.get_resource_usage_regular(resource_id)
        self.show_usage_window(resource_id, usage)

    def show_usage_window(self, resource_id, usage):
        window = tk.Toplevel(self.root)
        window.title(f"Usage for Resource ID {resource_id}")
        tree = ttk.Treeview(window, columns=[col for col in range(len(usage[0]) if usage else 0)], show='headings')
        for i in range(len(usage[0]) if usage else 0):
            tree.heading(i, text=f"Field {i+1}")
        tree.pack(expand=True, fill='both')
        for row in usage:
            tree.insert('', tk.END, values=row)

    def make_reservation(self):
        window = tk.Toplevel(self.root)
        window.title("Make Reservation")
        tk.Label(window, text="Select Resource:").pack()
        resources = self.db.get_all_resources()
        resource_var = tk.StringVar()
        ttk.Combobox(window, textvariable=resource_var, values=[f"{r[0]} - {r[1]}" for r in resources]).pack()
        tk.Label(window, text="Start Time (YYYY-MM-DD HH:MM):").pack()
        start_entry = tk.Entry(window)
        start_entry.pack()
        tk.Label(window, text="End Time (YYYY-MM-DD HH:MM):").pack()
        end_entry = tk.Entry(window)
        end_entry.pack()
        tk.Button(window, text="Reserve", command=lambda: self.save_reservation(resource_var.get(), start_entry.get(), end_entry.get(), window)).pack(pady=10)

    def save_reservation(self, resource_str, start_str, end_str, window):
        try:
            resource_id = int(resource_str.split(' - ')[0])
            start_time = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(end_str, '%Y-%m-%d %H:%M')
            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be after start time")
                return
            if self.db.check_conflict(resource_id, start_time, end_time):
                messagebox.showerror("Error", "Time slot conflict")
                return
            self.db.add_reservation(self.current_user[0], resource_id, start_time, end_time)
            messagebox.showinfo("Success", "Reservation made")
            window.destroy()
            self.setup_main_screen()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")

    def add_resource(self):
        window = tk.Toplevel(self.root)
        window.title("Add Resource")
        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()
        tk.Label(window, text="Category:").pack()
        cat_entry = tk.Entry(window)
        cat_entry.pack()
        tk.Label(window, text="Location:").pack()
        loc_entry = tk.Entry(window)
        loc_entry.pack()
        tk.Button(window, text="Add", command=lambda: self.save_resource(name_entry.get(), cat_entry.get(), loc_entry.get(), window)).pack(pady=10)

    def save_resource(self, name, category, location, window):
        if name and category and location:
            self.db.add_resource(name, category, location)
            messagebox.showinfo("Success", "Resource added")
            window.destroy()
            self.setup_main_screen()
        else:
            messagebox.showerror("Error", "All fields are required")

    def add_user(self):
        window = tk.Toplevel(self.root)
        window.title("Add User")
        tk.Label(window, text="Username:").pack()
        user_entry = tk.Entry(window)
        user_entry.pack()
        tk.Label(window, text="Password:").pack()
        pass_entry = tk.Entry(window, show="*")
        pass_entry.pack()
        tk.Label(window, text="Type (Admin/Regular):").pack()
        type_var = tk.StringVar(value="Regular")
        ttk.Combobox(window, textvariable=type_var, values=["Admin", "Regular"]).pack()
        tk.Label(window, text="Contact:").pack()
        contact_entry = tk.Entry(window)
        contact_entry.pack()
        tk.Label(window, text="Email:").pack()
        email_entry = tk.Entry(window)
        email_entry.pack()
        tk.Button(window, text="Add", command=lambda: self.save_user(user_entry.get(), pass_entry.get(), type_var.get(), contact_entry.get(), email_entry.get(), window)).pack(pady=10)

    def save_user(self, username, password, user_type, contact, email, window):
        if username and password and user_type:
            self.db.add_user(username, password, user_type, contact, email)
            messagebox.showinfo("Success", "User added")
            window.destroy()
            self.setup_main_screen()
        else:
            messagebox.showerror("Error", "Username, password, and type are required")

    def cancel_reservation(self, selection):
        if not selection:
            messagebox.showerror("Error", "Please select a reservation to cancel")
            return
        reservation_id = self.get_selected_id(selection[0])
        affected_rows = self.db.delete_reservation(reservation_id, self.current_user[0])
        if affected_rows is not None and affected_rows > 0:
            messagebox.showinfo("Success", "Reservation canceled")
            self.setup_main_screen()
        else:
            messagebox.showerror("Error", "Failed to cancel reservation")

    def search_users(self):
        window = tk.Toplevel(self.root)
        window.title("Search Users")
        tk.Label(window, text="Search Term:").pack()
        search_entry = tk.Entry(window)
        search_entry.pack()
        tk.Label(window, text="Search By:").pack()
        search_by_var = tk.StringVar(value="username")
        ttk.Combobox(window, textvariable=search_by_var, values=["username", "email", "contact"]).pack()
        tk.Button(window, text="Search", command=lambda: self.perform_user_search(search_entry.get(), search_by_var.get(), window)).pack(pady=10)

    def perform_user_search(self, search_term, search_by, window):
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term")
            return
        search_window = tk.Toplevel(window)
        search_window.title(f"Search Results for {search_term}")
        
        if search_by == "username":
            # Use the method to get user info with reservations for exact username match
            results = self.db.get_user_with_reservations(search_term)
            if not results:
                messagebox.showinfo("No Results", "No user found with the specified username")
                return
                
            # Display only username (taking the username from the first row)
            user_info = results[0][1:2]  # username only
            tk.Label(search_window, text="User Information", font=("Arial", 12, "bold")).pack(pady=5)
            user_tree = ttk.Treeview(search_window, columns=('Username',), show='headings')
            user_tree.heading('Username', text='Username')
            user_tree.pack(expand=True, fill='both')
            user_tree.insert('', tk.END, values=user_info)
            
            # Display reservation history with detailed resource information
            tk.Label(search_window, text="Reservation History with Resource Details", font=("Arial", 12, "bold")).pack(pady=5)
            res_tree = ttk.Treeview(search_window, columns=('Reservation ID', 'Start Time', 'End Time', 'Resource Name', 'Category', 'Location'), show='headings')
            for col in ('Reservation ID', 'Start Time', 'End Time', 'Resource Name', 'Category', 'Location'):
                res_tree.heading(col, text=col)
            res_tree.pack(expand=True, fill='both')
            reservation_found = False
            for row in results:
                if row[5] is not None:  # Check if reservation_id exists
                    reservation_found = True
                    res_tree.insert('', tk.END, values=(row[5], row[6], row[7], row[8], row[9], row[10]))
            if not reservation_found:
                tk.Label(search_window, text="No reservations found for this user").pack(pady=5)
        else:
            results = self.db.search_users(search_term, search_by, is_admin=True)
            tree = ttk.Treeview(search_window, columns=('ID', 'Username', 'Type', 'Contact', 'Email'), show='headings')
            for col in ('ID', 'Username', 'Type', 'Contact', 'Email'):
                tree.heading(col, text=col)
            tree.pack(expand=True, fill='both')
            for user in results:
                tree.insert('', tk.END, values=(user[0], user[1], user[3], user[4], user[5]))
            if not results:
                messagebox.showinfo("No Results", "No users found matching the search criteria")

    def view_all_users(self):
        window = tk.Toplevel(self.root)
        window.title("All Users")
        # Use search_users with an empty search term to get all users
        results = self.db.search_users("", "username", is_admin=True)
        tree = ttk.Treeview(window, columns=('ID', 'Username', 'Type', 'Contact', 'Email'), show='headings')
        for col in ('ID', 'Username', 'Type', 'Contact', 'Email'):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill='both')
        for user in results:
            tree.insert('', tk.END, values=(user[0], user[1], user[3], user[4], user[5]))
        if not results:
            messagebox.showinfo("No Users", "No users found in the system")

    def users_by_category_time(self):
        window = tk.Toplevel(self.root)
        window.title("Users by Category & Time")
        tk.Label(window, text="Resource Category:").pack()
        category_entry = tk.Entry(window)
        category_entry.pack()
        tk.Label(window, text="Start Time (YYYY-MM-DD HH:MM):").pack()
        start_entry = tk.Entry(window)
        start_entry.pack()
        tk.Label(window, text="End Time (YYYY-MM-DD HH:MM):").pack()
        end_entry = tk.Entry(window)
        end_entry.pack()
        tk.Button(window, text="Search", command=lambda: self.perform_category_time_search(category_entry.get(), start_entry.get(), end_entry.get(), window)).pack(pady=10)

    def perform_category_time_search(self, category, start_str, end_str, window):
        if not category or not start_str or not end_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        try:
            start_time = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(end_str, '%Y-%m-%d %H:%M')
            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be after start time")
                return
            results = self.db.get_users_by_category_and_time(category, start_time, end_time)
            search_window = tk.Toplevel(window)
            search_window.title(f"Users for Category {category} from {start_str} to {end_str}")
            tree = ttk.Treeview(search_window, columns=('Username',), show='headings')
            tree.heading('Username', text='Username')
            tree.pack(expand=True, fill='both')
            for user in results:
                tree.insert('', tk.END, values=user)
            if not results:
                messagebox.showinfo("No Results", f"No users found for category {category} in the specified time frame")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM")

    def get_selected_id(self, selection):
        return int(self.root.focus_get().item(selection)['values'][0])

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceReservationApp(root)
    root.mainloop()
