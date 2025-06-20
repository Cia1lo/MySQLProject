-- SQL Queries for Resource Reservation System

-- User Management
-- Create User
INSERT INTO users (username, password, user_type, contact, email) 
VALUES (?, ?, ?, ?, ?);

-- Read User (Admin view with sensitive data)
SELECT * FROM users WHERE user_id = ?;

-- Read User (Regular view without sensitive data)
SELECT user_id, username, user_type FROM users WHERE user_id = ?;

-- Update User
UPDATE users 
SET username = ?, password = ?, user_type = ?, contact = ?, email = ? 
WHERE user_id = ?;

-- Delete User
DELETE FROM users WHERE user_id = ?;

-- Resource Management
-- Create Resource
INSERT INTO resources (name, category, location, is_available) 
VALUES (?, ?, ?, ?);

-- Read Resource
SELECT * FROM resources WHERE resource_id = ?;

-- Read All Resources
SELECT * FROM resources;

-- Update Resource
UPDATE resources 
SET name = ?, category = ?, location = ?, is_available = ? 
WHERE resource_id = ?;

-- Delete Resource
DELETE FROM resources WHERE resource_id = ?;

-- Reservation Management
-- Create Reservation
INSERT INTO reservations (user_id, resource_id, start_time, end_time, is_recurring, recurrence_pattern) 
VALUES (?, ?, ?, ?, ?, ?);

-- Read Reservation
SELECT * FROM reservations WHERE reservation_id = ?;

-- Read User Reservations
SELECT r.*, res.name AS resource_name, res.category, res.location 
FROM reservations r
JOIN resources res ON r.resource_id = res.resource_id
WHERE r.user_id = ?;

-- Read Resource Reservations (for conflict checking)
SELECT * FROM reservations 
WHERE resource_id = ? 
AND ((start_time <= ? AND end_time >= ?) OR (start_time <= ? AND end_time >= ?))
AND reservation_id != ?;

-- Update Reservation
UPDATE reservations 
SET start_time = ?, end_time = ?, is_recurring = ?, recurrence_pattern = ? 
WHERE reservation_id = ?;

-- Delete Reservation
DELETE FROM reservations WHERE reservation_id = ?;

-- Classified Query (Admin: Detailed User Info for Resource Usage)
SELECT r.reservation_id, r.start_time, r.end_time, u.user_id, u.username, u.user_type, u.contact, u.email
FROM reservations r
JOIN users u ON r.user_id = u.user_id
WHERE r.resource_id = ?;

-- Classified Query (Regular: Only Occupancy Status)
SELECT r.reservation_id, r.start_time, r.end_time, 'Occupied' AS status
FROM reservations r
WHERE r.resource_id = ?;
