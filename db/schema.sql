-- Database Schema for Resource Reservation System

-- Create Database
CREATE DATABASE IF NOT EXISTS resource_reservation;
USE resource_reservation;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    user_type ENUM('Admin', 'Regular') NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100)
);

-- Resources Table
CREATE TABLE IF NOT EXISTS resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

-- Reservations Table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    resource_id INT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE
);

-- Insert Sample Data
INSERT INTO users (username, password, user_type, contact, email) VALUES
('admin1', 'adminpass', 'Admin', '1234567890', 'admin1@example.com'),
('user1', 'userpass', 'Regular', '0987654321', 'user1@example.com');

INSERT INTO resources (name, category, location, is_available) VALUES
('Projector A', 'Equipment', 'Room 101', TRUE),
('Lab Computer 1', 'Computer', 'Lab 202', TRUE);

-- Index for faster queries on reservations by time
CREATE INDEX idx_reservation_time ON reservations(start_time, end_time);

-- Views for simplified querying
-- View for User Reservations with Resource Details
CREATE VIEW user_reservations_view AS
SELECT u.user_id, u.username, r.reservation_id, r.start_time, r.end_time, res.name AS resource_name, res.category, res.location
FROM users u
JOIN reservations r ON u.user_id = r.user_id
JOIN resources res ON r.resource_id = res.resource_id;

-- View for Resource Usage (Admin perspective with user details)
CREATE VIEW resource_usage_admin_view AS
SELECT res.resource_id, res.name AS resource_name, res.category, res.location, r.reservation_id, r.start_time, r.end_time, u.username, u.user_type, u.contact, u.email
FROM resources res
JOIN reservations r ON res.resource_id = r.resource_id
JOIN users u ON r.user_id = u.user_id;

-- View for Resource Usage (Regular perspective with limited info)
CREATE VIEW resource_usage_regular_view AS
SELECT res.resource_id, res.name AS resource_name, res.category, res.location, r.reservation_id, r.start_time, r.end_time, 'Occupied' AS status
FROM resources res
JOIN reservations r ON res.resource_id = r.resource_id;
