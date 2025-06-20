# Resource Reservation System Functionality Analysis

This document provides an analysis of the functionalities available to Admin and Regular users in the Resource Reservation System project, along with the corresponding functions in the codebase that implement these features. The content is structured to facilitate conversion into a PowerPoint presentation.

## Slide 1: Title Slide
- **Title**: Resource Reservation System - Functionality Analysis
- **Subtitle**: Overview of Features for Admin and Regular Users
- **Date**: June 17, 2025

## Slide 2: Introduction
- **Content**:
  - The Resource Reservation System is a Python-based application with a MySQL backend and a tkinter GUI.
  - It manages public resource reservations with distinct roles for Admin and Regular users (Students/Teachers).
  - This analysis details the functionalities for each user type and maps them to specific methods in the codebase.

## Slide 3: User Roles Overview
- **Admin User**:
  - Full access to system management features.
  - Can view and modify user and resource data.
- **Regular User (Student/Teacher)**:
  - Limited access focused on personal reservations and resource availability.
  - Privacy restrictions on viewing detailed user information.

## Slide 4: Regular User Functionalities - Login
- **Functionality**: Login to the system
  - **Description**: Allows Regular users to authenticate and access their personalized interface.
  - **Corresponding Functions**:
    - `login(username, password)` in `main.py` - Authenticates user credentials.
    - `get_user_by_username(username, is_admin=False)` in `database.py` - Retrieves user data with limited fields for Regular users.

## Slide 5: Regular User Functionalities - View Resources
- **Functionality**: View available resources
  - **Description**: Displays a list of resources with details like ID, name, category, location, and availability status.
  - **Corresponding Functions**:
    - `setup_resources_tab(notebook)` in `main.py` - Sets up the Resources tab with a list of resources.
    - `get_all_resources()` in `database.py` - Fetches all resource data from the database.

## Slide 6: Regular User Functionalities - View Resource Usage
- **Functionality**: View resource usage (limited view)
  - **Description**: Shows occupancy status of a selected resource without user details for privacy.
  - **Corresponding Functions**:
    - `view_usage(selection)` in `main.py` - Displays usage based on user privilege (Regular users see limited data).
    - `get_resource_usage_regular(resource_id)` in `database.py` - Retrieves usage data with only status information.

## Slide 7: Regular User Functionalities - View My Reservations
- **Functionality**: View personal reservations
  - **Description**: Lists all reservations made by the user with details of the resource and time slots.
  - **Corresponding Functions**:
    - `setup_reservations_tab(notebook)` in `main.py` - Sets up the My Reservations tab with user's reservation list.
    - `get_user_reservations(user_id)` in `database.py` - Fetches reservation data for a specific user.

## Slide 8: Regular User Functionalities - Make Reservation
- **Functionality**: Make a new reservation
  - **Description**: Allows users to reserve a resource by selecting it and specifying a time slot, with conflict checking.
  - **Corresponding Functions**:
    - `make_reservation()` in `main.py` - Opens a dialog for reservation input.
    - `save_reservation(resource_str, start_str, end_str, window)` in `main.py` - Saves the reservation after validation.
    - `check_conflict(resource_id, start_time, end_time, reservation_id=None)` in `database.py` - Checks for time slot conflicts.
    - `add_reservation(user_id, resource_id, start_time, end_time, is_recurring=False, recurrence_pattern="")` in `database.py` - Adds the reservation to the database.

## Slide 9: Regular User Functionalities - Cancel Reservation
- **Functionality**: Cancel a reservation
  - **Description**: Enables users to cancel their existing reservations.
  - **Corresponding Functions**:
    - `cancel_reservation(selection)` in `main.py` - Handles cancellation of a selected reservation.
    - `delete_reservation(reservation_id, user_id)` in `database.py` - Removes the reservation from the database.

## Slide 10: Admin User Functionalities - Login
- **Functionality**: Login to the system
  - **Description**: Allows Admin users to authenticate and access the full system management interface.
  - **Corresponding Functions**:
    - `login(username, password)` in `main.py` - Authenticates user credentials.
    - `get_user_by_username(username, is_admin=True)` in `database.py` - Retrieves full user data for Admin users.

## Slide 11: Admin User Functionalities - View Resources
- **Functionality**: View available resources
  - **Description**: Same as Regular users, displays a list of resources with full details.
  - **Corresponding Functions**:
    - `setup_resources_tab(notebook)` in `main.py` - Sets up the Resources tab with a list of resources.
    - `get_all_resources()` in `database.py` - Fetches all resource data from the database.

## Slide 12: Admin User Functionalities - View Resource Usage
- **Functionality**: View resource usage (full view)
  - **Description**: Shows detailed usage information including user data associated with reservations.
  - **Corresponding Functions**:
    - `view_usage(selection)` in `main.py` - Displays usage based on user privilege (Admin sees full data).
    - `get_resource_usage_admin(resource_id)` in `database.py` - Retrieves detailed usage data including user information.

## Slide 13: Admin User Functionalities - View My Reservations
- **Functionality**: View personal reservations
  - **Description**: Same as Regular users, lists all reservations made by the Admin.
  - **Corresponding Functions**:
    - `setup_reservations_tab(notebook)` in `main.py` - Sets up the My Reservations tab with user's reservation list.
    - `get_user_reservations(user_id)` in `database.py` - Fetches reservation data for a specific user.

## Slide 14: Admin User Functionalities - Make Reservation
- **Functionality**: Make a new reservation
  - **Description**: Same as Regular users, allows Admin to reserve resources with conflict checking.
  - **Corresponding Functions**:
    - `make_reservation()` in `main.py` - Opens a dialog for reservation input.
    - `save_reservation(resource_str, start_str, end_str, window)` in `main.py` - Saves the reservation after validation.
    - `check_conflict(resource_id, start_time, end_time, reservation_id=None)` in `database.py` - Checks for time slot conflicts.
    - `add_reservation(user_id, resource_id, start_time, end_time, is_recurring=False, recurrence_pattern="")` in `database.py` - Adds the reservation to the database.

## Slide 15: Admin User Functionalities - Cancel Reservation
- **Functionality**: Cancel a reservation
  - **Description**: Same as Regular users, enables Admin to cancel their reservations.
  - **Corresponding Functions**:
    - `cancel_reservation(selection)` in `main.py` - Handles cancellation of a selected reservation.
    - `delete_reservation(reservation_id, user_id)` in `database.py` - Removes the reservation from the database.

## Slide 16: Admin User Functionalities - Add Resource
- **Functionality**: Add a new resource
  - **Description**: Allows Admin to add new resources to the system with details like name, category, and location.
  - **Corresponding Functions**:
    - `add_resource()` in `main.py` - Opens a dialog for resource input.
    - `save_resource(name, category, location, window)` in `main.py` - Saves the new resource.
    - `add_resource(name, category, location, is_available=True)` in `database.py` - Adds the resource to the database.

## Slide 17: Admin User Functionalities - Add User
- **Functionality**: Add a new user
  - **Description**: Enables Admin to create new user accounts with full details and user type specification.
  - **Corresponding Functions**:
    - `add_user()` in `main.py` - Opens a dialog for user input.
    - `save_user(username, password, user_type, contact, email, window)` in `main.py` - Saves the new user.
    - `add_user(username, password, user_type, contact, email)` in `database.py` - Adds the user to the database.

## Slide 18: Admin User Functionalities - Search Users
- **Functionality**: Search for users by criteria
  - **Description**: Allows Admin to search users by username, email, or contact, with detailed results including reservation history for username searches.
  - **Corresponding Functions**:
    - `search_users()` in `main.py` - Opens a search dialog.
    - `perform_user_search(search_term, search_by, window)` in `main.py` - Performs the search and displays results.
    - `search_users(search_term, search_by='username', is_admin=True)` in `database.py` - Searches users by criteria with full details for Admin.
    - `get_user_with_reservations(username)` in `database.py` - Fetches user details and reservation history for username search.

## Slide 19: Admin User Functionalities - View All Users
- **Functionality**: View all users
  - **Description**: Displays a complete list of all users in the system with full details.
  - **Corresponding Functions**:
    - `view_all_users()` in `main.py` - Displays a window with a list of all users.
    - `search_users("", "username", is_admin=True)` in `database.py` - Retrieves all user data.

## Slide 20: Admin User Functionalities - Users by Category & Time
- **Functionality**: Search users by resource category and time frame
  - **Description**: Enables Admin to find users who reserved resources of a specific category within a time period using a nested query.
  - **Corresponding Functions**:
    - `users_by_category_time()` in `main.py` - Opens a dialog for inputting category and time frame.
    - `perform_category_time_search(category, start_str, end_str, window)` in `main.py` - Executes the search and displays results.
    - `get_users_by_category_and_time(category, start_time, end_time)` in `database.py` - Performs the nested query to fetch usernames.

## Slide 21: Conclusion
- **Content**:
  - The Resource Reservation System provides a robust set of functionalities tailored to Admin and Regular user roles.
  - Admin users have comprehensive management capabilities, while Regular users focus on personal reservation management with privacy considerations.
  - Each functionality is supported by specific methods in `main.py` for GUI interactions and `database.py` for backend operations.

## Slide 22: Q&A
- **Content**:
  - Questions and Answers
  - Thank you for reviewing this analysis of the Resource Reservation System functionalities.

---

**Note**: This Markdown document can be used as a basis for creating a PowerPoint presentation by converting each slide section into individual slides with bullet points, images, or diagrams as needed. Tools like Markdown to PPT converters or manual slide creation in PowerPoint can be utilized to finalize the presentation.
