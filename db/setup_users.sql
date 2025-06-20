-- Setup MySQL Users with Different Permissions for Resource Reservation System

-- Ensure the database is selected
USE resource_reservation;

-- Create Admin User with Full Privileges
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'AdminPass123!';
GRANT ALL PRIVILEGES ON resource_reservation.* TO 'admin_user'@'localhost';
FLUSH PRIVILEGES;

-- Create Regular User with Limited Privileges (SELECT, INSERT on specific tables)
CREATE USER IF NOT EXISTS 'regular_user'@'localhost' IDENTIFIED BY 'RegularPass123!';
GRANT SELECT, INSERT ON resource_reservation.users TO 'regular_user'@'localhost';
GRANT SELECT, INSERT ON resource_reservation.reservations TO 'regular_user'@'localhost';
GRANT SELECT ON resource_reservation.resources TO 'regular_user'@'localhost';
FLUSH PRIVILEGES;

-- Note: To revoke privileges or change permissions, use REVOKE statements
-- Example to revoke specific privilege:
-- REVOKE INSERT ON resource_reservation.reservations FROM 'regular_user'@'localhost';

-- Note: Admin can upgrade a regular user to admin by changing their user_type in the users table
-- and potentially granting additional privileges if a separate MySQL user account is created for them.
