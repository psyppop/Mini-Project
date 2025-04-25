CREATE DATABASE IF NOT EXISTS facerecognitiondb;
USE facerecognitiondb;


-- Create faces table
CREATE TABLE faces (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    encoding BLOB NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS face_recognition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    face_data LONGBLOB NOT NULL,
    face_image LONGBLOB
);

select * from face_recognition;

-- Create reference_images table
CREATE TABLE reference_images (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    image_encoding TEXT NOT NULL,
    image_path TEXT NOT NULL,
    PRIMARY KEY (id)
);








--create only the tables which are not there in your database forensync, and create the tables in forensync, i created another database because mere forensync wale mai problems the


CREATE DATABASE IF NOT EXISTS fms;
USE fms;

-- Create investigator table
CREATE TABLE investigator (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY (username)
);

-- Create supervisor table
CREATE TABLE supervisor (
    supervisor_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (supervisor_id),
    UNIQUE KEY (username)
);

-- Create cases table
CREATE TABLE cases (
    case_id INT NOT NULL AUTO_INCREMENT,
    investigator_id INT,
    description TEXT,
    status VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    PRIMARY KEY (case_id),
    KEY (investigator_id)
);

-- Create actions table
CREATE TABLE actions (
    action_id INT NOT NULL AUTO_INCREMENT,
    investigator_id INT,
    action_type VARCHAR(50),
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    case_id INT,
    PRIMARY KEY (action_id),
    KEY (investigator_id),
    KEY (case_id)
);

-- Add foreign key constraints
ALTER TABLE actions
    ADD CONSTRAINT fk_actions_investigator FOREIGN KEY (investigator_id) REFERENCES investigator (id),
    ADD CONSTRAINT fk_actions_case FOREIGN KEY (case_id) REFERENCES cases (case_id);
    
ALTER TABLE cases
    ADD CONSTRAINT fk_cases_investigator FOREIGN KEY (investigator_id) REFERENCES investigator (id);
    

INSERT INTO supervisor (username, password)
VALUES ('Supervisor1', 'Supervisor1');


-- Add this to your database setup

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

-- Permissions table
CREATE TABLE IF NOT EXISTS permissions (
    user_id INT,
    can_view BOOLEAN DEFAULT TRUE,
    can_upload BOOLEAN DEFAULT FALSE,
    can_edit BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Activity log table
CREATE TABLE IF NOT EXISTS activity_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');
INSERT INTO users (name, username, password, role, is_active) 
VALUES ('Admin User', 'admin', 'admin123', 'admin', TRUE);
