-- Create Views for Resource Reservation System

USE resource_reservation;

-- View for User Reservations with Resource Details
DROP VIEW IF EXISTS user_reservations_view;
CREATE VIEW user_reservations_view AS
SELECT u.user_id, u.username, r.reservation_id, r.start_time, r.end_time, res.name AS resource_name, res.category, res.location
FROM users u
JOIN reservations r ON u.user_id = r.user_id
JOIN resources res ON r.resource_id = res.resource_id;

-- View for Resource Usage (Admin perspective with user details)
DROP VIEW IF EXISTS resource_usage_admin_view;
CREATE VIEW resource_usage_admin_view AS
SELECT res.resource_id, res.name AS resource_name, res.category, res.location, r.reservation_id, r.start_time, r.end_time, u.username, u.user_type, u.contact, u.email
FROM resources res
JOIN reservations r ON res.resource_id = r.resource_id
JOIN users u ON r.user_id = u.user_id;

-- View for Resource Usage (Regular perspective with limited info)
DROP VIEW IF EXISTS resource_usage_regular_view;
CREATE VIEW resource_usage_regular_view AS
SELECT res.resource_id, res.name AS resource_name, res.category, res.location, r.reservation_id, r.start_time, r.end_time, 'Occupied' AS status
FROM resources res
JOIN reservations r ON res.resource_id = r.resource_id;
