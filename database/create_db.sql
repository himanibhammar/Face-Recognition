CREATE DATABASE face_recognition_db;

USE face_recognition_db;

CREATE TABLE checkins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_name VARCHAR(255),
    checkin_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    face_encoding BLOB
);